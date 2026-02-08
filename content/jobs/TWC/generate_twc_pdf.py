#!/usr/bin/env python3
"""
Generate TWC Work Search Activity Log PDFs from CSV files.
Matches the EXACT format of the official TWC form - landscape orientation.
"""

import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def draw_checkbox(c, x, y, checked=False, size=10):
    """Draw a checkbox at the given position."""
    c.rect(x, y, size, size, stroke=1, fill=0)
    if checked:
        # Draw an X
        c.line(x, y, x + size, y + size)
        c.line(x + size, y, x, y + size)


def generate_twc_pdf(csv_file, output_pdf):
    """Generate a TWC Work Search Activity Log PDF from a CSV file."""

    # Read CSV data
    activities = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            activities.append(row)

    if not activities:
        print("No activities found in CSV file")
        return

    # Get week info from first row
    week_start = datetime.strptime(activities[0]['Week Starting'], '%Y-%m-%d')
    week_end = datetime.strptime(activities[0]['Week Ending'], '%Y-%m-%d')
    required_searches = activities[0]['Required Searches']

    # Create PDF in LANDSCAPE orientation
    c = canvas.Canvas(output_pdf, pagesize=landscape(letter))
    width, height = landscape(letter)  # width=11", height=8.5"

    # Title
    c.setFont("Helvetica-Bold", 14)
    title = "The Texas Workforce Commission Work Search Activity Log"
    c.drawCentredString(width / 2, height - 0.5 * inch, title)

    # TWC use only box (top right corner)
    box_width = 0.6 * inch
    box_height = 0.4 * inch
    box_x = width - box_width - 0.25 * inch
    box_y = height - 0.9 * inch

    c.setLineWidth(1)
    c.rect(box_x, box_y, box_width, box_height)

    c.setFont("Helvetica", 8)
    c.drawCentredString(box_x + box_width/2, box_y + 0.28 * inch, "TWC")
    c.drawCentredString(box_x + box_width/2, box_y + 0.18 * inch, "use")
    c.drawCentredString(box_x + box_width/2, box_y + 0.08 * inch, "only")

    # Header section - left side
    y = height - 1.0 * inch
    left_margin = 0.4 * inch

    # Name field with yellow highlight
    c.setFont("Helvetica-Bold", 10)
    name_label_x = left_margin
    c.drawString(name_label_x, y, "Name:")

    name_x = name_label_x + 0.45 * inch
    name_width = 3.8 * inch
    c.setFillColorRGB(1, 0.9, 0.6)  # Yellow highlight
    c.rect(name_x, y - 0.12 * inch, name_width, 0.18 * inch, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)  # Reset to black

    c.setFont("Helvetica", 10)
    c.drawString(name_x + 0.05 * inch, y, "Matthew Druhl")

    # Week of - right side
    week_label_x = name_x + name_width + 0.5 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(week_label_x, y, "Week of:")

    c.setFont("Helvetica", 10)
    week_value_x = week_label_x + 0.6 * inch
    c.drawString(week_value_x, y, f"{week_start.strftime('%m/%d/%Y')}")

    to_x = week_value_x + 0.85 * inch
    c.drawString(to_x, y, "to")

    week_end_x = to_x + 0.2 * inch
    c.drawString(week_end_x, y, f"{week_end.strftime('%m/%d/%Y')}")

    # Social Security # - left side
    y -= 0.25 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin, y, "Social Security #:")

    ssn_x = left_margin + 1.1 * inch
    c.setFont("Helvetica", 10)
    c.drawString(ssn_x, y, "483")
    c.drawString(ssn_x + 0.25 * inch, y, "-")
    c.drawString(ssn_x + 0.35 * inch, y, "08")
    c.drawString(ssn_x + 0.55 * inch, y, "-")
    c.drawString(ssn_x + 0.65 * inch, y, "5631")

    # Number of Required Searches - right side
    c.setFont("Helvetica-Bold", 10)
    required_label_x = week_label_x
    c.drawString(required_label_x, y, "Number of Required Searches:")

    c.setFont("Helvetica", 10)
    required_value_x = required_label_x + 2.1 * inch
    c.drawString(required_value_x, y, str(required_searches))

    # Instructions
    y -= 0.25 * inch
    c.setFont("Helvetica", 8)
    inst1 = "If you are still unemployed after eight weeks of benefits, you should reduce your salary requirement and look at more job openings. Make as many copies"
    c.drawString(left_margin, y, inst1)

    y -= 0.12 * inch
    c.drawString(left_margin, y, "of this as you need, or print copies at ")

    link_x = left_margin + 2.0 * inch
    c.setFillColorRGB(0, 0, 1)  # Blue for link
    c.drawString(link_x, y, "www.twc.texas.gov/worksearchlog")
    c.setFillColorRGB(0, 0, 0)  # Reset to black

    period_x = link_x + 2.1 * inch
    c.drawString(period_x, y, ".")

    # Table starts here
    y -= 0.25 * inch
    table_top = y

    # Column definitions
    col1_x = left_margin
    col1_width = 2.3 * inch

    col2_x = col1_x + col1_width
    col2_width = 3.2 * inch

    col3_x = col2_x + col2_width
    col3_width = 2.2 * inch

    col4_x = col3_x + col3_width
    col4_width = 1.8 * inch

    table_width = col1_width + col2_width + col3_width + col4_width

    # Draw table header
    header_height = 0.4 * inch
    c.setLineWidth(1)

    # Header boxes
    c.rect(col1_x, table_top - header_height, col1_width, header_height)
    c.rect(col2_x, table_top - header_height, col2_width, header_height)
    c.rect(col3_x, table_top - header_height, col3_width, header_height)
    c.rect(col4_x, table_top - header_height, col4_width, header_height)

    # Header text
    c.setFont("Helvetica-Bold", 8)

    # Column 1 header
    c.drawString(col1_x + 0.05 * inch, table_top - 0.15 * inch, "Date, Description of Work Search")
    c.drawString(col1_x + 0.05 * inch, table_top - 0.27 * inch, "(Ex: Applied for job, submitted resume,")

    # Column 2 header
    c.drawString(col2_x + 0.05 * inch, table_top - 0.15 * inch, "Name, Location and Telephone Number of")
    c.drawString(col2_x + 0.05 * inch, table_top - 0.27 * inch, "Employer/Service/Agency")

    # Column 3 header
    c.drawString(col3_x + 0.05 * inch, table_top - 0.15 * inch, "Contact Information")
    c.drawString(col3_x + 0.05 * inch, table_top - 0.27 * inch, "Complete all that apply.")

    # Column 4 header
    c.drawString(col4_x + 0.05 * inch, table_top - 0.2 * inch, "Results")

    # Draw 5 activity rows
    y = table_top - header_height
    row_height = 1.05 * inch

    for i in range(5):
        if i < len(activities):
            activity = activities[i]
            draw_activity_row(c, y, activity, col1_x, col2_x, col3_x, col4_x,
                            col1_width, col2_width, col3_width, col4_width, row_height)
        else:
            draw_empty_row(c, y, col1_x, col2_x, col3_x, col4_x,
                          col1_width, col2_width, col3_width, col4_width, row_height)

        y -= row_height

    # ONE vertical outcome block on right side (spans header + all activity rows)
    right_edge_x = width - 0.25 * inch
    vertical_block_width = 0.55 * inch

    # Start at the same Y position as the table header (same as table_top)
    vertical_block_top = table_top
    vertical_block_height = header_height + (row_height * 5)  # Spans header + all 5 rows

    # Draw ONE large block spanning from header to bottom of last row
    c.setLineWidth(1)
    c.rect(right_edge_x - vertical_block_width, vertical_block_top - vertical_block_height,
           vertical_block_width, vertical_block_height)

    # Add vertical text labels (rotated 270 degrees, reading from top to bottom)
    c.setFont("Helvetica", 8)

    # Position text strings vertically down the block
    text_x = right_edge_x - vertical_block_width/2

    # Verifier ID at top
    c.saveState()
    c.translate(text_x, vertical_block_top - 0.7 * inch)
    c.rotate(270)
    c.drawString(0, 0, "Verifier ID")
    c.restoreState()

    # Outcomes:
    c.saveState()
    c.translate(text_x, vertical_block_top - 1.7 * inch)
    c.rotate(270)
    c.drawString(0, 0, "Outcomes:")
    c.restoreState()

    # A
    c.saveState()
    c.translate(text_x, vertical_block_top - 2.5 * inch)
    c.rotate(270)
    c.drawString(0, 0, "A")
    c.restoreState()

    # U#
    c.saveState()
    c.translate(text_x, vertical_block_top - 3.3 * inch)
    c.rotate(270)
    c.drawString(0, 0, "U#")
    c.restoreState()

    # U/O
    c.saveState()
    c.translate(text_x, vertical_block_top - 4.1 * inch)
    c.rotate(270)
    c.drawString(0, 0, "U/O")
    c.restoreState()

    # RD
    c.saveState()
    c.translate(text_x, vertical_block_top - 4.7 * inch)
    c.rotate(270)
    c.drawString(0, 0, "RD")
    c.restoreState()

    # WSV BWE
    c.saveState()
    c.translate(text_x, vertical_block_top - 5.15 * inch)
    c.rotate(270)
    c.drawString(0, 0, "WSV BWE")
    c.restoreState()

    # Bottom section - lower positioning
    y = 0.75 * inch
    c.setFont("Helvetica", 7)
    c.drawString(left_margin, y, "An individual may receive and review information that TWC collects regarding that individual by emailing ")

    email_x = left_margin + 4.6 * inch
    c.setFillColorRGB(0, 0, 1)
    c.drawString(email_x, y, "open.records@twc.texas.gov")
    c.setFillColorRGB(0, 0, 0)

    or_x = email_x + 1.55 * inch
    c.drawString(or_x, y, " or writing to")

    y -= 0.12 * inch
    c.setFont("Helvetica", 7)
    c.drawString(left_margin, y, "TWC Open Records Unit, 101 E. 15th St. Room 266, Austin TX 78778-0001. For more information, see ")

    link_x = left_margin + 4.85 * inch
    c.setFillColorRGB(0, 0, 1)
    c.drawString(link_x, y, "https://twc.texas.gov/services/open-records")
    c.setFillColorRGB(0, 0, 0)

    period_x = link_x + 2.4 * inch
    c.drawString(period_x, y, ".")

    y -= 0.18 * inch
    c.setFont("Helvetica-Bold", 7)
    c.drawString(left_margin, y, "Keep this form for your records.")

    c.setFont("Helvetica", 7)
    submit_x = left_margin + 1.65 * inch
    c.drawString(submit_x, y, "Submit a copy to TWC only if requested using our online UI Submission Portal at ")

    portal_x = submit_x + 4.2 * inch
    c.setFillColorRGB(0, 0, 1)
    c.drawString(portal_x, y, "https://twc.texas.gov/uidocs")
    c.setFillColorRGB(0, 0, 0)

    y -= 0.12 * inch
    c.setFont("Helvetica", 7)
    c.drawString(left_margin, y, "or the address or fax number we gave you.")

    # Form ID
    y = 0.25 * inch
    c.setFont("Helvetica", 7)
    c.drawString(left_margin, y, "BN900E (10-12-23)")

    c.save()
    print(f"Generated: {output_pdf}")


