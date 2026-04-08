#!/usr/bin/env python3
"""
Fill out TWC Work Search Activity Log PDF forms from CSV files.
Uses the original fillable PDF form.
Creates multiple pages if more than 5 activities.
"""

import csv
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import TextStringObject

# ---------------------------------------------------------------------------
# PDF field-name constants (Issue #118 / CQ-1)
#
# The TWC fillable PDF uses inconsistent naming for its form fields:
# double spaces, missing dashes, varying suffixes.  These dicts capture
# the *exact* field names so that every magic string lives in one place.
# Keys are 0-based activity indices (0-4).
# ---------------------------------------------------------------------------

HEADER_FIELDS = {
    "claimant_name": "Enter Claimant Name",
    "week_of": "Enter Week Of",
    "end_date": "Enter End Date",
    "ssn_first3": "Enter Social Security Number First 3 Digits",
    "ssn_mid2": "Enter Social Security Number Middle 2 Digits",
    "ssn_last4": "Enter Last 4 Digits of Social Security Number",
    "required_searches": "Enter Number of Required Searches",
}

# Per-activity field names, indexed 0-4
ACTIVITY_DATE_FIELDS: dict[int, str] = {
    0: "Enter Date of Job Search Activity",
    1: "Enter Date of Job Search Activity - 2",
    2: "Enter Date of Job Search Activity - 3",
    3: "Enter Date of Job Search Activity - 4",
    4: "Enter Date of Job Search Activity - 5",
}

WORK_SEARCH_FIELDS: dict[int, str] = {
    0: "Enter Work Search Activity",
    1: "Enter Work Search Activity - 2",
    2: "Enter Work Search Activity - 3",
    3: "Enter Work Search Activity - 4",
    4: "Enter Work Search Activity - 5",
}

JOB_TYPE_FIELDS: dict[int, str] = {
    0: "Enter Job Type",
    1: "Enter Job Type  - 2",       # double space in PDF
    2: "Enter Job Type - 3",
    3: "Enter Job Type - 4",
    4: "Enter Job Type - 5",
}

ORGANIZATION_NAME_FIELDS: dict[int, str] = {
    0: "Enter Name of Organization - 1",
    1: "Enter Name of Organization  - 2",   # double space
    2: "Enter Name of Organization - 3",
    3: "Enter Name of Organization  4",      # no dash
    4: "Enter Name of Organization - 5",
}

ADDRESS_FIELDS: dict[int, str] = {
    0: "Enter Street Address - Organization 1",
    1: "Enter Street Address - Organization - 2",
    2: "Enter Street Address - Organization - 3",
    3: "Enter Street Address - Organization 4",
    4: "Enter Street Address - Organization 5",
}

LOCATION_FIELDS: dict[int, str] = {
    0: "Enter City, State, Zip Code - Organization 1",
    1: "Enter City, State, Zip Code - Organization 2",
    2: "Enter City, State, Zip Code - Organization 3",
    3: "Enter City, State, Zip Code - Organization 4",
    4: "Enter City, State, Zip Code - Organization 5",
}

AREA_CODE_FIELDS: dict[int, str] = {
    0: "Enter Area Code - Organization 1",
    1: "Enter Area Code - Organization 2",
    2: "Enter Area Code - Organization 3",
    3: "Enter Area Code - Organization 4",
    4: "Enter Area Code - Organization 5",
}

PHONE_MIDDLE_FIELDS: dict[int, str] = {
    0: "Enter Middle 3 Phone Digits",
    1: "Enter Middle 3 Phone Digits - 2",
    2: "Enter Middle 3 Phone Digits - 3",
    3: "Enter Middle 3 Phone Digits - 4",
    4: "Enter Middle 3 Phone Digits - 5",
}

