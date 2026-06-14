# Bootstrap Website Generator — Agentic System

An agentic system that takes a plain English prompt and generates a complete, demo-ready Bootstrap 5 website. One command produces a fully assembled multi-page site with unique visual identity, real hero images, SEO meta tags, and a QA review report.

---

## Quick Start

`/bootstrap_builder` is the single entry point for everything. It detects your intent automatically and routes to the right operation.

### Generate a new site

```
/bootstrap_builder create a landing page for a yoga studio with an about page and a contact page
```

```
/bootstrap_builder build a portfolio site for a freelance developer named Jane Smith with a portfolio page
```

```
/bootstrap_builder make a SaaS landing page for a project management tool called TaskFlow, include a pricing page
```

Runs the full 14-step pipeline:

```
image sourcing → design research → content planning → HTML generation
→ assembly → additional pages → SEO meta → QA review
```

The site is written to `output/[site-slug]/` (e.g. `output/jane-smith/`). Every build writes `output/.last-build` so subsequent commands auto-discover the site.

---

### Restyle an existing site

Use any of these trigger phrases and `/bootstrap_builder` will route to the restyle agent automatically:

```
/bootstrap_builder restyle with "Tron vibes, dark, technological and slick"
```

```
/bootstrap_builder make it look more minimal and clean
```

```
/bootstrap_builder change the theme to bold energetic fitness brand
```

```
/bootstrap_builder update the style to warm earthy organic cafe
```

```
/bootstrap_builder new look — retro brutalist editorial
```

Without a site name, restyle targets the most recent build (via `output/.last-build`). To target a specific older site, name it:

```
/bootstrap_builder restyle serenity-flow with "Luxury spa minimalist"
```

**Trigger words** (any of these route to restyle): `restyle`, `re-style`, `change the style`, `change the theme`, `change the design`, `make it look`, `make it more`, `update the design`, `update the style`, `update the theme`, `new theme`, `new style`, `new look`

Restyle goes well beyond swapping colors — it controls fonts, button shape, card style (glassmorphism vs flat vs bordered), navbar appearance, hero backgrounds, section alternation, hover animations, and spacing density. It rewrites `custom.css` comprehensively and edits Bootstrap utility classes directly in partials where CSS alone can't achieve the effect.

---

### 3. QA review

```
read .claude/agents/review.md and run it
```

Runs 10 checks across all assembled HTML files: broken anchor links, missing cross-page links, brand name consistency, navbar completeness, contact form action, hero image quality, placeholder leakage, font consistency, accordion ID collisions, and copyright year. Auto-fixes copyright year and font mismatches; reports everything else with specific file and line context.

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
    │              ├── Collision check: if output/[slug]/ already has content,
    │              │   append -2, -3, etc. and inform the user
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
    ├── Step 11:   page-builder agent (one per additional page requested)
    │              └── writes [SITE_DIR]/[page].html
    │              └── updates landing page navbar to link all pages, re-assembles index.html
    │
    ├── Step 12:   seo-meta skill → runs AFTER all pages exist
    │              └── writes [SITE_DIR]/site-meta.json, re-assembles all HTML
    │
    ├── Step 13:   review agent → audits all assembled HTML
    │              └── outputs PASS/WARN/FAIL report, auto-fixes simple issues
    │
    └── Step 14:   Writes output/.last-build → reports to user
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| CSS framework | Bootstrap 5.3.8 (CDN) |
| Icons | Font Awesome 6.5 (CDN) |
| Fonts | Google Fonts (via `@import` in `custom.css`) |
| Assembly | Python 3 (`scripts/assemble.py`) |
| Images | Unsplash (direct URLs preferred, source.unsplash.com fallback) |
| Forms | Formspree (placeholder — replace `YOUR_FORM_ID` before deploying) |

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
    ├── .last-build             ← Slug of most recent build (auto-written at Step 14)
    ├── serenity-flow/          ← Example: yoga studio build
    └── mark-twinjamin/         ← Example: freelance developer + portfolio page
        ├── index.html          ← Assembled landing page
        ├── portfolio.html      ← Additional page (if requested)
        ├── custom.css          ← Brand fonts + color overrides (rewritten by restyle)
        ├── custom.js           ← Smooth scroll, scroll spy, form handler
        ├── site.json           ← Landing page config (title + section order)
        ├── site-meta.json      ← SEO meta tags for all pages
        ├── portfolio-site.json ← Additional page config
        ├── design.json         ← Color + font profile (updated by restyle)
        ├── image.json          ← Hero image URL from find-image skill
        └── partials/           ← Individual section HTML files
            ├── navbar.html
            ├── hero.html
            ├── features.html
            ├── testimonials.html
            ├── faq.html
            ├── contact-form.html
            ├── cta.html
            ├── footer.html
            ├── scroll-top-btn.html
            ├── portfolio-navbar.html   ← Page-prefixed partials for additional pages
            ├── portfolio-hero.html
            ├── portfolio-projects.html
            └── ...
