# AutoCAD automation on macOS

Read this reference only when the drawing workflow runs on macOS or a headless
AutoCAD build needs a GUI export adapter.

## Adapter boundary

Discover the installed AutoCAD application and its Core Console executable; do
not assume a particular release or installation path. Discover `osascript`,
`pdfinfo`, and a PDF rasterizer such as `pdftoppm` in the same preflight. Keep
machine paths overridable without changing tracked drawing sources.

Use Core Console for the deterministic portion: load the source template, run
the generator, populate attributes, save the derived DWG, and run `AUDIT`. Use a
temporary command script, remove it on exit, and preserve the console output.

The macOS Core Console may crash while initializing a PDF plot driver even when
generation and audit work correctly. If that happens, keep the passing console
path and move only PDF export behind a small GUI adapter. Do not retry the same
crashing plot path indefinitely or shift all drawing construction into GUI
automation.

## GUI export contract

Before launching automation, verify Accessibility permission and ensure the
target output does not appear to be a newer passing artifact. The adapter
should:

1. open the exact derived DWG and wait for its document window;
2. assert the expected plotter, paper, area, scale, orientation, and style;
3. export to an explicit output path and wait with a bounded timeout;
4. capture a diagnostic screenshot or UI state when an expected control is
   absent;
5. close only the generated document, handling any save prompt according to the
   workflow contract; and
6. return AutoCAD to a known state without terminating unrelated drawings.

Plotting can mark a document dirty. When the audited DWG must remain byte-for-
byte authoritative, discard GUI-only plot changes on close. Confirm that no
`.dwl` or `.dwl2` lock remains. Use a shell builtin or a discovered executable
for file waits rather than assuming `/usr/bin/test` exists.

AppleScript UI automation depends on application, menu, window, and control
labels. Treat those labels and popup ordering as a versioned adapter: fail on an
unexpected value instead of clicking by position and hoping the remembered UI
still applies.

## Known failure patterns

| Signal | Response |
|---|---|
| Core Console crashes while loading the PDF driver | Keep headless generation/audit and export through the full application. |
| Title text overlaps despite correct attributes | Inspect duplicate attribute aliases, font substitution, MTEXT width/height, and the rendered sheet. |
| PDF exists but has the wrong sheet | Verify page count and physical dimensions with `pdfinfo`; do not accept existence alone. |
| Export leaves a drawing open or creates locks | Close the exact derived document, resolve its save state, and fail if locks remain. |
| UI labels or popup order changed | Stop the adapter, retain diagnostics, and update the version-specific selectors. |
| A failed rebuild replaced trusted evidence | Preserve the last passing manifest and mark current outputs unverified. |

Convert the PDF to a review image at a declared resolution and inspect it. GUI
export success, DWG audit success, and visual acceptance remain three distinct
checks.
