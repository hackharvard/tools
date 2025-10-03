# HackHarvard Walk-In Confirmation (Static Frontend)

A simple, modern, accessible frontend for confirming walk-in attendance at HackHarvard.

## Files
- `index.html` – main page with the waiver workflow and required agreements.
- `style.css` – modern dark theme styling.
- `main.js` – interaction logic (enable waiver acceptance after opening the PDF, validate checkboxes, show confirmation).
- `walkin_waiver.pdf` – required waiver PDF (you must add this file).

## Setup
1. Place your PDF as `walkin_waiver.pdf` in the same directory as `index.html`.
2. Serve the folder with any static server, for example:

   ```bash
   python3 -m http.server 8000
   ```

3. Open `http://127.0.0.1:8000/` in your browser.

## Behavior
- The "Open Waiver PDF" button opens `walkin_waiver.pdf` in a new tab. If a popup blocker prevents this, a direct download link is shown.
- The checkbox to accept the waiver becomes enabled after clicking the open button.
- Two additional required checkboxes:
  - Media release agreement (exact language supplied).
  - Final decision confirmation (no more changes after submitting).
- The "Submit Confirmation" button enables only when all required boxes are checked and shows a confirmation receipt with timestamp when submitted.

## Customization
- Update colors or spacing in `style.css`.
- Replace the page title or logo in `index.html` as needed.

## Notes
- This is a static client-only implementation. If you need to persist submissions, connect it to an API or store results via a backend.
