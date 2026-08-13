---
name: publish-novel-pdf
description: Typeset the current canonical novel manuscript into a polished, print-style PDF and validate the result. Use when Codex is asked to publish, export, typeset, compile, render, or periodically rebuild a novel PDF from manuscript scene files, including requests for a reading copy, book cover, trade paperback layout, title page, chapters, running heads, or page numbers.
---

# Publish Novel PDF

Build a deterministic reading PDF from canonical scene files without editing manuscript prose.

## Workflow

1. Locate the project root containing `.novel/config.yaml` and `AGENTS.md`.
2. Read `.novel/publishing.yaml` when present. Read [configuration.md](references/configuration.md) only when changing publishing settings or diagnosing input order.
3. Run:

   ```bash
   <bundled-python> scripts/build_novel_pdf.py --project-root <project-root>
   ```

   Use the Python runtime returned by `codex_app__load_workspace_dependencies`; it includes ReportLab and PDF inspection packages.
4. Refuse to publish when no scene files exist unless `--allow-empty` is explicitly used for pipeline testing.
5. Render the PDF with `pdftoppm`; inspect the cover when configured, the title page, every chapter opener, several representative text pages, and the final page. For a short PDF, inspect every page.
6. Run `pdfinfo` and use `pypdf` or `pdfplumber` to confirm page count, page size, extractable title/chapter text, and absence of blank trailing pages.
7. Report the output path, included scene/chapter count, and any warnings. Never present an empty test build as a current-manuscript edition.

## Guardrails

- Treat `manuscript/` and `planning/scene-index.yaml` as read-only inputs.
- Exclude `manuscript/README.md`, hidden files, and files beginning with `_`.
- Prefer scene-index order when it provides file paths; otherwise use natural filename order.
- Preserve prose wording. Interpret only lightweight Markdown needed for typography: paragraphs, emphasis, headings, and centered scene breaks.
- Do not incorporate planning, research, intake, notes, or editorial files unless the author explicitly configures them as front or back matter.
- When `cover_image` is configured, require it to match the trim aspect ratio and place it full bleed on the first PDF page without changing manuscript page numbering.
- Write finished editions to `output/pdf/` and temporary renders to `tmp/pdfs/`.
- Use a stable filename by default so recurring automation replaces the prior reading copy intentionally.

## Changing the design

Edit `.novel/publishing.yaml`, not the build script, for cover image, title, author, subtitle, trim size, margins, font, font size, line spacing, and output filename. Change the script only when adding a reusable layout capability.
