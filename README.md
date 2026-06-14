# Bootstrap Website Generator — Agentic System

An agentic system that takes a plain English prompt and generates a complete, demo-ready Bootstrap 5 website. One command produces a fully assembled multi-page site with unique visual identity, real hero images, SEO meta tags, and a QA review report.

---

## Quick Start

```
/bootstrap_builder create a landing page for a yoga studio with an about page and a contact page
```

That single command runs the full pipeline: image sourcing → visual design research → content generation → HTML assembly → SEO meta → QA review.

After the build, you can optionally restyle the entire site:

```
read .claude/agents/restyle.md and run it with "Modern dark theme tech startup"
```

Or run a standalone QA check on an existing build:

```
read .claude/agents/review.md and run it
```

---

## Architecture

```
User Prompt
    │
    ▼
bootstrap_builder (orchestrator — .claude/commands/bootstrap_builder.md)
    │
    ├── Step 1:    Analyse prompt → extract brand, industry, tone
    │
    ├── Step 2:    Derive site slug → create SITE_DIR = output/[slug]/
    │              └── mkdir output/[slug]/partials/
    │
    ├── Step 3:    Decide sections + detect additional_pages list
    │
    ├── Step 4:    find-image skill → sources hero image from Unsplash
    │              └── writes [SITE_DIR]/image.json
    │
    ├── Step 5:    design-profile agent → researches industry design patterns
    │              └── writes [SITE_DIR]/design.json + [SITE_DIR]/custom.css
    │
    ├── Step 6:    custom-js skill → generates vanilla JS + scroll-to-top button
    │              └── writes [SITE_DIR]/custom.js + [SITE_DIR]/partials/scroll-top-btn.html
    │
    ├── Step 7-9:  Content planning → generates all HTML section partials
    │              └── writes [SITE_DIR]/partials/[section].html
    │
    ├── Step 10:   python scripts/assemble.py [SITE_DIR]/site.json
    │              └── writes [SITE_DIR]/index.html
    │
    ├── Step 11:   seo-meta skill → writes meta tags for all pages
    │              └── writes [SITE_DIR]/site-meta.json, re-assembles all HTML
    │
    ├── Step 12:   page-builder agent (one per additional page requested)
    │              └── writes [SITE_DIR]/[page].html
    │
    ├── Step 13:   review agent → audits all assembled HTML
    │              └── outputs PASS/WARN/FAIL report, auto-fixes simple issues
    │
    └── Step 14:   Report to user (including SITE_DIR folder path)
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| CSS framework | Bootstrap 5.3.8 (CDN) |
| Icons | Font Awesome 6.5 (CDN) |
| Fonts | Google Fonts (via `@import` in `custom.css`) |
| Assembly | Python 3 (`scripts/assemble.py`) |
| Images | Unsplash (direct URLs preferred, source.unsplash.com fallback) |

---

## Directory Structure

```
bootstrap_skills_and_agents/
│
├── .claude/
│   ├── commands/               # Skills (Claude Code slash commands)
│   │   ├── bootstrap_builder.md    ← Main orchestrator
│   │   ├── navbar.md
│   │   ├── hero.md
│   │   ├── features.md
│   │   ├── testimonials.md
│   │   ├── pricing.md
│   │   ├── faq.md
│   │   ├── team.md
│   │   ├── contact-form.md
│   │   ├── cta.md
│   │   ├── footer.md
│   │   ├── custom-css.md
│   │   ├── custom-js.md
│   │   ├── find-image.md
│   │   └── seo-meta.md
│   │
│   └── agents/                 # Multi-step agents (invoked by orchestrator)
│       ├── design-profile.md       ← Industry design research
│       ├── page-builder.md         ← Additional page generator
│       ├── review.md               ← QA / consistency auditor
│       └── restyle.md              ← Visual theme overhaul
│
├── scripts/
│   └── assemble.py             # Stitches partials into complete HTML pages
│
└── output/                     # One subfolder per generated site
    └── [site-slug]/            ← Named from brand (e.g. serenity-flow)
        ├── index.html          ← Assembled landing page
        ├── about.html          ← Additional page (if requested)
        ├── contact.html        ← Additional page (if requested)
        ├── custom.css          ← Brand fonts + color overrides
        ├── custom.js           ← Smooth scroll, scroll spy, form handler
        ├── site.json           ← Landing page config (title + section order)
        ├── site-meta.json      ← SEO meta tags for all pages
        ├── about-site.json     ← Additional page config
        ├── design.json         ← Color + font profile from design-profile agent
        ├── image.json          ← Hero image URL from find-image skill
        └── partials/           ← Individual section HTML files
            ├── navbar.html
            ├── hero.html
            ├── features.html
            ├── testimonials.html
            ├── pricing.html
            ├── faq.html
            ├── team.html
            ├── contact-form.html
            ├── cta.html
            ├── footer.html
            ├── scroll-top-btn.html
            ├── about-navbar.html   ← Page-prefixed partials for additional pages
            ├── about-hero.html
            └── ...
