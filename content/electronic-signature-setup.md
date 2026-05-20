# Electronic Signature Setup

**Status:** Not started
**Date:** 2026-05-15

## Goal
Set up a personal tool to add an electronic signature to documents (PDFs).

## Plan

### Step 1: Create Signature Image
Options:
- Sign on paper with dark pen, photograph it, clean up into transparent PNG
- Use macOS Preview (markup toolbar > signature tool > sign on trackpad or hold paper to camera), export
- Draw digitally on iPad/stylus, export as PNG

### Step 2: Clean Up Signature
- Remove background, make transparent PNG
- Crop and optimize for overlay use

### Step 3: Build Signing Tool
- Python script using `pypdf` or `reportlab`
- Overlays signature PNG onto a PDF at a specified location
- Usage: something like `sign document.pdf --page 1`