PHONE_LAST_FIELDS: dict[int, str] = {
    0: "Enter Last 4 Phone Digits",
    1: "Enter Last 4 Phone Digits - 2",
    2: "Enter Last 4 Phone Digits - 3",
    3: "Enter Last 4 Phone Digits - 4",
    4: "Enter Last 4 Phone Digits - 5",
}

EMAIL_CHECKBOX_FIELDS: dict[int, str] = {
    0: "Click this checkbox if you contacted organization by email",
    1: "Click this checkbox if you contacted organization by email - 2",
    2: "Click this checkbox if you contacted organization by email - 3",
    3: "Click this checkbox if you contacted organization by email - 4",
    4: "Click this checkbox if you contacted organization by email - 5",
}

MAIL_CHECKBOX_FIELDS: dict[int, str] = {
    0: "Click this checkbox if you contacted organization by mail - 1",
    1: "Click this checkbox if you contacted organization by mail - 2",
    2: "Click this checkbox if you contacted organization by mail - 3",
    3: "Click this checkbox if you contacted organization by mail  - 4",  # double space
    4: "Click this checkbox if you contacted organization by mail - 5",
}

FAX_CHECKBOX_FIELDS: dict[int, str] = {
    0: "Click this checkbox if you contacted organization by fax",
    1: "Click this checkbox if you contacted organization by fax -2",
    2: "Click this checkbox if you contacted organization by fax -3",
    3: "Click this checkbox if you contacted organization by fax -4",
    4: "Click this checkbox if you contacted organization by fax -5",
}

PERSON_CONTACTED_FIELDS: dict[int, str] = {
    0: "Enter Name of Person Contacted - Organization 1",
    1: "Enter Name of Person Contacted - Organization 2",
    2: "Enter Name of Person Contacted - Organization 3",
    3: "Enter Name of Person Contacted - Organization 4",
    4: "Enter Name of Person Contacted - Organization 5",
}

HIRED_CHECKBOX_FIELDS: dict[int, str] = {
    0: "Click This Checkbox If You Were Hired - 1",
    1: "Click This Checkbox If You Were Hired - 2",
    2: "Click This Checkbox If You Were Hired - 3",
    3: "Click This Checkbox If You Were Hired - 4",
    4: "Click This Checkbox If You Were Hired - 5",
}

NOT_HIRED_CHECKBOX_FIELDS: dict[int, str] = {
    0: "Click This Checkbox If Not Hired - 1",
    1: "Click This Checkbox If Not Hired - 2",
    2: "Click This Checkbox If Not Hired - 3",
    3: "Click This Checkbox If Not Hired - 4",
    4: "Click This Checkbox If Not Hired - 5",
}

APPLICATION_FILED_FIELDS: dict[int, str] = {
    0: "Click this Checkbox if You Filed an Application - 1",
    1: "Click this Checkbox if You Filed an Application - 2",
    2: "Click this Checkbox if You Filed an Application - 3",
    3: "Click this Checkbox if You Filed an Application - 4",
    4: "Click this Checkbox if You Filed an Application - 5",
}

OTHER_RESULT_FIELDS: dict[int, str] = {
    0: "Click this checkbox to tell us about other job result",
    1: "Click the Other Checkbox to tell us about a different job result - 2",
    2: "Click the Other Checkbox to tell us about a different job result - 3",
    3: "Click the Other Checkbox to tell us about a different job result - 4",
    4: "Click the Other Checkbox to tell us about a different job result - 5",
}

# Master collection for validation
ALL_FIELD_DICTS: list[dict[int, str]] = [
    ACTIVITY_DATE_FIELDS,
    WORK_SEARCH_FIELDS,
    JOB_TYPE_FIELDS,
    ORGANIZATION_NAME_FIELDS,
    ADDRESS_FIELDS,
    LOCATION_FIELDS,
    AREA_CODE_FIELDS,
    PHONE_MIDDLE_FIELDS,
    PHONE_LAST_FIELDS,
    EMAIL_CHECKBOX_FIELDS,
    MAIL_CHECKBOX_FIELDS,
    FAX_CHECKBOX_FIELDS,
    PERSON_CONTACTED_FIELDS,
    HIRED_CHECKBOX_FIELDS,
    NOT_HIRED_CHECKBOX_FIELDS,
    APPLICATION_FILED_FIELDS,
    OTHER_RESULT_FIELDS,
]