```

---

## Skills (Slash Commands)

Skills live in `.claude/commands/`. Each skill has one job: generate one Bootstrap 5 component and write it to `output/partials/`.

| Skill | What it generates | Output file |
|-------|------------------|-------------|
| `/bootstrap_builder` | Runs the full pipeline (orchestrator) | All output files |
| `/navbar` | Sticky navbar with hamburger toggle | `partials/navbar.html` |
| `/hero` | Hero section (split or centered) | `partials/hero.html` |
| `/features` | Feature cards grid | `partials/features.html` |
| `/testimonials` | Testimonial cards or carousel | `partials/testimonials.html` |
| `/pricing` | Three-tier pricing cards | `partials/pricing.html` |
| `/faq` | Bootstrap accordion | `partials/faq.html` |
| `/team` | Team member cards | `partials/team.html` |
| `/contact-form` | Contact form (simple or split) | `partials/contact-form.html` |
| `/cta` | Call-to-action band | `partials/cta.html` |
| `/footer` | Footer with columns + social links | `partials/footer.html` |
| `/custom-css` | Brand fonts + Bootstrap overrides | `custom.css` |
| `/custom-js` | Smooth scroll, scroll spy, scroll-to-top | `custom.js` |
| `/find-image` | Sources hero image from Unsplash | `image.json` |
| `/seo-meta` | Meta description + Open Graph tags | `site-meta.json` |

### Section Decision Matrix

The orchestrator uses this matrix to decide which sections to include:

| Section | Include when |
|---------|-------------|
| navbar | ALWAYS |
| hero | ALWAYS |
| features | Product/service has distinct benefits to showcase |
| testimonials | Social proof would help conversions (most sites) |
| pricing | Site sells something with multiple tiers |
| faq | Complex product/service that generates questions |
| team | Agency, studio, consultancy, or personal brand |
| contact-form | Users need a way to reach out directly |
| cta | ALWAYS — placed just before footer |
| footer | ALWAYS |
| scroll-top-btn | ALWAYS |

---

## Agents

Agents live in `.claude/agents/`. Unlike skills (one output, deterministic), agents are multi-step and do research or validation before writing files.

### `design-profile` — Visual Identity Research
Runs automatically during every `bootstrap_builder` build. Searches the web for real industry design patterns, visits a competitor site, and synthesizes a unique color + font profile. Ensures no two sites look the same.

**Outputs:** `output/design.json`, `output/custom.css`

**Rules:**
- Never defaults to Bootstrap blue (`#0d6efd`)
- Primary color must pass WCAG AA contrast (≥ 4.5:1)
- Font pairing must be available on Google Fonts

### `page-builder` — Additional Page Generator
Invoked by `bootstrap_builder` once per requested additional page. Reads `design.json` for the brand's visual profile, selects appropriate sections from a decision matrix, and produces a complete assembled HTML page that links correctly to all other pages in the site.

**Shared sections** (reused from landing page, not regenerated): `footer`, `scroll-top-btn`, `team`, `testimonials`, `pricing`, `faq`, `contact-form`

**Page-specific sections** (prefixed, e.g. `about-hero`): navbar, hero, story content, values, CTA

| Page type | Generates | Reuses |
|-----------|-----------|--------|
| about | navbar, hero, story, values, cta | team, footer |
| contact | navbar, hero, cta | contact-form, faq, footer |
| services | navbar, hero, services, cta | pricing, testimonials, footer |
| gallery | navbar, hero, gallery grid, cta | footer |
| blog | navbar, hero, posts grid, cta | footer |

### `review` — QA Auditor
Runs at the end of every `bootstrap_builder` build. Reads all assembled HTML files and runs 10 checks. Auto-fixes simple issues; reports everything else with specific file + line context.

**Checks:**
| Check | What it verifies |
|-------|-----------------|
| A | All `href="#id"` anchor targets exist in the same file |
| B | All `href="page.html"` cross-page links point to existing files |
| C | Brand name is consistent across all pages (title, navbar, footer) |
| D | Every page has a navbar linking to all other pages |
| E | Contact forms have a non-empty `action` attribute |
| F | Hero image is a real URL (not `placehold.co`) |
| G | No placeholder copy leaked (`[brand name]`, `@example.com`, etc.) |
| H | `custom.css` font names match `design.json` |
| I | No duplicate Bootstrap accordion IDs on any single page |
| J | Copyright year in footer matches current year |

