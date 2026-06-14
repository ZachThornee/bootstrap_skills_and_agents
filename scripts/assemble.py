#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

DEFAULT_SECTIONS = [
    "navbar", "hero", "features", "testimonials",
    "pricing", "faq", "team", "contact-form", "cta", "footer"
]

HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{meta_block}  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="custom.css">
</head>
<body>
"""

HTML_FOOT = """
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
  <script src="custom.js"></script>
</body>
</html>
"""


def load_meta(output_filename, site_meta_path):
    if not site_meta_path.exists():
        return ""
    with open(site_meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    page_meta = meta.get(output_filename, {})
    if not page_meta:
        return ""
    lines = []
    if page_meta.get("description"):
        lines.append(f'  <meta name="description" content="{page_meta["description"]}">')
    if page_meta.get("canonical"):
        lines.append(f'  <link rel="canonical" href="{page_meta["canonical"]}">')
    if page_meta.get("og_title"):
        lines.append(f'  <meta property="og:title" content="{page_meta["og_title"]}">')
    if page_meta.get("og_description"):
        lines.append(f'  <meta property="og:description" content="{page_meta["og_description"]}">')
    if page_meta.get("og_image"):
        lines.append(f'  <meta property="og:image" content="{page_meta["og_image"]}">')
    if page_meta.get("og_type"):
        lines.append(f'  <meta property="og:type" content="{page_meta["og_type"]}">')
    if page_meta.get("twitter_card"):
        lines.append(f'  <meta name="twitter:card" content="{page_meta["twitter_card"]}">')
    if page_meta.get("og_title"):
        lines.append(f'  <meta name="twitter:title" content="{page_meta["og_title"]}">')
    if page_meta.get("og_description"):
        lines.append(f'  <meta name="twitter:description" content="{page_meta["og_description"]}">')
    if page_meta.get("og_image"):
        lines.append(f'  <meta name="twitter:image" content="{page_meta["og_image"]}">')
    return "\n".join(lines) + "\n" if lines else ""


def resolve_site_dir(config_path):
    """Infer site_dir from the config file's parent directory.

    When no config_path is given, reads output/.last-build for the most
    recent site slug. Falls back to output/ if that file doesn't exist.
    """
    if config_path:
        p = Path(config_path)
        if not p.is_absolute():
            p = ROOT / p
        return p.parent

    last_build = ROOT / "output" / ".last-build"
    if last_build.exists():
        slug = last_build.read_text(encoding="utf-8").strip()
        site_dir = ROOT / "output" / slug
        if (site_dir / "site.json").exists():
            print(f"(Using last build: output/{slug}/)")
            return site_dir
        print(f"Warning: last build '{slug}' has no site.json, falling back to output/")

    legacy = ROOT / "output"
    if not (legacy / "site.json").exists():
        print(
            "Error: no config found.\n"
            "Usage:  python scripts/assemble.py output/[slug]/site.json\n"
            "        python scripts/assemble.py output/[slug]/about-site.json",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return legacy


def load_config(config_path, site_dir):
    p = Path(config_path) if config_path else site_dir / "site.json"
    if not p.is_absolute():
        p = ROOT / p
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"title": "My Website", "sections": DEFAULT_SECTIONS}


def assemble(config_path=None):
    site_dir = resolve_site_dir(config_path)
    partials_dir = site_dir / "partials"
    site_meta_path = site_dir / "site-meta.json"

    config = load_config(config_path, site_dir)
    title = config.get("title", "My Website")
    sections = config.get("sections", DEFAULT_SECTIONS)
    output_filename = config.get("output", "index.html")
    output_file = site_dir / output_filename

    included = []
    skipped = []
    meta_block = load_meta(output_filename, site_meta_path)
    parts = [HTML_HEAD.format(title=title, meta_block=meta_block)]

    for section in sections:
        partial = partials_dir / f"{section}.html"
        if partial.exists():
            parts.append(f"\n<!-- {section} -->\n")
            parts.append(partial.read_text(encoding="utf-8"))
            included.append(section)
        else:
            skipped.append(section)

    parts.append(HTML_FOOT)

    output_file.write_text("".join(parts), encoding="utf-8")

    print(f"Assembled -> {output_file}")
    print(f"  Title:    {title}")
    print(f"  Sections: {' > '.join(included)}")
    if skipped:
        print(f"  Skipped:  {', '.join(skipped)} (no partial found)")


if __name__ == "__main__":
    try:
        assemble(sys.argv[1] if len(sys.argv) > 1 else None)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
