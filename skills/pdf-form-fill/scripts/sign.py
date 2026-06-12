#!/usr/bin/env python3
"""
sign.py - apply a signature and date to a PDF, then optionally lock it.

The signature can be typed text rendered in a script font, or a pre-made
signature image (transparent PNG recommended). Placement is either explicit
coordinates or anchor-based: give the label text that sits next to the line
(e.g. "Signature" and "Date") and the helper places the mark just after it.

Examples:
  # Anchor-based (finds the line by nearby label text), then lock:
  python sign.py INPUT.pdf OUTPUT.pdf \
      --text "Matthew Druhl" \
      --sig-anchor "Signature" --date "06/09/2026" --date-anchor "Date" \
      --lock

  # Use a signature image instead of typed text:
  python sign.py INPUT.pdf OUTPUT.pdf \
      --sig-image ~/.signatures/matt.png --sig-anchor "Signature" \
      --date "06/09/2026" --date-anchor "Date" --lock

  # Explicit coordinates (PDF points from bottom-left), page index 0:
  python sign.py INPUT.pdf OUTPUT.pdf \
      --text "Matthew Druhl" --sig-xy 135 233 \
      --date "06/09/2026" --date-xy 415 233

Locking uses pdftk (preferred) or qpdf to flatten interactive fields into
static page content so nothing can be edited after signing.
"""
import argparse
import os
import shutil
import subprocess
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FONT = os.path.join(HERE, "..", "assets", "fonts", "Allura-Regular.ttf")

# Default signature image. The skill uses this automatically when no
# --sig-image or --text is given, so the user never has to supply the path.
# Override per-run with the SIGNATURE_IMAGE environment variable.
DEFAULT_SIG = os.environ.get("SIGNATURE_IMAGE") or os.path.expanduser(
    "~/.signatures/signature.png"
)


def find_anchor(pdf_path, label, page_index, occurrence="last"):
    """Return (x_after_label, baseline_y_pdf) for a label on the page.

    `label` may be a single word or a multi-word phrase on one line (e.g.
    "U.S. person" or "Date"). Phrase matching disambiguates common words.
    `occurrence` is "first" (topmost match) or "last" (lowest match); pick
    whichever isolates the signing line on a given form. Returns the position
    just after the last word of the match.

    Note: labels that wrap across two lines (the W-9's "Signature of / U.S.
    person") will not match as one phrase. For those, use explicit --sig-xy.
    """
    import pdfplumber

    tokens = label.split()
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_index]
        h = page.height
        words = page.extract_words()
        lines = {}
        for w in words:
            lines.setdefault(round(w["top"]), []).append(w)
        matches = []  # (bottom, x1_of_last_token, baseline_y)
        for top, lw in lines.items():
            lw = sorted(lw, key=lambda x: x["x0"])
            clean = [x["text"].strip(":.\u25b6 ") for x in lw]
            for i in range(len(clean) - len(tokens) + 1):
                if clean[i:i + len(tokens)] == tokens:
                    last = lw[i + len(tokens) - 1]
                    matches.append((last["bottom"], last["x1"], h - last["bottom"]))
                    break
        if not matches:
            raise ValueError(f"anchor not found on page {page_index}: {label!r}")
        matches.sort(key=lambda m: m[0])  # by vertical position, top to bottom
        chosen = matches[0] if occurrence == "first" else matches[-1]
        return chosen[1], chosen[2]


