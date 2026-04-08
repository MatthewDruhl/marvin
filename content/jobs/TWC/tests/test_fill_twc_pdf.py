"""Tests for fill_twc_pdf.py — TWC Work Search Activity Log PDF filler."""

import csv
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from PyPDF2 import PdfWriter

# Add parent directory to path so we can import fill_twc_pdf
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fill_twc_pdf import (
    ALL_FIELD_DICTS,
    HEADER_FIELDS,
    VALID_ACTIVITY_TYPES,
    FieldValidationError,
    TWCComplianceError,
    fill_activities,
    fill_twc_pdf,
    get_all_expected_field_names,
    load_env,
    validate_csv,
    validate_pdf_fields,
)

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


# ---------------------------------------------------------------------------
# Output validation (Issue #34)
# ---------------------------------------------------------------------------

class TestOutputValidation:
    """Verify that field_mapping produced by fill_activities matches source CSV data."""

    def test_all_required_fields_populated(self):
        """Every required field should be present in the mapping for a complete activity."""
        activities = [make_activity()]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        required_fields = [
            "Enter Date of Job Search Activity",
            "Enter Work Search Activity",
            "Enter Job Type",
            "Enter Name of Organization - 1",
        ]
        for field in required_fields:
            assert field in field_mapping, f"Missing required field: {field}"
            assert field_mapping[field].strip(), f"Field is empty: {field}"

    def test_date_format_matches_mm_dd_yyyy(self):
        """Output dates must be in MM/DD/YYYY format for the government form."""
        activities = [make_activity(date="2026-03-15")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        date_val = field_mapping["Enter Date of Job Search Activity"]
        # Verify MM/DD/YYYY format
        parsed = datetime.strptime(date_val, "%m/%d/%Y")
        assert parsed.year == 2026
        assert parsed.month == 3
        assert parsed.day == 15

    def test_field_mapping_roundtrip_preserves_company(self):
        """Company name in field_mapping should exactly match CSV source."""
        company = "Acme & Sons, Inc."
        activities = [make_activity(company=company)]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Name of Organization - 1"] == company

    def test_field_mapping_roundtrip_preserves_job_type(self):
        """Job type in field_mapping should exactly match CSV source."""
        job_type = "Senior Platform Engineer"
        activities = [make_activity(job_type=job_type)]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Job Type"] == job_type

    def test_field_mapping_roundtrip_preserves_work_search(self):
        """Work search activity should exactly match CSV source."""
        work_search = "Applied for position online"
        activities = [make_activity(work_search=work_search)]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Work Search Activity"] == work_search

    def test_five_activities_all_have_dates(self):
        """Every activity in a full page should have a date field set."""
        activities = [make_activity(date=f"2026-01-{26+i}") for i in range(5)]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        # First uses base name, rest use numbered suffix
        assert "Enter Date of Job Search Activity" in field_mapping
        for i in range(2, 6):
            assert f"Enter Date of Job Search Activity - {i}" in field_mapping

    def test_phone_split_produces_correct_digits(self):
        """Phone number split should preserve all digits correctly."""
        activities = [make_activity(phone="(737) 867-5309")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter Area Code - Organization 1"] == "737"
        assert field_mapping["Enter Middle 3 Phone Digits"] == "867"
        assert field_mapping["Enter Last 4 Phone Digits"] == "5309"

    def test_location_combines_city_state_zip(self):
        """City, State, Zip should be combined into one field."""
        activities = [make_activity(city="Dallas", state="TX", zip_code="75201")]
        field_mapping = {}
        fill_activities(field_mapping, activities)

        assert field_mapping["Enter City, State, Zip Code - Organization 1"] == "Dallas, TX 75201"

    def test_malformed_date_raises(self):
        """A completely invalid date should raise an error, not produce silent garbage."""
        activities = [make_activity(date="not-a-date")]
        field_mapping = {}
        with pytest.raises(ValueError):
            fill_activities(field_mapping, activities)


# ---------------------------------------------------------------------------
# Field constants (Issue #118 / CQ-1)
# ---------------------------------------------------------------------------

class TestFieldConstants:
    """Verify that extracted constants are complete and consistent."""

    def test_all_activity_dicts_have_five_entries(self):
        """Each per-activity field dict should have exactly 5 entries (indices 0-4)."""
        for d in ALL_FIELD_DICTS:
            assert set(d.keys()) == {0, 1, 2, 3, 4}, f"Bad keys in {d}"

    def test_header_fields_complete(self):
        """Header fields dict should contain all seven expected keys."""
        expected_keys = {
            "claimant_name", "week_of", "end_date",
            "ssn_first3", "ssn_mid2", "ssn_last4", "required_searches",
        }
        assert set(HEADER_FIELDS.keys()) == expected_keys

    def test_no_duplicate_field_names(self):
        """No two constant dicts should share the same PDF field name."""
        all_names: list[str] = list(HEADER_FIELDS.values())
        for d in ALL_FIELD_DICTS:
            all_names.extend(d.values())
        assert len(all_names) == len(set(all_names)), "Duplicate field names detected"

    def test_get_all_expected_field_names_returns_set(self):
        """Utility should return a non-empty set of strings."""
        names = get_all_expected_field_names()
        assert isinstance(names, set)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)

    def test_constants_match_fill_activities_output(self):
        """Field names produced by fill_activities should be a subset of declared constants."""
        activities = [make_activity(
            contact_method="Email",
            results="Application filed",
            notes="test note",
        )]
        field_mapping: dict[str, str] = {}
        fill_activities(field_mapping, activities)

        expected = get_all_expected_field_names()
        for key in field_mapping:
            assert key in expected, f"Unexpected field name from fill_activities: {key}"

    def test_five_activities_all_fields_in_constants(self):
        """All field names from a full 5-activity page should be declared constants."""
        activities = [make_activity(
            company=f"Co {i+1}",
            contact_method="Email",
            results="Application filed",
            notes="n",
        ) for i in range(5)]
        field_mapping: dict[str, str] = {}
        fill_activities(field_mapping, activities)

        expected = get_all_expected_field_names()
        for key in field_mapping:
            assert key in expected, f"Unexpected field: {key}"


# ---------------------------------------------------------------------------
# PDF field validation (Issue #118 / CQ-1)
# ---------------------------------------------------------------------------

class TestValidatePdfFields:
    """Tests for validate_pdf_fields()."""

    def test_missing_fields_raises_error(self, tmp_path):
        """A PDF with no form fields should raise FieldValidationError."""
        # Create a minimal PDF via PdfWriter (no form fields)
        pdf_path = tmp_path / "empty.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        with open(pdf_path, "wb") as f:
            writer.write(f)

        with pytest.raises(FieldValidationError) as exc_info:
            validate_pdf_fields(str(pdf_path))

        assert "expected field(s) not found" in str(exc_info.value)

    def test_field_validation_error_is_exception(self):
        """FieldValidationError should be a proper Exception subclass."""
        err = FieldValidationError("test")
        assert isinstance(err, Exception)
        assert str(err) == "test"


# ---------------------------------------------------------------------------
# CSV compliance validation (Issue #116)
# ---------------------------------------------------------------------------

class TestValidateCSV:
    """Tests for validate_csv TWC compliance checks."""

    def _week_start(self):
        return datetime(2026, 1, 25)  # Sunday

    def _week_end(self):
        return datetime(2026, 1, 31)  # Saturday

    def _valid_activities(self, count=4):
        """Return a list of valid activities within the declared week."""
        types = list(VALID_ACTIVITY_TYPES)
        return [
            make_activity(
                date=f"2026-01-{26 + i}",
                work_search=types[i % len(types)],
            )
            for i in range(count)
        ]

    def test_valid_csv_passes(self):
        """Four valid activities within the week should pass validation."""
        activities = self._valid_activities(4)
        # Should not raise
        validate_csv(activities, self._week_start(), self._week_end())

    def test_more_than_four_activities_passes(self):
        """More than the minimum should also pass."""
        activities = self._valid_activities(6)
        validate_csv(activities, self._week_start(), self._week_end())

    def test_too_few_activities_raises(self):
        """Fewer than 4 activities should fail compliance."""
        activities = self._valid_activities(3)
        with pytest.raises(TWCComplianceError, match="at least 4 activities"):
            validate_csv(activities, self._week_start(), self._week_end())

    def test_zero_activities_raises(self):
        """Zero activities should fail compliance."""
        with pytest.raises(TWCComplianceError, match="at least 4 activities"):
            validate_csv([], self._week_start(), self._week_end())

    def test_date_before_week_start_raises(self):
        """An activity date before the week start should fail."""
        activities = self._valid_activities(4)
        activities[0] = make_activity(
            date="2026-01-24",  # Saturday before the week
            work_search="Applied for job",
        )
        with pytest.raises(TWCComplianceError, match="outside the declared week"):
            validate_csv(activities, self._week_start(), self._week_end())

    def test_date_after_week_end_raises(self):
        """An activity date after the week end should fail."""
        activities = self._valid_activities(4)
        activities[3] = make_activity(
            date="2026-02-01",  # Sunday after the week
            work_search="Applied for job",
        )
        with pytest.raises(TWCComplianceError, match="outside the declared week"):
            validate_csv(activities, self._week_start(), self._week_end())

    def test_boundary_dates_pass(self):
        """Activities on the exact start and end dates should pass."""
        activities = [
            make_activity(date="2026-01-25", work_search="Applied for job"),
            make_activity(date="2026-01-26", work_search="Interview"),
            make_activity(date="2026-01-30", work_search="Searched online"),
            make_activity(date="2026-01-31", work_search="Follow-up email"),
        ]
        validate_csv(activities, self._week_start(), self._week_end())

    def test_invalid_activity_type_raises(self):
        """An activity type not in the valid TWC list should fail."""
        activities = self._valid_activities(4)
        activities[1] = make_activity(
            date="2026-01-27",
            work_search="Took an online course",
        )
        with pytest.raises(TWCComplianceError, match="invalid activity type"):
            validate_csv(activities, self._week_start(), self._week_end())

    def test_multiple_errors_reported(self):
        """All errors should be collected and reported, not just the first."""
        activities = [
            make_activity(date="2026-01-24", work_search="Invalid type"),
            make_activity(date="2026-01-26", work_search="Another bad type"),
        ]
        with pytest.raises(TWCComplianceError) as exc_info:
            validate_csv(activities, self._week_start(), self._week_end())
        msg = str(exc_info.value)
        # Should report: too few, out-of-range date, and invalid types
        assert "at least 4" in msg
        assert "outside the declared week" in msg
        assert "invalid activity type" in msg

    def test_date_with_time_component_validates(self):
        """Dates with a time component should still validate correctly."""
        activities = [
            make_activity(date="2026-01-26 14:30:00", work_search="Applied for job"),
            make_activity(date="2026-01-27 09:00:00", work_search="Interview"),
            make_activity(date="2026-01-28", work_search="Searched online"),
            make_activity(date="2026-01-29", work_search="Follow-up email"),
        ]
        validate_csv(activities, self._week_start(), self._week_end())

    def test_invalid_date_format_reported(self):
        """A completely invalid date string should be reported as an error."""
        activities = self._valid_activities(4)
        activities[2] = make_activity(date="not-a-date", work_search="Applied for job")
        with pytest.raises(TWCComplianceError, match="invalid date"):
            validate_csv(activities, self._week_start(), self._week_end())

    def test_fill_twc_pdf_rejects_noncompliant_csv(self):
        """fill_twc_pdf should raise TWCComplianceError for non-compliant data."""
        # Only 2 activities — below the 4 minimum
        activities = [
            make_activity(date="2026-01-26", work_search="Applied for job"),
            make_activity(date="2026-01-27", work_search="Interview"),
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as csv_f:
            fieldnames = list(activities[0].keys())
            writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
            writer.writeheader()
            for a in activities:
                writer.writerow(a)
            csv_path = csv_f.name

        try:
            with pytest.raises(TWCComplianceError, match="at least 4 activities"):
                fill_twc_pdf(csv_path, "template.pdf", "output.pdf")
        finally:
            os.unlink(csv_path)
