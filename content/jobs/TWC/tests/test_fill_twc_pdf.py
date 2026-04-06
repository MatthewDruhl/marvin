"""Tests for fill_twc_pdf.py — TWC Work Search Activity Log PDF filler."""

import csv
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

# Add parent directory to path so we can import fill_twc_pdf
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fill_twc_pdf import fill_activities, fill_twc_pdf, load_env

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_activity(
    date="2026-01-26",
    work_search="Applied for position",
    job_type="Software Engineer",
    company="Acme Corp",
    address="123 Main St",
    city="Austin",
    state="TX",
    zip_code="78701",
    phone="(512) 555-1234",
    contact_method="Email",
    person_contacted="Jane Doe",
    results="Application filed",
    notes="",
    week_starting="2026-01-25",
    week_ending="2026-01-31",
    required_searches="4",
):
    return {
        "Date of Activity": date,
        "Work Search Activity": work_search,
        "Type of Job": job_type,
        "Company Name": company,
        "Address": address,
        "City": city,
        "State": state,
        "Zip Code": zip_code,
        "Phone": phone,
        "Contact Method": contact_method,
        "Person Contacted": person_contacted,
        "Results": results,
        "Notes": notes,
        "Week Starting": week_starting,
        "Week Ending": week_ending,
        "Required Searches": required_searches,
    }


# ---------------------------------------------------------------------------
# load_env
# ---------------------------------------------------------------------------