def build_overlay(page, items):
    """items: list of dicts with kind/text|image, x, y, size/width. Returns overlay page."""
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    for it in items:
        if it["kind"] == "text":
            c.setFont(it["font"], it["size"])
            c.drawString(it["x"], it["y"], it["text"])
        elif it["kind"] == "image":
            iw = it.get("width")
            ih = it.get("height")
            if iw and not ih:
                from PIL import Image as _PILImage
                with _PILImage.open(it["path"]) as _im:
                    ih = iw * (_im.height / _im.width)
            c.drawImage(
                it["path"], it["x"], it["y"],
                width=iw, height=ih,
                preserveAspectRatio=True, mask="auto",
            )
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def lock(in_path, out_path):
    if shutil.which("pdftk"):
        subprocess.run(["pdftk", in_path, "output", out_path, "flatten"], check=True)
    elif shutil.which("qpdf"):
        subprocess.run(
            ["qpdf", "--generate-appearances", "--flatten-annotations=all", in_path, out_path],
            check=True,
        )
    else:
        raise RuntimeError("locking needs pdftk or qpdf installed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--page", type=int, default=0, help="page index for the signature (default 0)")
    ap.add_argument("--text", help="signature text rendered in the script font")
    ap.add_argument("--font", default=DEFAULT_FONT, help="path to a TTF for the signature text")
    ap.add_argument("--size", type=float, default=24, help="signature font size (default 24)")
    ap.add_argument("--sig-image", help="path to a signature image (transparent PNG)")
    ap.add_argument("--sig-width", type=float, default=150, help="signature image width in pts")
    ap.add_argument("--sig-anchor", help="label text the signature line sits next to, e.g. Signature")
    ap.add_argument("--sig-xy", nargs=2, type=float, metavar=("X", "Y"), help="explicit signature x y")
    ap.add_argument("--date", help="date string to place")
    ap.add_argument("--date-size", type=float, default=11)
    ap.add_argument("--date-anchor", help="label text the date sits next to, e.g. Date")
    ap.add_argument("--date-xy", nargs=2, type=float, metavar=("X", "Y"), help="explicit date x y")
    ap.add_argument("--gap", type=float, default=8, help="horizontal gap after an anchor label (pts)")
    ap.add_argument("--occurrence", choices=["first", "last"], default="last",
                    help="which anchor match to use when a label repeats (default last)")
    ap.add_argument("--lock", action="store_true", help="flatten the result so it cannot be edited")
    args = ap.parse_args()

    # Expand ~ in any user-supplied path so it resolves regardless of caller.
    args.input = os.path.expanduser(args.input)
    args.output = os.path.expanduser(args.output)
    args.font = os.path.expanduser(args.font)
    if args.sig_image:
        args.sig_image = os.path.expanduser(args.sig_image)

    # If no signature source was given but a placement was, fall back to the
    # default signature image so the caller never has to supply the path.
    if not args.text and not args.sig_image and (args.sig_xy or args.sig_anchor):
        if os.path.exists(DEFAULT_SIG):
            args.sig_image = DEFAULT_SIG
        else:
            ap.error(
                f"no signature given and default not found at {DEFAULT_SIG}. "
                "Save your signature there, set SIGNATURE_IMAGE, or pass --sig-image/--text."
            )

    reader = PdfReader(args.input)
    page = reader.pages[args.page]
    items = []

    # Signature
    if args.text or args.sig_image:
        if args.sig_xy:
            sx, sy = args.sig_xy
        elif args.sig_anchor:
            ax, ay = find_anchor(args.input, args.sig_anchor, args.page, args.occurrence)
            sx, sy = ax + args.gap, ay
        else:
            ap.error("signature needs --sig-xy or --sig-anchor")
        if args.text:
            pdfmetrics.registerFont(TTFont("SigFont", args.font))
            items.append({"kind": "text", "text": args.text, "font": "SigFont", "size": args.size, "x": sx, "y": sy})
        else:
            items.append({"kind": "image", "path": args.sig_image, "x": sx, "y": sy, "width": args.sig_width})

    # Date
    if args.date:
        if args.date_xy:
            dx, dy = args.date_xy
        elif args.date_anchor:
            ax, ay = find_anchor(args.input, args.date_anchor, args.page, args.occurrence)
            dx, dy = ax + args.gap, ay
        else:
            ap.error("date needs --date-xy or --date-anchor")
        items.append({"kind": "text", "text": args.date, "font": "Helvetica", "size": args.date_size, "x": dx, "y": dy})

    if not items:
        ap.error("nothing to do: pass --text/--sig-image and/or --date")

    writer = PdfWriter()
    writer.append(reader)
    overlay = build_overlay(page, items)
    writer.pages[args.page].merge_page(overlay)

    if args.lock:
        tmp = args.output + ".tmp.pdf"
        with open(tmp, "wb") as f:
            writer.write(f)
        lock(tmp, args.output)
        os.remove(tmp)
    else:
        with open(args.output, "wb") as f:
            writer.write(f)

    print(f"wrote {args.output} (locked={args.lock})")


if __name__ == "__main__":
    main()