def draw_activity_row(c, y_top, activity, col1_x, col2_x, col3_x, col4_x,
                     col1_width, col2_width, col3_width, col4_width, row_height):
    """Draw a single activity row."""

    # Parse activity date
    date_str = activity['Date of Activity']
    if ' ' in date_str:  # Remove time if present
        date_str = date_str.split()[0]
    activity_date = datetime.strptime(date_str, '%Y-%m-%d')

    # Draw borders
    c.setLineWidth(1)
    c.rect(col1_x, y_top - row_height, col1_width, row_height)
    c.rect(col2_x, y_top - row_height, col2_width, row_height)
    c.rect(col3_x, y_top - row_height, col3_width, row_height)
    c.rect(col4_x, y_top - row_height, col4_width, row_height)

    # Column 1: Date, Work Search Activity, Type of Job
    y = y_top - 0.15 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col1_x + 0.05 * inch, y, "Date of Activity")

    y -= 0.12 * inch
    c.setFont("Helvetica", 9)
    c.drawString(col1_x + 0.05 * inch, y, activity_date.strftime('%m/%d/%Y'))

    y -= 0.2 * inch
    # Yellow highlight for Work Search Activity label
    c.setFillColorRGB(1, 0.9, 0.6)
    c.rect(col1_x + 0.05 * inch, y - 0.05 * inch, 1.5 * inch, 0.13 * inch, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica", 7)
    c.drawString(col1_x + 0.05 * inch, y, "Work Search Activity")

    y -= 0.12 * inch
    c.setFont("Helvetica", 9)
    c.drawString(col1_x + 0.05 * inch, y, activity['Work Search Activity'])

    y -= 0.2 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col1_x + 0.05 * inch, y, "Type of Job")

    y -= 0.12 * inch
    c.setFont("Helvetica", 8)
    job_type = activity['Type of Job']
    if len(job_type) > 28:
        c.drawString(col1_x + 0.05 * inch, y, job_type[:28])
        y -= 0.1 * inch
        c.drawString(col1_x + 0.05 * inch, y, job_type[28:])
    else:
        c.drawString(col1_x + 0.05 * inch, y, job_type)

    # Column 2: Name, Address, City/State/Zip, Phone
    y = y_top - 0.15 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col2_x + 0.05 * inch, y, "Name")

    y -= 0.12 * inch
    c.setFont("Helvetica", 9)
    c.drawString(col2_x + 0.05 * inch, y, activity['Company Name'])

    y -= 0.17 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col2_x + 0.05 * inch, y, "Address")

    if activity['Address']:
        y -= 0.12 * inch
        c.setFont("Helvetica", 9)
        c.drawString(col2_x + 0.05 * inch, y, activity['Address'])

    y -= 0.17 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col2_x + 0.05 * inch, y, "City, State, Zip Code")

    if activity['City'] or activity['State'] or activity['Zip Code']:
        y -= 0.12 * inch
        c.setFont("Helvetica", 9)
        location_parts = []
        if activity['City']:
            location_parts.append(activity['City'])
        if activity['State']:
            location_parts.append(activity['State'])
        if activity['Zip Code']:
            location_parts.append(activity['Zip Code'])
        location = ', '.join(location_parts) if len(location_parts) > 1 else ''.join(location_parts)
        c.drawString(col2_x + 0.05 * inch, y, location)

    y -= 0.17 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col2_x + 0.05 * inch, y, "Area Code + Phone #")

    if activity['Phone']:
        y -= 0.12 * inch
        c.setFont("Helvetica", 9)
        c.drawString(col2_x + 0.05 * inch, y, activity['Phone'])

    # Column 3: Contact Information checkboxes
    y = y_top - 0.15 * inch
    c.setFont("Helvetica", 7)
    checkbox_x = col3_x + 0.05 * inch

    # Person Contacted
    person_contacted = bool(activity['Person Contacted'].strip())
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=person_contacted, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Person Contacted")

    y -= 0.17 * inch
    # By Mail
    by_mail = 'mail' in activity['Contact Method'].lower()
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=by_mail, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "By Mail (Enter Address at left)")

    y -= 0.17 * inch
    # Email
    email_checked = 'email' in activity['Contact Method'].lower() or 'online' in activity['Contact Method'].lower()
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=email_checked, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Email")

    y -= 0.17 * inch
    # Fax
    fax_checked = 'fax' in activity['Contact Method'].lower()
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=fax_checked, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Fax #")

    # Column 4: Results checkboxes
    y = y_top - 0.15 * inch
    c.setFont("Helvetica", 7)
    checkbox_x = col4_x + 0.05 * inch

    # Hired
    hired = 'hired' in activity['Results'].lower() and 'not hiring' not in activity['Results'].lower()
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=hired, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Hired")

    # Not hiring
    not_hiring_x = checkbox_x + 0.8 * inch
    not_hiring = 'not hiring' in activity['Results'].lower()
    draw_checkbox(c, not_hiring_x, y - 0.07 * inch, checked=not_hiring, size=8)
    c.drawString(not_hiring_x + 0.12 * inch, y, "Not hiring")

    y -= 0.17 * inch
    # Start date
    start_date = 'start date' in activity['Results'].lower()
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=start_date, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Start date")

    y -= 0.17 * inch
    # Application filed
    app_filed = 'application filed' in activity['Results'].lower()
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=app_filed, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Application filed")

    y -= 0.17 * inch
    # Other
    other_result = not (hired or not_hiring or start_date or app_filed) or len(activity['Notes']) > 0
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, checked=other_result, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Other")


