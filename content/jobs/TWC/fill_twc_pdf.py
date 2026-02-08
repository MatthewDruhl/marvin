#!/usr/bin/env python3
"""
Fill out TWC Work Search Activity Log PDF forms from CSV files.
Uses the original fillable PDF form.
Creates multiple pages if more than 5 activities.
"""

import csv
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter


def fill_activities(field_mapping, activities, start_idx=0):
    """Fill activity fields for up to 5 activities starting from start_idx."""

    for i, activity_idx in enumerate(range(start_idx, min(start_idx + 5, len(activities)))):
        activity = activities[activity_idx]

        date_str = activity['Date of Activity']
        if ' ' in date_str:
            date_str = date_str.split()[0]
        activity_date = datetime.strptime(date_str, '%Y-%m-%d')

        # Activity numbering: first activity has no number, rest have -2, -3, -4, -5
        activity_num = '' if i == 0 else f' - {i+1}'

        # Date of Activity
        date_field = f'Enter Date of Job Search Activity{activity_num}' if i > 0 else 'Enter Date of Job Search Activity'
        field_mapping[date_field] = activity_date.strftime('%m/%d/%Y')

        # Work Search Activity
        work_field = f'Enter Work Search Activity{activity_num}' if i > 0 else 'Enter Work Search Activity'
        field_mapping[work_field] = activity['Work Search Activity']

        # Type of Job
        if i == 0:
            field_mapping['Enter Job Type'] = activity['Type of Job']
        elif i == 1:
            field_mapping['Enter Job Type  - 2'] = activity['Type of Job']  # Note: double space
        else:
            field_mapping[f'Enter Job Type - {i+1}'] = activity['Type of Job']

        # Company Name
        if i == 0:
            field_mapping['Enter Name of Organization - 1'] = activity['Company Name']
        elif i == 1:
            field_mapping['Enter Name of Organization  - 2'] = activity['Company Name']  # Note: double space
        elif i == 2:
            field_mapping['Enter Name of Organization - 3'] = activity['Company Name']
        elif i == 3:
            field_mapping['Enter Name of Organization  4'] = activity['Company Name']  # Note: no dash
        else:
            field_mapping['Enter Name of Organization - 5'] = activity['Company Name']

        # Address
        if activity['Address']:
            if i == 0:
                field_mapping['Enter Street Address - Organization 1'] = activity['Address']
            elif i == 1:
                field_mapping['Enter Street Address - Organization - 2'] = activity['Address']
            elif i == 2:
                field_mapping['Enter Street Address - Organization - 3'] = activity['Address']
            elif i == 3:
                field_mapping['Enter Street Address - Organization 4'] = activity['Address']
            else:
                field_mapping['Enter Street Address - Organization 5'] = activity['Address']

        # City, State, Zip Code
        if activity['City'] or activity['State'] or activity['Zip Code']:
            location = f"{activity['City']}, {activity['State']} {activity['Zip Code']}".strip(', ')
            field_mapping[f'Enter City, State, Zip Code - Organization {i+1}'] = location

        # Phone Number (split into area code, middle 3, last 4)
        if activity['Phone']:
            # Assuming format like (XXX) XXX-XXXX or similar
            phone = activity['Phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            if len(phone) >= 10:
                area_code = phone[:3]
                middle_3 = phone[3:6]
                last_4 = phone[6:10]

                area_field = f'Enter Area Code - Organization {i+1}'
                middle_field = f'Enter Middle 3 Phone Digits{activity_num}' if i > 0 else 'Enter Middle 3 Phone Digits'
                last_field = f'Enter Last 4 Phone Digits{activity_num}' if i > 0 else 'Enter Last 4 Phone Digits'

                field_mapping[area_field] = area_code
                field_mapping[middle_field] = middle_3
                field_mapping[last_field] = last_4

        # Contact method checkboxes
        contact_method = activity['Contact Method'].lower()

        # Email checkbox
        if 'email' in contact_method or 'online' in contact_method:
            email_checkbox = f'Click this checkbox if you contacted organization by email{activity_num}' if i > 0 else 'Click this checkbox if you contacted organization by email'
            field_mapping[email_checkbox] = '/Yes'

        # Mail checkbox
        if 'mail' in contact_method:
            if i == 0:
                field_mapping['Click this checkbox if you contacted organization by mail - 1'] = '/Yes'
            elif i == 1:
                field_mapping['Click this checkbox if you contacted organization by mail - 2'] = '/Yes'
            elif i == 2:
                field_mapping['Click this checkbox if you contacted organization by mail - 3'] = '/Yes'
            elif i == 3:
                field_mapping['Click this checkbox if you contacted organization by mail  - 4'] = '/Yes'  # Note: double space
            else:
                field_mapping['Click this checkbox if you contacted organization by mail - 5'] = '/Yes'

        # Fax checkbox
        if 'fax' in contact_method:
            fax_suffix = f' -{i+1}' if i > 0 else ''
            field_mapping[f'Click this checkbox if you contacted organization by fax{fax_suffix}'] = '/Yes'

        # Person Contacted
        if activity['Person Contacted']:
            field_mapping[f'Enter Name of Person Contacted - Organization {i+1}'] = activity['Person Contacted']

        # Results checkboxes
        results = activity['Results'].lower()

        # Hired checkbox
        if 'hired' in results and 'not hiring' not in results:
            field_mapping[f'Click This Checkbox If You Were Hired - {i+1}'] = '/Yes'

        # Not hired checkbox
        if 'not hiring' in results:
            field_mapping[f'Click This Checkbox If Not Hired - {i+1}'] = '/Yes'

        # Application filed checkbox
        if 'application filed' in results:
            if i == 0:
                field_mapping['Click this Checkbox if You Filed an Application - 1'] = '/Yes'
            else:
                field_mapping[f'Click this Checkbox if You Filed an Application - {i+1}'] = '/Yes'

        # Other checkbox (for search activities and other results)
        notes = activity.get('Notes', '') or ''
        if 'searched online' in activity['Work Search Activity'].lower() or len(notes) > 0:
            if i == 0:
                field_mapping['Click this checkbox to tell us about other job result'] = '/Yes'
            else:
                field_mapping[f'Click the Other Checkbox to tell us about a different job result - {i+1}'] = '/Yes'


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
            'Enter Claimant Name': 'Matthew Druhl',
            'Enter Week Of': week_start.strftime('%m/%d/%Y'),
            'Enter End Date': week_end.strftime('%m/%d/%Y'),
            'Enter Social Security Number First 3 Digits': '483',
            'Enter Social Security Number Middle 2 Digits': '08',
            'Enter Last 4 Digits of Social Security Number': '5631',
            'Enter Number of Required Searches': str(required_searches),
        }

        # Fill activities for this page
        fill_activities(field_mapping, activities, start_idx)

        # Update form fields
        writer.update_page_form_field_values(
            writer.pages[0],
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

    csv_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        output_pdf = csv_file.replace('.csv', '-filled.pdf')

    template_pdf = '/Users/matthewdruhl/marvin/content/jobs/TWC/work-search-log-blank.pdf'

    fill_twc_pdf(csv_file, template_pdf, output_pdf)