```

---

## Skills (Slash Commands)

Skills live in `.claude/commands/`. Each skill has one job: generate one Bootstrap 5 component and write it to `[SITE_DIR]/partials/`. All skills accept a `SITE_DIR` parameter — defaults to `output/` when run standalone.

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

**Outputs:** `[SITE_DIR]/design.json`, `[SITE_DIR]/custom.css`

**Rules:**
- Never defaults to Bootstrap blue (`#0d6efd`)
- Primary color must pass WCAG AA contrast (≥ 4.5:1)
- Font pairing must be available on Google Fonts

### `page-builder` — Additional Page Generator

Invoked by `bootstrap_builder` once per requested additional page. Reads `design.json` for the brand's visual profile, selects appropriate sections from a decision matrix, and produces a complete assembled HTML page that links correctly to all other pages in the site.

**Shared sections** (reused from landing page, not regenerated): `footer`, `scroll-top-btn`, `team`, `testimonials`, `pricing`, `faq`, `contact-form`

**Page-specific sections** (prefixed, e.g. `portfolio-hero`): navbar, hero, page content, CTA

| Page type | Generates | Reuses |
|-----------|-----------|--------|
| about | navbar, hero, story, values, cta | team, footer |
| contact | navbar, hero, cta | contact-form, faq, footer |
| services | navbar, hero, services, cta | pricing, testimonials, footer |
| gallery | navbar, hero, gallery grid, cta | footer |
| blog | navbar, hero, posts grid, cta | footer |
| portfolio | navbar, hero, projects grid, skills, cta | footer |

For page types not in the table, the agent uses judgement — always includes a navbar, hero, relevant content, CTA, and reuses footer and scroll-top-btn.

### `review` — QA Auditor

Runs at the end of every `bootstrap_builder` build. Reads all assembled HTML files and runs 10 checks. Auto-fixes simple issues; reports everything else with specific file + line context.

**Checks:**

| Check | What it verifies |
|-------|-----------------|
| A | All `href="#id"` anchor targets exist in the same file |
| B | All `href="page.html"` cross-page links point to existing files |
| C | Brand name is consistent across all pages (title, navbar, footer) |
| D | Every page has a navbar linking to all other pages |
| E | Contact forms have a real `action` URL (WARN if Formspree placeholder, FAIL if missing) |
| F | Hero image is a real URL (not `placehold.co`) |
| G | No placeholder copy leaked (`[brand name]`, `@example.com`, etc.) |
| H | `custom.css` font names match `design.json` |
| I | No duplicate Bootstrap accordion IDs on any single page |
| J | Copyright year in footer matches current year |

**Auto-fixes:** Check H (font mismatch), Check J (outdated copyright year)

### `restyle` — Visual Theme Overhaul

Run manually post-build to completely change the site's visual language. Takes a plain English style descriptor, rewrites `custom.css` comprehensively, edits Bootstrap utility classes in partials where CSS alone can't achieve the effect, and re-assembles all pages.

**How to run:**

```
read .claude/agents/restyle.md and run it with "Tron vibes, dark, technological and slick"
```

Auto-discovers the most recent build via `output/.last-build`. All pages are re-assembled automatically.

**What restyle controls:**

| Axis | Examples |
|------|---------|
| Color scheme | Primary, background, surface, border, muted text |
| Typography | Google Font pairing — heading + body |
| Button shape | Sharp corners (tech) / pill (luxury) / default |
| Card style | Glassmorphism / flat / thin border / brutalist |
| Section backgrounds | Dark throughout / light/white alternation / brand color |
| Navbar | Transparent + blur / solid / bordered |
| Hero | CSS gradient + grid overlay / image-only / full-bleed |
| Animations | Hover glow / lift / none |

**Example style prompts:**

```
read .claude/agents/restyle.md and run it with "Tron vibes, dark, technological and slick"
read .claude/agents/restyle.md and run it with "Modern dark theme tech startup"
read .claude/agents/restyle.md and run it with "Luxury spa minimalist"
read .claude/agents/restyle.md and run it with "Bold energetic fitness brand"
read .claude/agents/restyle.md and run it with "Warm earthy organic cafe"
read .claude/agents/restyle.md and run it with "Retro brutalist editorial"
```

---

## Assembly Script

