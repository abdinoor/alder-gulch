# Publishing configuration

The builder reads `.novel/publishing.yaml`. It supports a deliberately small YAML subset: one `key: value` per line, quoted or unquoted scalar values, booleans, and decimal numbers.

Supported keys:

- `title`, `subtitle`, `author`, `edition`
- `output_filename`
- `back_matter_file`, `back_matter_title`
- `trim_width_in`, `trim_height_in`
- `font_regular`, `font_italic`, `font_bold`, `font_bold_italic`
- `body_font_size`, `leading`
- `inner_margin_in`, `outer_margin_in`, `top_margin_in`, `bottom_margin_in`
- `chapter_label` (`Chapter` by default)
- `running_heads`, `page_numbers`

Scene discovery:

1. Read the manuscript directory from `.novel/config.yaml` (default `manuscript`).
2. If `planning/scene-index.yaml` contains recognized `file:`, `path:`, or `manuscript_file:` entries, publish those files in listed order.
3. Append any unindexed scene files in natural path order and emit a warning.
4. Group `01.01-opening.md`, `01.02-arrival.md`, and similar names as Chapter 1. A top-level `01-opening.md` becomes Chapter 1 on its own.

Markdown handling is intentionally conservative. A single `#` heading can supply a chapter title; `##` and deeper headings become in-text subheads. Lines containing only `***`, `---`, or `* * *` become centered scene breaks. YAML frontmatter is omitted.

When `back_matter_file` names a project-relative Markdown file, the builder places its body on a new final page without counting it as a scene or chapter. The file's first-level heading is omitted. Set `back_matter_title` to add an optional displayed heading; leave it empty for unheaded back matter such as back-cover copy.