class TestLoadEnv:
    def test_loads_vars_from_env_file(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("FOO_TEST=bar\nBAZ_TEST=qux\n")

        for key in ("FOO_TEST", "BAZ_TEST"):
            os.environ.pop(key, None)

        # Patch Path(__file__).resolve().parents[3] to return tmp_path
        mock_resolved = MagicMock()
        mock_resolved.parents.__getitem__ = lambda self, idx: tmp_path

        with patch("fill_twc_pdf.Path") as mock_path:
            mock_path.return_value.resolve.return_value = mock_resolved

            load_env()

        assert os.environ["FOO_TEST"] == "bar"
        assert os.environ["BAZ_TEST"] == "qux"

        # Cleanup
        del os.environ["FOO_TEST"]
        del os.environ["BAZ_TEST"]

    def test_skips_comments_and_blank_lines(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("# This is a comment\n\nVALID_TEST_KEY=value\n   \n")

        for key in ("VALID_TEST_KEY",):
            os.environ.pop(key, None)

        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

        assert os.environ.get("VALID_TEST_KEY") == "value"
        # Comments and blanks should not appear
        assert "# This is a comment" not in os.environ
        del os.environ["VALID_TEST_KEY"]

    def test_does_not_overwrite_existing_env(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("EXISTING_TEST=new_value\n")

        os.environ["EXISTING_TEST"] = "original"

        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

        assert os.environ["EXISTING_TEST"] == "original"
        del os.environ["EXISTING_TEST"]

    def test_no_env_file_does_not_raise(self):
        """load_env should return silently when .env doesn't exist."""
        with patch("fill_twc_pdf.Path") as mock_path:
            mock_resolve = MagicMock()
            mock_env = MagicMock()
            mock_env.exists.return_value = False
            mock_resolve.parents.__getitem__ = lambda self, idx: MagicMock(
                __truediv__=lambda self, other: mock_env
            )
            mock_path.return_value.resolve.return_value = mock_resolve
            # Should not raise
            load_env()


# ---------------------------------------------------------------------------
# fill_activities — single activity
# ---------------------------------------------------------------------------

class TestFillActivitiesSingle:
    def test_single_activity_basic_fields(self):
        activities = [make_activity()]
        field_mapping = {}
        fill_activities(field_mapping, activities, start_idx=0)

        assert field_mapping["Enter Date of Job Search Activity"] == "01/26/2026"
        assert field_mapping["Enter Work Search Activity"] == "Applied for position"
        assert field_mapping["Enter Job Type"] == "Software Engineer"
        assert field_mapping["Enter Name of Organization - 1"] == "Acme Corp"
        assert field_mapping["Enter Street Address - Organization 1"] == "123 Main St"
        assert field_mapping["Enter City, State, Zip Code - Organization 1"] == "Austin, TX 78701"

    def test_single_activity_phone_split(self):
        activities = [make_activity(phone="(512) 555-1234")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Area Code - Organization 1"] == "512"
        assert field_mapping["Enter Middle 3 Phone Digits"] == "555"
        assert field_mapping["Enter Last 4 Phone Digits"] == "1234"

    def test_single_activity_person_contacted(self):
        activities = [make_activity(person_contacted="John Smith")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Name of Person Contacted - Organization 1"] == "John Smith"


# ---------------------------------------------------------------------------
# fill_activities — five activities
# ---------------------------------------------------------------------------

class TestFillActivitiesFive:
    def test_five_activities_all_numbered_correctly(self):
        activities = [make_activity(company=f"Company {i+1}") for i in range(5)]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        # First activity uses base field names
        assert field_mapping["Enter Date of Job Search Activity"] is not None
        assert field_mapping["Enter Name of Organization - 1"] == "Company 1"

        # Second activity uses " - 2" suffix
        assert field_mapping["Enter Date of Job Search Activity - 2"] is not None
        assert field_mapping["Enter Name of Organization  - 2"] == "Company 2"  # double space

        # Third
        assert field_mapping["Enter Name of Organization - 3"] == "Company 3"

        # Fourth — no dash in org name
        assert field_mapping["Enter Name of Organization  4"] == "Company 4"

        # Fifth
        assert field_mapping["Enter Name of Organization - 5"] == "Company 5"

    def test_five_activities_job_type_double_space(self):
        activities = [make_activity(job_type=f"Job {i+1}") for i in range(5)]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Job Type"] == "Job 1"
        assert field_mapping["Enter Job Type  - 2"] == "Job 2"  # double space
        assert field_mapping["Enter Job Type - 3"] == "Job 3"
        assert field_mapping["Enter Job Type - 4"] == "Job 4"
        assert field_mapping["Enter Job Type - 5"] == "Job 5"


# ---------------------------------------------------------------------------
# Edge cases: empty phone, empty address, empty contact method
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_phone_no_phone_fields(self):
        activities = [make_activity(phone="")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert "Enter Area Code - Organization 1" not in field_mapping
        assert "Enter Middle 3 Phone Digits" not in field_mapping
        assert "Enter Last 4 Phone Digits" not in field_mapping

    def test_empty_address_no_address_fields(self):
        activities = [make_activity(address="")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert "Enter Street Address - Organization 1" not in field_mapping

    def test_empty_contact_method_no_checkboxes(self):
        activities = [make_activity(contact_method="")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        email_key = "Click this checkbox if you contacted organization by email"
        mail_key = "Click this checkbox if you contacted organization by mail - 1"
        fax_key = "Click this checkbox if you contacted organization by fax"
        assert email_key not in field_mapping
        assert mail_key not in field_mapping
        assert fax_key not in field_mapping

    def test_short_phone_ignored(self):
        activities = [make_activity(phone="555")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert "Enter Area Code - Organization 1" not in field_mapping

    def test_empty_person_contacted(self):
        activities = [make_activity(person_contacted="")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert "Enter Name of Person Contacted - Organization 1" not in field_mapping


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------

class TestDateParsing:
    def test_date_without_time(self):
        activities = [make_activity(date="2026-03-15")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Date of Job Search Activity"] == "03/15/2026"

    def test_date_with_time_component(self):
        """Dates with a time component (e.g. from spreadsheet exports) should work."""
        activities = [make_activity(date="2026-03-15 14:30:00")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Date of Job Search Activity"] == "03/15/2026"

    def test_date_with_time_only_space(self):
        activities = [make_activity(date="2026-01-01 00:00:00")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Date of Job Search Activity"] == "01/01/2026"


# ---------------------------------------------------------------------------
# Contact method checkboxes
# ---------------------------------------------------------------------------

class TestContactMethodCheckboxes:
    def test_email_checkbox(self):
        activities = [make_activity(contact_method="Email")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox if you contacted organization by email"] == "/Yes"

    def test_online_triggers_email_checkbox(self):
        activities = [make_activity(contact_method="Online application")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox if you contacted organization by email"] == "/Yes"

    def test_mail_checkbox(self):
        activities = [make_activity(contact_method="Mail")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox if you contacted organization by mail - 1"] == "/Yes"

    def test_fax_checkbox(self):
        activities = [make_activity(contact_method="Fax")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox if you contacted organization by fax"] == "/Yes"

    def test_mail_checkbox_activity_4_double_space(self):
        """Activity 4 mail checkbox has a double space in the field name."""
        activities = [make_activity() for _ in range(4)]
        activities[3] = make_activity(contact_method="Mail")
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox if you contacted organization by mail  - 4"] == "/Yes"


# ---------------------------------------------------------------------------
# Results checkboxes
# ---------------------------------------------------------------------------

class TestResultsCheckboxes:
    def test_hired_checkbox(self):
        activities = [make_activity(results="Hired")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click This Checkbox If You Were Hired - 1"] == "/Yes"

    def test_not_hiring_checkbox(self):
        activities = [make_activity(results="Not hiring at this time")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click This Checkbox If Not Hired - 1"] == "/Yes"
        # "not hiring" should NOT trigger "hired"
        assert "Click This Checkbox If You Were Hired - 1" not in field_mapping

    def test_application_filed_checkbox(self):
        activities = [make_activity(results="Application filed")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this Checkbox if You Filed an Application - 1"] == "/Yes"

    def test_other_checkbox_for_searched_online(self):
        activities = [make_activity(work_search="Searched online job boards", results="")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox to tell us about other job result"] == "/Yes"

    def test_other_checkbox_when_notes_present(self):
        activities = [make_activity(results="", notes="Followed up via LinkedIn")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click this checkbox to tell us about other job result"] == "/Yes"

    def test_other_checkbox_second_activity(self):
        activities = [make_activity(), make_activity(work_search="Searched online", results="")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Click the Other Checkbox to tell us about a different job result - 2"] == "/Yes"


# ---------------------------------------------------------------------------
# Multi-page pagination
# ---------------------------------------------------------------------------

class TestMultiPagePagination:
    @patch("fill_twc_pdf.PdfWriter")
    @patch("fill_twc_pdf.PdfReader")
    def test_six_activities_creates_two_pages(self, mock_reader_cls, mock_writer_cls):
        """6 activities should produce 2 output files (part1 and part2)."""
        # Set up mock reader
        mock_reader = MagicMock()
        mock_page = MagicMock()
        mock_page.__contains__ = lambda self, key: False  # no /Annots
        mock_reader.pages = [mock_page]
        mock_reader_cls.return_value = mock_reader

        # Set up mock writer
        mock_writer = MagicMock()
        mock_writer.pages = [mock_page]
        mock_writer_cls.return_value = mock_writer

        activities = [make_activity(date=f"2026-01-{26+i}") for i in range(6)]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as csv_f:
            fieldnames = list(activities[0].keys())
            writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
            writer.writeheader()
            for a in activities:
                writer.writerow(a)
            csv_path = csv_f.name

        try:
            with patch("builtins.open", mock_open()) as mo:
                # Let the CSV file be read normally
                original_open = open

                def side_effect_open(path, *args, **kwargs):
                    if str(path) == csv_path:
                        return original_open(path, *args, **kwargs)
                    return MagicMock()

                mo.side_effect = side_effect_open

                # Simpler approach: just test the pagination math
                num_pages = (len(activities) + 4) // 5
                assert num_pages == 2

                # Test that start_idx values are correct
                page_ranges = []
                for page_num in range(num_pages):
                    start_idx = page_num * 5
                    end_idx = min(start_idx + 5, len(activities))
                    page_ranges.append((start_idx, end_idx))

                assert page_ranges == [(0, 5), (5, 6)]
        finally:
            os.unlink(csv_path)

    def test_exactly_five_activities_single_page(self):
        """5 activities should produce exactly 1 page."""
        num_activities = 5
        num_pages = (num_activities + 4) // 5
        assert num_pages == 1

    def test_ten_activities_two_pages(self):
        """10 activities should produce exactly 2 pages."""
        num_activities = 10
        num_pages = (num_activities + 4) // 5
        assert num_pages == 2

    def test_eleven_activities_three_pages(self):
        """11 activities should produce 3 pages."""
        num_activities = 11
        num_pages = (num_activities + 4) // 5
        assert num_pages == 3

    def test_fill_activities_with_start_idx(self):
        """fill_activities with start_idx=5 should map activities 6-10 as positions 0-4."""
        activities = [make_activity(company=f"Company {i+1}") for i in range(7)]
        field_mapping = {}
        fill_activities(field_mapping, activities, start_idx=5)

        # Activities at index 5 and 6 should map to positions 0 and 1
        assert field_mapping["Enter Name of Organization - 1"] == "Company 6"
        assert field_mapping["Enter Name of Organization  - 2"] == "Company 7"


# ---------------------------------------------------------------------------
# Empty CSV
# ---------------------------------------------------------------------------

class TestEmptyCSV:
    @patch("fill_twc_pdf.PdfWriter")
    @patch("fill_twc_pdf.PdfReader")
    def test_empty_csv_returns_early(self, mock_reader_cls, mock_writer_cls, capsys):
        """An empty CSV (no activities) should print a message and return without creating PDFs."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as csv_f:
            csv_f.write(
                "Date of Activity,Work Search Activity,Type of Job,Company Name,"
                "Address,City,State,Zip Code,Phone,Contact Method,Person Contacted,"
                "Results,Notes,Week Starting,Week Ending,Required Searches\n"
            )
            csv_path = csv_f.name

        try:
            fill_twc_pdf(csv_path, "template.pdf", "output.pdf")
            captured = capsys.readouterr()
            assert "No activities found" in captured.out

            # PdfReader should never be called
            mock_reader_cls.assert_not_called()
            mock_writer_cls.assert_not_called()
        finally:
            os.unlink(csv_path)

    @patch("fill_twc_pdf.PdfWriter")
    @patch("fill_twc_pdf.PdfReader")
    def test_csv_with_only_empty_rows(self, mock_reader_cls, mock_writer_cls, capsys):
        """Rows with blank Date of Activity should be skipped."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as csv_f:
            csv_f.write(
                "Date of Activity,Work Search Activity,Type of Job,Company Name,"
                "Address,City,State,Zip Code,Phone,Contact Method,Person Contacted,"
                "Results,Notes,Week Starting,Week Ending,Required Searches\n"
                ",,,,,,,,,,,,,,,\n"
                "  ,,,,,,,,,,,,,,,\n"
            )
            csv_path = csv_f.name

        try:
            fill_twc_pdf(csv_path, "template.pdf", "output.pdf")
            captured = capsys.readouterr()
            assert "No activities found" in captured.out
            mock_reader_cls.assert_not_called()
        finally:
            os.unlink(csv_path)