def get_all_expected_field_names() -> set[str]:
    """Return every field name that fill_activities may reference."""
    names: set[str] = set(HEADER_FIELDS.values())
    for d in ALL_FIELD_DICTS:
        names.update(d.values())
    return names


class FieldValidationError(Exception):
    """Raised when expected PDF form fields are missing from the template."""


def validate_pdf_fields(pdf_path: str) -> list[str]:
    """Check that all expected field names exist in the PDF template.

    Returns a list of missing field names (empty if all present).
    Raises FieldValidationError if any fields are missing.
    """
    reader = PdfReader(pdf_path)
    pdf_fields: set[str] = set()
    for page in reader.pages:
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot_obj = annot.get_object()
                field_name = annot_obj.get("/T")
                if field_name:
                    pdf_fields.add(str(field_name))

    expected = get_all_expected_field_names()
    missing = sorted(expected - pdf_fields)
    if missing:
        raise FieldValidationError(
            f"{len(missing)} expected field(s) not found in PDF template: "
            + ", ".join(missing[:10])
            + (" ..." if len(missing) > 10 else "")
        )
    return missing


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def load_env():
    """Load variables from .env file."""
    env_path = Path(__file__).resolve().parents[3] / ".env"
    load_dotenv(env_path)


def fill_activities(field_mapping, activities, start_idx=0):
    """Fill activity fields for up to 5 activities starting from start_idx."""

    for i, activity_idx in enumerate(range(start_idx, min(start_idx + 5, len(activities)))):
        activity = activities[activity_idx]

        date_str = activity['Date of Activity']
        if ' ' in date_str:
            date_str = date_str.split()[0]
        activity_date = datetime.strptime(date_str, '%Y-%m-%d')

        # Date of Activity
        field_mapping[ACTIVITY_DATE_FIELDS[i]] = activity_date.strftime('%m/%d/%Y')

        # Work Search Activity
        field_mapping[WORK_SEARCH_FIELDS[i]] = activity['Work Search Activity']

        # Type of Job
        field_mapping[JOB_TYPE_FIELDS[i]] = activity['Type of Job']

        # Company Name
        field_mapping[ORGANIZATION_NAME_FIELDS[i]] = activity['Company Name']

        # Address
        if activity['Address']:
            field_mapping[ADDRESS_FIELDS[i]] = activity['Address']

        # City, State, Zip Code
        if activity['City'] or activity['State'] or activity['Zip Code']:
            location = f"{activity['City']}, {activity['State']} {activity['Zip Code']}".strip(', ')
            field_mapping[LOCATION_FIELDS[i]] = location

        # Phone Number (split into area code, middle 3, last 4)
        if activity['Phone']:
            phone = activity['Phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            if len(phone) >= 10:
                field_mapping[AREA_CODE_FIELDS[i]] = phone[:3]
                field_mapping[PHONE_MIDDLE_FIELDS[i]] = phone[3:6]
                field_mapping[PHONE_LAST_FIELDS[i]] = phone[6:10]

        # Contact method checkboxes
        contact_method = activity['Contact Method'].lower()

        if 'email' in contact_method or 'online' in contact_method:
            field_mapping[EMAIL_CHECKBOX_FIELDS[i]] = '/Yes'

        if 'mail' in contact_method:
            field_mapping[MAIL_CHECKBOX_FIELDS[i]] = '/Yes'

        if 'fax' in contact_method:
            field_mapping[FAX_CHECKBOX_FIELDS[i]] = '/Yes'

        # Person Contacted
        if activity['Person Contacted']:
            field_mapping[PERSON_CONTACTED_FIELDS[i]] = activity['Person Contacted']

        # Results checkboxes
        results = activity['Results'].lower()

        if 'hired' in results and 'not hiring' not in results:
            field_mapping[HIRED_CHECKBOX_FIELDS[i]] = '/Yes'

        if 'not hiring' in results:
            field_mapping[NOT_HIRED_CHECKBOX_FIELDS[i]] = '/Yes'

        if 'application filed' in results:
            field_mapping[APPLICATION_FILED_FIELDS[i]] = '/Yes'

        # Other checkbox (for search activities and other results)
        notes = activity.get('Notes', '') or ''
        if 'searched online' in activity['Work Search Activity'].lower() or len(notes) > 0:
            field_mapping[OTHER_RESULT_FIELDS[i]] = '/Yes'


def fill_twc_pdf(csv_file, template_pdf, output_pdf):
    """Fill out a TWC Work Search Activity Log PDF from a CSV file."""

    # Read CSV data
    activities = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip empty rows (no date)
            if row.get('Date of Activity', '').strip():
                activities.append(row)

    if not activities:
        print("No activities found in CSV file")
        return

    # Get week info from first row
    week_start = datetime.strptime(activities[0]['Week Starting'], '%Y-%m-%d')
    week_end = datetime.strptime(activities[0]['Week Ending'], '%Y-%m-%d')
    required_searches = activities[0]['Required Searches']

    # Create PDFs for all activities (5 per page)
    num_pages = (len(activities) + 4) // 5  # Round up

    for page_num in range(num_pages):
        start_idx = page_num * 5
        end_idx = min(start_idx + 5, len(activities))

        # Determine output filename
        if num_pages == 1:
            current_output = output_pdf
        else:
            # Add part1, part2, etc.
            base_name = output_pdf.replace('.pdf', '')
            current_output = f"{base_name}-part{page_num + 1}.pdf"

        # Read the PDF template
        reader = PdfReader(template_pdf)
        writer = PdfWriter()

        # Copy pages from reader to writer
        for page in reader.pages:
            writer.add_page(page)

        # Fill in the header fields
        field_mapping = {
            HEADER_FIELDS["claimant_name"]: os.environ.get('TWC_CLAIMANT_NAME', ''),
            HEADER_FIELDS["week_of"]: week_start.strftime('%m/%d/%Y'),
            HEADER_FIELDS["end_date"]: week_end.strftime('%m/%d/%Y'),
            HEADER_FIELDS["ssn_first3"]: os.environ.get('TWC_SSN_FIRST3', ''),
            HEADER_FIELDS["ssn_mid2"]: os.environ.get('TWC_SSN_MID2', ''),
            HEADER_FIELDS["ssn_last4"]: os.environ.get('TWC_SSN_LAST4', ''),
            HEADER_FIELDS["required_searches"]: str(required_searches),
        }

        # Fill activities for this page
        fill_activities(field_mapping, activities, start_idx)

        # Clear existing form field values to prevent double-print
        page = writer.pages[0]
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot_obj = annot.get_object()
                if annot_obj.get("/FT") == "/Tx":  # Text fields
                    annot_obj.update({"/V": TextStringObject("")})

        # Update form fields
        writer.update_page_form_field_values(
            page,
            field_mapping
        )

        # Write the filled PDF
        with open(current_output, 'wb') as output_file:
            writer.write(output_file)

        print(f"Filled PDF created: {current_output} (activities {start_idx+1}-{end_idx})")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 fill_twc_pdf.py <csv_file> [output_pdf]")
        sys.exit(1)

    load_env()
    csv_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        output_pdf = csv_file.replace('.csv', '-filled.pdf')

    template_pdf = os.environ.get(
        'TWC_TEMPLATE_PDF',
        str(Path(__file__).parent / 'work-search-log-blank.pdf'),
    )

    fill_twc_pdf(csv_file, template_pdf, output_pdf)
