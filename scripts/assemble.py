#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PARTIALS_DIR = ROOT / "output" / "partials"
OUTPUT_DIR = ROOT / "output"
SITE_CONFIG = ROOT / "output" / "site.json"

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
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
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


def load_config(config_path=None):
    path = Path(config_path) if config_path else SITE_CONFIG
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"title": "My Website", "sections": DEFAULT_SECTIONS}


def assemble(config_path=None):
    config = load_config(config_path)
    title = config.get("title", "My Website")
    sections = config.get("sections", DEFAULT_SECTIONS)
    output_file = OUTPUT_DIR / config.get("output", "index.html")

    included = []
    skipped = []
    parts = [HTML_HEAD.format(title=title)]

    for section in sections:
        partial = PARTIALS_DIR / f"{section}.html"
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