`scripts/assemble.py` is pure Python — no LLM tokens. It:

1. Reads a site config JSON — the config path determines the output folder (`site_dir` = config's parent directory)
2. Reads `[site_dir]/site-meta.json` and injects SEO meta tags into `<head>` if present
3. Loops through the sections list, reads each partial from `[site_dir]/partials/`
4. Wraps everything in a Bootstrap 5.3.8 HTML shell with CDN links
5. Writes the final HTML file to `[site_dir]/`

```bash
# Assemble a specific site's landing page
python scripts/assemble.py output/mark-twinjamin/site.json

# Assemble an additional page
python scripts/assemble.py output/mark-twinjamin/portfolio-site.json

# Assemble the most recent build's landing page (reads output/.last-build automatically)
python scripts/assemble.py
```

### Site Config Format

**`output/[slug]/site.json`** (landing page):
```json
{
  "title": "Mark Twinjamin - Freelance Developer",
  "sections": ["navbar", "hero", "features", "testimonials", "faq", "contact-form", "cta", "footer", "scroll-top-btn"]
}
```

**`output/[slug]/portfolio-site.json`** (additional page):
```json
{
  "title": "Portfolio | Mark Twinjamin",
  "output": "portfolio.html",
  "sections": ["portfolio-navbar", "portfolio-hero", "portfolio-projects", "portfolio-skills", "portfolio-cta", "footer", "scroll-top-btn"]
}
```

### SEO Meta Format

**`output/[slug]/site-meta.json`**:
```json
{
  "index.html": {
    "description": "Mark Twinjamin is a freelance full-stack developer...",
    "og_title": "Mark Twinjamin - Freelance Developer",
    "og_description": "...",
    "og_image": "https://images.unsplash.com/photo-...",
    "og_type": "website",
    "twitter_card": "summary_large_image",
    "canonical": "https://example.com/index.html"
  },
  "portfolio.html": { ... }
}
```

---

## Per-Site Isolation

Every build lives in its own subfolder under `output/`. This means:

- Multiple sites can coexist without overwriting each other
- Running `/bootstrap_builder` twice for the same brand name will detect the collision and append `-2`, `-3`, etc.
- `output/.last-build` always contains the slug of the most recent build — `review` and `restyle` read this automatically so you never have to type the folder path

---

## Design Principles

- **Hyper-specific skills**: each skill generates one Bootstrap component. Narrow scope = low token cost per skill.
- **Scripts for mechanical work**: HTML assembly, meta injection, and file management are pure Python — zero LLM tokens.
- **Agents for research and validation**: design research, additional page generation, and QA review require multi-step reasoning and are handled by agents, not skills.
- **Unique visual identity per build**: the `design-profile` agent researches real industry websites before picking colors and fonts. Every build looks different.
- **Restyle without rebuilding**: `restyle` operates on the existing partials. You never have to regenerate content to change the look — just run it with a new style prompt.
- **Shared partials across pages**: `footer`, `team`, `faq`, and other sections are generated once and reused across all pages. Consistency is structural, not copied.
- **SEO meta runs last**: `seo-meta` runs at Step 12 — after all pages (including additional pages from `page-builder`) exist. Every page gets meta tags in the same pass.

---

## Post-Build Commands

`review` and `restyle` auto-discover the most recent build via `output/.last-build` — no need to specify the folder.

| Command | What it does |
|---------|-------------|
| `/bootstrap_builder restyle with "Dark tech"` | Restyle the last build |
| `/bootstrap_builder restyle serenity-flow with "Dark tech"` | Restyle a specific older build |
| `read .claude/agents/review.md and run it` | QA audit the last build |
| `python scripts/assemble.py` | Re-assemble the last build's landing page |
| `python scripts/assemble.py output/[slug]/[page]-site.json` | Re-assemble a specific page |
| `/seo-meta` | Regenerate SEO meta tags for the last build |

---

## Workflow

1. **Prompt** — describe the site in plain English; mention any additional pages you want
2. **Build** — `/bootstrap_builder` runs the full 14-step pipeline and writes `output/.last-build`
3. **Restyle** (optional) — run `restyle` with a style descriptor to overhaul the visual identity
4. **Review** — the QA report runs automatically at the end of every build; re-run it any time
5. **Refine** — edit individual partials and re-run `assemble.py` to pick up changes
6. **Deploy** — copy the `output/[site-slug]/` folder to any static host (Netlify, GitHub Pages, etc.)
   - Before deploying: replace `YOUR_FORM_ID` in `partials/contact-form.html` with a real Formspree ID
   - Before deploying: update `canonical` URLs in `site-meta.json` from `https://example.com` to your real domain