def draw_empty_row(c, y_top, col1_x, col2_x, col3_x, col4_x,
                  col1_width, col2_width, col3_width, col4_width, row_height):
    """Draw an empty activity row."""

    # Draw borders
    c.setLineWidth(1)
    c.rect(col1_x, y_top - row_height, col1_width, row_height)
    c.rect(col2_x, y_top - row_height, col2_width, row_height)
    c.rect(col3_x, y_top - row_height, col3_width, row_height)
    c.rect(col4_x, y_top - row_height, col4_width, row_height)

    # Column 1 labels
    y = y_top - 0.15 * inch
    c.setFont("Helvetica", 7)
    c.drawString(col1_x + 0.05 * inch, y, "Date of Activity")

    y -= 0.32 * inch
    c.drawString(col1_x + 0.05 * inch, y, "Work Search Activity")

    y -= 0.32 * inch
    c.drawString(col1_x + 0.05 * inch, y, "Type of Job")

    # Column 2 labels
    y = y_top - 0.15 * inch
    c.drawString(col2_x + 0.05 * inch, y, "Name")

    y -= 0.17 * inch
    c.drawString(col2_x + 0.05 * inch, y, "Address")

    y -= 0.17 * inch
    c.drawString(col2_x + 0.05 * inch, y, "City, State, Zip Code")

    y -= 0.17 * inch
    c.drawString(col2_x + 0.05 * inch, y, "Area Code + Phone #")

    # Column 3 checkboxes
    y = y_top - 0.15 * inch
    checkbox_x = col3_x + 0.05 * inch

    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Person Contacted")

    y -= 0.17 * inch
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "By Mail (Enter Address at left)")

    y -= 0.17 * inch
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Email")

    y -= 0.17 * inch
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Fax #")

    # Column 4 checkboxes
    y = y_top - 0.15 * inch
    checkbox_x = col4_x + 0.05 * inch

    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Hired")

    not_hiring_x = checkbox_x + 0.8 * inch
    draw_checkbox(c, not_hiring_x, y - 0.07 * inch, size=8)
    c.drawString(not_hiring_x + 0.12 * inch, y, "Not hiring")

    y -= 0.17 * inch
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Start date")

    y -= 0.17 * inch
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Application filed")

    y -= 0.17 * inch
    draw_checkbox(c, checkbox_x, y - 0.07 * inch, size=8)
    c.drawString(checkbox_x + 0.12 * inch, y, "Other")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 generate_twc_pdf.py <csv_file> [output_pdf]")
        sys.exit(1)

    csv_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        # Generate output filename from input
        output_pdf = csv_file.replace('.csv', '.pdf')

    generate_twc_pdf(csv_file, output_pdf)
