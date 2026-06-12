---
name: pdf-form-fill
description: Inspect, fill, sign, and lock PDF forms, both fillable (AcroForm) and flat/scanned
---



# PDF Form Fill Skill

Fills PDF forms from supplied data, applies a signature and date, and locks
the result so it cannot be edited. Handles fillable forms with real form
fields and flat or scanned forms via coordinate overlay. Always inspects the
PDF first so field names and signing positions are confirmed before anything
is written.

## Trigger Phrases
- "fill out this PDF"
- "fill out this form"
- "complete this PDF form"
- "sign this PDF"
- "sign and date this form"
- "lock this form" / "flatten this PDF"

## Dependencies
- Python: pypdf, reportlab, pdfplumber, pillow
- System: pdftk or qpdf (for locking), poppler-utils (pdftoppm, for visual checks)
- Install Python deps once: pip install pypdf reportlab pdfplumber pillow
- Helper scripts live in scripts/ inside this skill directory.
- A signature script font is bundled at assets/fonts/Allura-Regular.ttf.

## Scripts
- scripts/fill_form.py: inspect, fill, and overlay text on forms.
- scripts/sign.py: place a signature (typed script font or image) and date,
  with optional locking.

## Fill Workflow

When asked to fill a form, Claude should:

1. Locate the source PDF (user path or upload).
2. Inspect it:
   python scripts/fill_form.py inspect SOURCE.pdf
3. Read the result. If has_fillable_fields is true, note every field name,
   type, and for checkboxes/radios the allowed states. If false, the form is
   flat and needs the overlay path.
4. Gather values from the user, context, or a data file. Never invent values.
5. Confirm the field-to-value mapping with the user before writing. This is
   the review gate.
6. Fill:
   - Fillable: write data.json as a flat {field_name: value} map, then
     python scripts/fill_form.py fill SOURCE.pdf data.json OUTPUT.pdf
   - Flat: write placements.json as a list of
     {"page","x","y","text","size"} entries, then
     python scripts/fill_form.py overlay SOURCE.pdf placements.json OUTPUT.pdf
7. Verify by inspecting OUTPUT.pdf or rasterizing a page.
8. Provide the result via present_files.

## Sign and Lock Workflow

When asked to sign or sign-and-lock a form, Claude should:

1. Confirm what the user wants signed. A signature on a certification (for
   example a W-9 Part II) is signed under penalties of perjury, so confirm
   the exact signature mark, the date, and that the user wants it applied.
   Never fabricate a signature the user did not specify.
2. Find the signing position. The signature and date line is often flat space
   with no fillable field. Locate it one of two ways:
   - Anchor: pass the label text the line sits next to (for example
     --date-anchor "Date"). Use --occurrence first or last when a label
     repeats on the page.
   - Explicit coordinates: render the page (pdftoppm) and read positions with
     pdfplumber, then pass --sig-xy and --date-xy. Coordinates are PDF points
     from the bottom-left of the page; US Letter is 612 by 792. Use explicit
     coordinates when the label wraps across two lines, because anchoring
     matches single lines only.
3. Sign with the default signature, the bundled font (typed), or a specific
   signature image. The signature SOURCE is resolved automatically in this
   order, so the user does not need to supply it:
   - explicit --text (typed script signature), or
   - explicit --sig-image PATH, or
   - the default signature image at ~/.signatures/signature.png (override
     with the SIGNATURE_IMAGE environment variable).
   When the user asks to sign and has a default signature on file, do not ask
   where it is. Just give a placement (--sig-xy or --sig-anchor) and let the
   script load the default:
   python scripts/sign.py SOURCE.pdf OUTPUT.pdf \
       --sig-xy X Y --sig-width 150 \
       --date "MM/DD/YYYY" --date-xy X Y --lock
   To override for one run, add --text "Full Name" or --sig-image /path.png.
4. Render the signed page and confirm placement before delivering.
5. Locking (--lock) flattens all interactive fields into static content using
   pdftk or qpdf, so neither the filled fields nor the signature can be edited
   afterward. Apply locking only once the user has approved the content.

## Known Coordinates: IRS W-9 (Rev. 10-2018)
- Page index 0.
- Signature: --sig-xy 135 233 (size 24 in the bundled font).
- Date: --date-xy 415 233.

## Signature Assets
- Default signature image location: ~/.signatures/signature.png. The skill
  uses it automatically when no --text or --sig-image is given. Override per
  run with the SIGNATURE_IMAGE environment variable or --sig-image.
- The bundled font can produce a typed script signature on demand instead.
- A signature image is sensitive: anyone holding it can apply the signature.
  Keep it in ~/.signatures/ (chmod 700 the dir, chmod 600 the file), outside
  any version-controlled or cloud-synced location. Never commit it to the
  Marvin repo. The skill .gitignore blocks signature images as a backstop.

## Formatting Standards
- Follow markdown-file-format skill guidelines.
- No bold, italic, or decorative formatting.
- Simple headers (# ## ###).

## Customization Note
This skill can be modified anytime. Request changes to the workflow or
defaults and Claude edits this SKILL.md with str_replace. Changes apply to
all future runs.

## Example Response After Signing
"Signed and locked the W-9. Placed your signature on the Sign Here line and
06/09/2026 in the Date field, then flattened the form so the fields and
signature can no longer be edited. The locked PDF is ready for download above.
A reusable signature image is also available; store it somewhere protected and
keep it out of the repo."
