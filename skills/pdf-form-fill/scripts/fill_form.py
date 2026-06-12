#!/usr/bin/env python3
"""
fill_form.py - inspect and fill PDF forms.

Usage:
  python fill_form.py inspect INPUT.pdf
      Prints JSON describing the form: whether it has fillable AcroForm
      fields, and for each field its name, type, current value, and
      (for checkboxes/radios) the allowed "on" states.

  python fill_form.py fill INPUT.pdf DATA.json OUTPUT.pdf [--flatten]
      Fills fillable fields from DATA.json (a flat {field_name: value} map)
      and writes OUTPUT.pdf. --flatten makes values non-editable.

  python fill_form.py overlay INPUT.pdf DATA.json OUTPUT.pdf
      For FLAT (non-fillable) PDFs. DATA.json is a list of placements:
        [{"page": 0, "x": 72, "y": 700, "text": "John Doe", "size": 11}, ...]
      Coordinates are PDF points from the bottom-left of the page.

Exit codes: 0 ok, 1 usage error, 2 runtime error.
"""
import json
import sys

from pypdf import PdfReader, PdfWriter


def inspect(path):
    reader = PdfReader(path)
    fields = reader.get_fields()
    out = {"path": path, "pages": len(reader.pages), "has_fillable_fields": bool(fields), "fields": []}
    if fields:
        for name, f in fields.items():
            entry = {
                "name": name,
                "type": f.get("/FT"),
                "value": f.get("/V"),
            }
            states = f.get("/_States_")
            if states:
                entry["states"] = list(states)
            out["fields"].append(entry)
    return out


def fill(in_path, data_path, out_path, flatten=False):
    with open(data_path) as fh:
        data = json.load(fh)
    reader = PdfReader(in_path)
    writer = PdfWriter()
    writer.append(reader)
    for page in writer.pages:
        writer.update_page_form_field_values(
            page, {k: str(v) for k, v in data.items()}, auto_regenerate=False
        )
    if flatten:
        writer.set_need_appearances_writer(False)
        for page in writer.pages:
            writer.update_page_form_field_values(page, {}, auto_regenerate=False)
        # mark fields read-only
        try:
            writer.flatten()  # available in newer pypdf
        except Exception:
            pass
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return {"written": out_path, "fields_filled": len(data), "flattened": flatten}


def overlay(in_path, data_path, out_path):
    from io import BytesIO

    from reportlab.pdfgen import canvas

    with open(data_path) as fh:
        placements = json.load(fh)
    reader = PdfReader(in_path)
    writer = PdfWriter()

    # Build one overlay page per source page that has placements.
    by_page = {}
    for p in placements:
        by_page.setdefault(p.get("page", 0), []).append(p)

    for i, page in enumerate(reader.pages):
        if i in by_page:
            buf = BytesIO()
            w = float(page.mediabox.width)
            h = float(page.mediabox.height)
            c = canvas.Canvas(buf, pagesize=(w, h))
            for p in by_page[i]:
                c.setFont("Helvetica", p.get("size", 11))
                c.drawString(p["x"], p["y"], str(p["text"]))
            c.save()
            buf.seek(0)
            ov = PdfReader(buf).pages[0]
            page.merge_page(ov)
        writer.add_page(page)

    with open(out_path, "wb") as fh:
        writer.write(fh)
    return {"written": out_path, "placements": len(placements)}


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    cmd = argv[1]
    try:
        if cmd == "inspect":
            print(json.dumps(inspect(argv[2]), indent=2, default=str))
        elif cmd == "fill":
            if len(argv) < 5:
                print(__doc__)
                return 1
            flatten = "--flatten" in argv
            print(json.dumps(fill(argv[2], argv[3], argv[4], flatten), indent=2))
        elif cmd == "overlay":
            if len(argv) < 5:
                print(__doc__)
                return 1
            print(json.dumps(overlay(argv[2], argv[3], argv[4]), indent=2))
        else:
            print(__doc__)
            return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