**Auto-fixes:** Check H (font mismatch), Check J (outdated year)

### `restyle` — Visual Theme Overhaul
Run manually post-build to completely change the site's visual language. Takes a plain English style descriptor and rewrites `custom.css` comprehensively, edits Bootstrap structural classes in partials where needed, and re-assembles all pages.

**Example prompts:**
```
read .claude/agents/restyle.md and run it with "Modern dark theme tech startup"
read .claude/agents/restyle.md and run it with "Luxury spa minimalist"
read .claude/agents/restyle.md and run it with "Bold energetic fitness brand"
read .claude/agents/restyle.md and run it with "Warm earthy organic cafe"
read .claude/agents/restyle.md and run it with "Retro brutalist editorial"
```

Goes beyond color/font changes — controls button shape (pill vs sharp), card style (glassmorphism vs flat vs bordered), section backgrounds, navbar style, hero backgrounds, hover animations, and spacing density.

---

## Assembly Script

`scripts/assemble.py` is pure Python — no LLM tokens. It:

1. Reads a site config JSON — the config path determines the output folder (site_dir = config's parent directory)
2. Reads `[site_dir]/site-meta.json` and injects SEO meta tags into `<head>` if present
3. Loops through the sections list, reads each partial from `[site_dir]/partials/`
4. Wraps everything in a Bootstrap 5.3.8 HTML shell with CDN links
5. Writes the final HTML file to `[site_dir]/`

```bash
# Assemble a site's landing page
python scripts/assemble.py output/serenity-flow/site.json

# Assemble an additional page
python scripts/assemble.py output/serenity-flow/about-site.json
```

### Site Config Format

**`output/[slug]/site.json`** (landing page):
```json
{
  "title": "Serenity Flow Yoga Studio",
  "sections": ["navbar", "hero", "features", "testimonials", "pricing", "faq", "team", "contact-form", "cta", "footer", "scroll-top-btn"]
}
```

**`output/[slug]/about-site.json`** (additional page):
```json
{
  "title": "About Us | Serenity Flow Yoga Studio",
  "output": "about.html",
  "sections": ["about-navbar", "about-hero", "about-story", "about-values", "team", "about-cta", "footer", "scroll-top-btn"]
}
```

### SEO Meta Format

**`output/[slug]/site-meta.json`**:
```json
{
  "index.html": {
    "description": "Serenity Flow is Springfield's premier yoga studio...",
    "og_title": "Serenity Flow Yoga Studio",
    "og_description": "...",
    "og_image": "https://images.unsplash.com/photo-...",
    "og_type": "website",
    "twitter_card": "summary_large_image",
    "canonical": "https://example.com/index.html"
  },
  "about.html": { ... }
}
```

---

## Design Principles

- **Hyper-specific skills**: each skill generates one Bootstrap component. Narrow scope = low token cost per skill.
- **Scripts for mechanical work**: HTML assembly, meta injection, and file management are pure Python — zero LLM tokens.
- **Agents for research and validation**: design research, additional page generation, and QA review require multi-step reasoning and are handled by agents, not skills.
- **Unique visual identity per build**: the `design-profile` agent researches real industry websites before picking colors and fonts. Every build looks different.
- **Shared partials across pages**: `footer`, `team`, `faq`, and other sections are generated once and reused across all pages. Consistency is structural, not copied.
- **Additive pipeline**: each step (`find-image` → `design-profile` → `seo-meta` → `review`) adds value without requiring the previous step to be rebuilt. Run them independently post-build.

---

## Post-Build Commands

These can be run on any existing build without rebuilding from scratch. Replace `output/serenity-flow` with the actual site folder name.

| Command | What it does |
|---------|-------------|
| `/seo-meta` | Generate / regenerate SEO meta tags |
| read `review.md` and run with SITE_DIR `output/serenity-flow` | Run QA audit on a site |
| read `restyle.md` and run with prompt | Overhaul the visual theme |
| `python scripts/assemble.py output/serenity-flow/site.json` | Re-assemble landing page |
| `python scripts/assemble.py output/serenity-flow/about-site.json` | Re-assemble a specific page |

---

## Workflow

1. **Prompt** — describe the site in plain English, optionally request additional pages
2. **Build** — `bootstrap_builder` runs the full 12-step pipeline automatically
3. **Review** — QA report identifies any issues; simple ones are auto-fixed
4. **Refine** — edit individual partials and re-run `assemble.py`, or use `restyle` for a full visual overhaul
5. **Deploy** — copy the `output/` folder to any static host (Netlify, GitHub Pages, etc.)
