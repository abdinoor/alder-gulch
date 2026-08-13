#!/usr/bin/env python3
"""Build a print-style reading PDF from a scene-based Markdown manuscript."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import OrderedDict
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.colors import black
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Flowable, Frame, PageBreak, PageTemplate, Paragraph, Spacer


DEFAULTS = {
    "title": "Untitled Novel",
    "subtitle": "",
    "author": "",
    "edition": "Reading Copy",
    "output_filename": "novel-reading-copy.pdf",
    "cover_image": "",
    "back_matter_file": "",
    "back_matter_title": "",
    "trim_width_in": 6.0,
    "trim_height_in": 9.0,
    "body_font_size": 10.5,
    "leading": 14.2,
    "inner_margin_in": 0.8,
    "outer_margin_in": 0.65,
    "top_margin_in": 0.7,
    "bottom_margin_in": 0.7,
    "font_regular": "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "font_italic": "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "font_bold": "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "font_bold_italic": "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
    "chapter_label": "Chapter",
    "running_heads": True,
    "page_numbers": True,
}


def scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    low = value.lower()
    if low in {"true", "yes", "on"}:
        return True
    if low in {"false", "no", "off"}:
        return False
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def read_simple_yaml(path: Path) -> dict:
    values = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key.strip()):
            values[key.strip()] = scalar(value)
    return values


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", str(path))]


def manuscript_dir(project: Path) -> Path:
    cfg = read_simple_yaml(project / ".novel" / "config.yaml")
    return project / str(cfg.get("manuscript_dir", "manuscript"))


def discover_scenes(project: Path) -> tuple[list[Path], list[str]]:
    root = manuscript_dir(project)
    all_files = sorted(
        (p for p in root.rglob("*.md") if p.name != "README.md" and not p.name.startswith(('.', '_'))),
        key=natural_key,
    )
    index = project / "planning" / "scene-index.yaml"
    ordered, warnings = [], []
    if index.exists():
        for raw in index.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\s*(?:-\s*)?(?:file|path|manuscript_file):\s*[\"']?([^\"'#]+)", raw)
            if not match:
                continue
            candidate = (project / match.group(1).strip()).resolve()
            if candidate.exists() and candidate.suffix.lower() == ".md" and candidate not in ordered:
                ordered.append(candidate)
    unindexed = [p.resolve() for p in all_files if p.resolve() not in ordered]
    if ordered and unindexed:
        warnings.append(f"appended {len(unindexed)} unindexed scene file(s) in filename order")
    return ordered + unindexed, warnings


def strip_frontmatter(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1 :])
    return "\n".join(lines)


def chapter_number(path: Path, fallback: int) -> int:
    for value in (path.name, path.parent.name):
        match = re.search(r"(?:^|ch[-_ ])(\d{1,3})(?:\D|$)", value, re.I)
        if match:
            return int(match.group(1))
    return fallback


def parse_scene(path: Path) -> tuple[str | None, list[tuple[str, str]]]:
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    blocks, current, chapter_title = [], [] , None

    def flush():
        if current:
            blocks.append(("paragraph", " ".join(x.strip() for x in current)))
            current.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"<!--.*?-->", stripped):
            flush()
        elif not stripped:
            flush()
        elif re.fullmatch(r"(?:\*\s*){3}|\*{3}|-{3,}", stripped):
            flush(); blocks.append(("break", "* * *"))
        elif stripped.startswith("# "):
            flush()
            heading = stripped[2:].strip()
            if re.fullmatch(r"chapter(?:\s+(?:\d+|[ivxlcdm]+|one|two|three|four|five|six|seven|eight|nine|ten))?", heading, re.I):
                continue
            if chapter_title is None:
                chapter_title = heading
            else:
                blocks.append(("subhead", heading))
        elif re.match(r"^#{2,6}\s+", stripped):
            flush()
            heading = re.sub(r"^#{2,6}\s+", "", stripped)
            if chapter_title is None:
                chapter_title = heading
            else:
                blocks.append(("subhead", heading))
        else:
            current.append(stripped)
    flush()
    return chapter_title, blocks


def inline_markup(text: str) -> str:
    value = html.escape(text, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", value)
    value = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"<i>\1</i>", value)
    return value


class ChapterMarker(Flowable):
    def __init__(self, chapter: str):
        super().__init__(); self.chapter = chapter; self.width = self.height = 0

    def draw(self):
        self.canv._novel_chapter = self.chapter
        self.canv._novel_chapter_open = True


class BackMatterMarker(Flowable):
    def __init__(self):
        super().__init__(); self.width = self.height = 0

    def draw(self):
        self.canv._novel_back_matter = True


class CoverImage(Flowable):
    def __init__(self, path: Path, width: float, height: float):
        super().__init__()
        self.path = path
        self.width = width
        self.height = height

    def wrap(self, available_width, available_height):
        return self.width, self.height

    def draw(self):
        self.canv.drawImage(str(self.path), 0, 0, width=self.width, height=self.height,
                            preserveAspectRatio=False, mask="auto")


class NovelDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, cfg: dict):
        self.cfg = cfg
        page = (float(cfg["trim_width_in"]) * inch, float(cfg["trim_height_in"]) * inch)
        super().__init__(filename, pagesize=page, leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
                         title=str(cfg["title"]), author=str(cfg["author"]))
        width, height = page
        inner, outer = float(cfg["inner_margin_in"]) * inch, float(cfg["outer_margin_in"]) * inch
        top, bottom = float(cfg["top_margin_in"]) * inch, float(cfg["bottom_margin_in"]) * inch
        odd = Frame(inner, bottom, width-inner-outer, height-top-bottom, id="odd")
        even = Frame(outer, bottom, width-inner-outer, height-top-bottom, id="even")
        templates = []
        if cfg.get("_cover_path"):
            cover = Frame(0, 0, width, height, id="cover", leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0)
            templates.append(PageTemplate(id="cover", frames=[cover], autoNextPageTemplate="even"))
        templates += [
            PageTemplate(id="odd", frames=[odd], onPageEnd=self.decorate, autoNextPageTemplate="even"),
            PageTemplate(id="even", frames=[even], onPageEnd=self.decorate, autoNextPageTemplate="odd"),
        ]
        self.addPageTemplates(templates)

    def decorate(self, canvas, doc):
        front_pages = 2 if self.cfg.get("_cover_path") else 1
        if doc.page <= front_pages or getattr(canvas, "_novel_back_matter", False):
            return
        cfg, width, height = self.cfg, *self.pagesize
        body_page = doc.page - front_pages
        canvas.saveState()
        canvas.setFillColor(black)
        canvas.setFont("Novel-Regular", 7.5)
        if cfg["running_heads"] and not getattr(canvas, "_novel_chapter_open", False):
            head = str(cfg["title"]) if body_page % 2 == 0 else getattr(canvas, "_novel_chapter", str(cfg["title"]))
            canvas.drawCentredString(width / 2, height - 0.43 * inch, head.upper())
        if cfg["page_numbers"]:
            canvas.drawCentredString(width / 2, 0.38 * inch, str(body_page))
        canvas.restoreState()
        canvas._novel_chapter_open = False


def register_fonts(cfg: dict):
    files = [("Novel-Regular", "font_regular"), ("Novel-Italic", "font_italic"),
             ("Novel-Bold", "font_bold"), ("Novel-BoldItalic", "font_bold_italic")]
    for name, key in files:
        path = Path(str(cfg[key])).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"font not found: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily("Novel", normal="Novel-Regular", bold="Novel-Bold",
                                  italic="Novel-Italic", boldItalic="Novel-BoldItalic")


def resolve_cover(project: Path, cfg: dict, warnings: list[str]) -> Path | None:
    value = str(cfg.get("cover_image", "")).strip()
    if not value:
        return None
    path = (project / value).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"cover image not found: {path}")
    reader = ImageReader(str(path))
    pixel_width, pixel_height = reader.getSize()
    trim_ratio = float(cfg["trim_width_in"]) / float(cfg["trim_height_in"])
    image_ratio = pixel_width / pixel_height
    if abs(image_ratio - trim_ratio) / trim_ratio > 0.01:
        raise ValueError(
            f"cover aspect ratio {pixel_width}:{pixel_height} does not match "
            f"trim size {cfg['trim_width_in']}:{cfg['trim_height_in']}"
        )
    effective_dpi = min(pixel_width / float(cfg["trim_width_in"]),
                        pixel_height / float(cfg["trim_height_in"]))
    if effective_dpi < 150:
        warnings.append(f"cover image resolution is only {effective_dpi:.0f} DPI at trim size")
    return path


def styles(cfg: dict):
    base = getSampleStyleSheet()
    size, leading = float(cfg["body_font_size"]), float(cfg["leading"])
    return {
        "title": ParagraphStyle("BookTitle", parent=base["Title"], fontName="Novel-Regular", fontSize=25,
                                leading=31, alignment=TA_CENTER, spaceAfter=16),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontName="Novel-Italic", fontSize=12,
                                   leading=16, alignment=TA_CENTER),
        "byline": ParagraphStyle("Byline", parent=base["Normal"], fontName="Novel-Regular", fontSize=11,
                                 leading=15, alignment=TA_CENTER),
        "edition": ParagraphStyle("Edition", parent=base["Normal"], fontName="Novel-Regular", fontSize=8,
                                  leading=11, alignment=TA_CENTER),
        "chapter": ParagraphStyle("Chapter", parent=base["Heading1"], fontName="Novel-Regular", fontSize=15,
                                  leading=20, alignment=TA_CENTER, spaceAfter=30),
        "body_first": ParagraphStyle("BodyFirst", parent=base["BodyText"], fontName="Novel-Regular", fontSize=size,
                                     leading=leading, alignment=0, firstLineIndent=0, spaceAfter=0,
                                     allowWidows=0, allowOrphans=0),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Novel-Regular", fontSize=size,
                               leading=leading, alignment=0, firstLineIndent=0.24*inch, spaceAfter=0,
                               allowWidows=0, allowOrphans=0),
        "subhead": ParagraphStyle("Subhead", parent=base["Heading2"], fontName="Novel-Bold", fontSize=size,
                                  leading=leading, alignment=TA_CENTER, spaceBefore=leading, spaceAfter=leading/2),
        "break": ParagraphStyle("Break", parent=base["Normal"], fontName="Novel-Regular", fontSize=9,
                                leading=leading*1.5, alignment=TA_CENTER, spaceBefore=leading/2, spaceAfter=leading/2),
        "back_matter": ParagraphStyle("BackMatter", parent=base["BodyText"], fontName="Novel-Regular",
                                      fontSize=size, leading=leading, alignment=0, firstLineIndent=0,
                                      spaceAfter=leading, allowWidows=0, allowOrphans=0),
    }


def build(project: Path, output: Path, allow_empty: bool) -> tuple[int, int, list[str]]:
    cfg = dict(DEFAULTS); cfg.update(read_simple_yaml(project / ".novel" / "publishing.yaml"))
    scenes, warnings = discover_scenes(project)
    if not scenes and not allow_empty:
        raise RuntimeError("no manuscript scene files found; use --allow-empty only to test the pipeline")
    cover_path = resolve_cover(project, cfg, warnings)
    cfg["_cover_path"] = str(cover_path) if cover_path else ""
    register_fonts(cfg); style = styles(cfg)
    chapters: OrderedDict[int, list[Path]] = OrderedDict()
    for i, scene in enumerate(scenes, 1):
        chapters.setdefault(chapter_number(scene, i), []).append(scene)

    story = []
    if cover_path:
        story += [CoverImage(cover_path, float(cfg["trim_width_in"]) * inch,
                             float(cfg["trim_height_in"]) * inch), PageBreak()]
    story += [Spacer(1, 1.65*inch), Paragraph(inline_markup(str(cfg["title"])), style["title"])]
    if cfg["subtitle"]:
        story += [Paragraph(inline_markup(str(cfg["subtitle"])), style["subtitle"]), Spacer(1, 0.7*inch)]
    else:
        story.append(Spacer(1, 0.7*inch))
    if cfg["author"]:
        story.append(Paragraph("by " + inline_markup(str(cfg["author"])), style["byline"]))
    story += [Spacer(1, 1.35*inch), Paragraph(inline_markup(str(cfg["edition"])), style["edition"]), PageBreak()]

    for chapter_i, (number, paths) in enumerate(chapters.items()):
        if chapter_i:
            story.append(PageBreak())
        parsed = [parse_scene(p) for p in paths]
        chapter_title = next((title for title, _ in parsed if title), None)
        label = f"{cfg['chapter_label']} {number}"
        if chapter_title and chapter_title.casefold() != label.casefold():
            label += f"<br/><font size='11'><i>{inline_markup(chapter_title)}</i></font>"
        story += [ChapterMarker(f"{cfg['chapter_label']} {number}"), Spacer(1, 1.1*inch), Paragraph(label, style["chapter"])]
        first = True
        for scene_i, (_, blocks) in enumerate(parsed):
            if scene_i and blocks:
                story.append(Paragraph("* * *", style["break"])); first = True
            for kind, content in blocks:
                if kind == "paragraph":
                    story.append(Paragraph(inline_markup(content), style["body_first"] if first else style["body"])); first = False
                elif kind == "subhead":
                    story.append(Paragraph(inline_markup(content), style["subhead"])); first = True
                else:
                    story.append(Paragraph("* * *", style["break"])); first = True

    back_matter_file = str(cfg.get("back_matter_file", "")).strip()
    if back_matter_file:
        back_matter_path = (project / back_matter_file).resolve()
        if not back_matter_path.is_file():
            raise FileNotFoundError(f"back matter file not found: {back_matter_path}")
        _, blocks = parse_scene(back_matter_path)
        if chapters:
            story.append(PageBreak())
        story += [BackMatterMarker(), Spacer(1, 1.1*inch)]
        back_matter_title = str(cfg.get("back_matter_title", "")).strip()
        if back_matter_title:
            story.append(Paragraph(inline_markup(back_matter_title), style["chapter"]))
        for kind, content in blocks:
            if kind == "paragraph":
                story.append(Paragraph(inline_markup(content), style["back_matter"]))
            elif kind == "subhead":
                story.append(Paragraph(inline_markup(content), style["subhead"]))
            else:
                story.append(Paragraph("* * *", style["break"]))

    output.parent.mkdir(parents=True, exist_ok=True)
    NovelDocTemplate(str(output), cfg).build(story)
    return len(scenes), len(chapters), warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args()
    project = args.project_root.resolve()
    cfg = dict(DEFAULTS); cfg.update(read_simple_yaml(project / ".novel" / "publishing.yaml"))
    output = (args.output or project / "output" / "pdf" / str(cfg["output_filename"])).resolve()
    try:
        scenes, chapters, warnings = build(project, output, args.allow_empty)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1
    print(f"PDF: {output}")
    print(f"Scenes: {scenes}")
    print(f"Chapters: {chapters}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if not scenes:
        print("WARNING: empty pipeline test; this is not a current-manuscript edition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
