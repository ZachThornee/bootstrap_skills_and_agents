You are a Bootstrap 5 website orchestrator. You handle two operations: generating a new site from scratch, and restyling an existing site. Detect which operation the user wants in Step 0, then follow the appropriate path.

## Input
$ARGUMENTS — either a natural language description of a new website, or a restyle instruction for an existing one.

---

## Step 0 — Detect intent

Scan $ARGUMENTS for any of these explicit restyle trigger words or phrases (case-insensitive):
- `restyle`, `re-style`
- `change the style`, `change the theme`, `change the design`
- `make it look`, `make it more`
- `update the design`, `update the style`, `update the theme`
- `new theme`, `new style`, `new look`

**If a trigger is found → RESTYLE PATH:**

Extract:
- `style_descriptor`: everything in $ARGUMENTS that describes the desired look (e.g. "dark brutalist", "warm earthy organic"). Strip the trigger phrase itself — only keep the description.
- `target_slug`: if $ARGUMENTS names a specific site (e.g. "restyle mark-twinjamin", "change the style of serenity-flow"), extract that slug. Otherwise leave blank.

Then:
1. If `target_slug` is blank, read `output/.last-build` to get the most recent site slug.
2. Set `SITE_DIR = output/[slug]`.
3. Confirm to the user: "Restyling `[SITE_DIR]` with: *[style_descriptor]*"
4. Read `.claude/agents/restyle.md` and execute it with `SITE_DIR` set to `[SITE_DIR]` and the `style_descriptor` as the style prompt.
5. Stop — do not proceed to Step 1.

**If no trigger is found → GENERATE PATH:**

Continue to Step 1 and run the full 14-step generation pipeline.

---

## Step 1 — Analyse the prompt

Extract the following from $ARGUMENTS:
- `brand`: business or site name (infer if not stated)
- `tagline`: one-line description of what they do
- `industry`: type of business (SaaS, restaurant, agency, portfolio, e-commerce, etc.)
- `tone`: professional / casual / bold / friendly / minimal (infer from context)
- `primary_color`: hex color if mentioned, otherwise pick one appropriate for the industry
- `font`: Google Font appropriate for the tone (default: Inter)

---

## Step 2 — Establish SITE_DIR

Derive a site slug from the brand name. This slug becomes the output folder name.

**Slug rules:**
1. If $ARGUMENTS contains an explicit folder name (e.g. "save as my-project", "name the folder cool-brand", "folder name my-site"), use that value exactly as the slug.
2. Otherwise, slugify the brand name: lowercase all letters, replace spaces and special characters with hyphens, strip common filler words ("a", "an", "the", "landing", "page", "website", "for"), collapse multiple hyphens, trim to 40 characters.

**Examples:**
- "Serenity Flow Yoga Studio" → `serenity-flow-yoga-studio`
- "The Oak & Barrel Gastropub" → `oak-barrel-gastropub`
- "Sunshine Steps Daycare" → `sunshine-steps-daycare`
- "TechLaunch SaaS" → `techlaunch-saas`

**Collision check:** Before creating the directory, check whether `output/[slug]/` already has content from a previous build:
```
python -c "from pathlib import Path; p = Path('output/[slug]'); print('EXISTS' if p.exists() and any(p.iterdir()) else 'CLEAR')"
```
If the output is `EXISTS`, increment a numeric suffix until you find an unused folder (`[slug]-2`, `[slug]-3`, etc.) and use that as the final slug. Inform the user: "A previous build already exists at `output/[slug]/`. Using `output/[slug]-2/` instead." Update `SITE_DIR` to the new value before proceeding.

Set `SITE_DIR = output/[slug]` (or the suffixed version if a collision was found) and use this variable for every file path in all subsequent steps.

Create the required directories using the Bash tool:
```
python -c "from pathlib import Path; Path('output/[slug]/partials').mkdir(parents=True, exist_ok=True); print('Created output/[slug]/partials')"
```

---

## Step 3 — Decide which sections to include

Use this decision matrix. Be selective — a focused 5-6 section site is better than a bloated one:

| Section       | Include when |
|---------------|-------------|
| navbar        | ALWAYS |
| hero          | ALWAYS |
| features      | Product or service has distinct benefits to showcase |
| testimonials  | Social proof would help conversions (most sites) |
| pricing       | Site sells something with multiple tiers |
| faq           | Complex product/service that generates questions |
| team          | Agency, startup, consultancy, or personal brand |
| contact-form  | Users need a way to reach out directly |
| cta           | ALWAYS (place just before footer) |
| footer        | ALWAYS |
| scroll-top-btn| ALWAYS |

Decide the section order. Standard order: navbar → hero → features → testimonials → pricing → faq → team → contact-form → cta → footer → scroll-top-btn

Also scan $ARGUMENTS for any additional pages the user wants beyond the landing page. Common signals: "with an about page", "include a contact page", "also make a services page". Extract these as:
- `additional_pages`: list of page types requested (e.g. `["about", "contact", "services"]`)

If no additional pages are mentioned, `additional_pages` is empty and this is a single-page site.

---

## Step 4 — Source the hero image

Before building content, find a relevant image for the hero section.

Check $ARGUMENTS for a user-provided image URL or file path first. If found, use it directly.

If no image is provided, extract 2-3 image keywords from the prompt (e.g. "personal trainer fitness", "coffee shop interior", "SaaS team working") and run the `/find-image` skill by reading `.claude/commands/find-image.md` and executing it with those keywords and `SITE_DIR` set to `[SITE_DIR]`.

After the skill runs, read `[SITE_DIR]/image.json` to get the `hero_image` URL and `alt` text. Use these in the hero partial in Step 8. If `[SITE_DIR]/image.json` does not exist or the URL is empty, fall back to:
`https://source.unsplash.com/800x500/?[keywords-joined-by-plus]`

---

## Step 5 — Run the design profile agent

Before writing any HTML, establish the visual identity for the site.

Check $ARGUMENTS for explicit color or font preferences. If the user has specified colors or fonts, skip this step and use them directly when generating `[SITE_DIR]/custom.css` later.

If no design preferences are given, invoke the design profile agent by reading `.claude/agents/design-profile.md` and executing it with:
- `industry`: the industry extracted in Step 1
- `tone`: the tone extracted in Step 1
- `brand`: the brand name extracted in Step 1
- `SITE_DIR`: `[SITE_DIR]`

The agent will write `[SITE_DIR]/design.json` and `[SITE_DIR]/custom.css`. After it completes, read `[SITE_DIR]/design.json` to confirm the primary color, fonts, and vibe. Use the vibe and tone to inform the copy written in Step 7 — a "playful" vibe should produce warmer, more energetic copy than a "minimal" vibe.

---

## Step 6 — Generate custom.js

Read `.claude/commands/custom-js.md` and execute it with `SITE_DIR` set to `[SITE_DIR]`.

This writes `[SITE_DIR]/custom.js` and `[SITE_DIR]/partials/scroll-top-btn.html`.

---

## Step 7 — Build content plan

For each included section, plan specific content tailored to the brand. Never use Lorem Ipsum. Everything must feel like it belongs to this specific business.

Plan the following:
- **navbar**: brand name, 3-4 nav links matching included sections, CTA button label if appropriate
- **hero**: headline (punchy, benefit-led), subheadline (1-2 sentences), primary CTA label, secondary CTA label, style (centered or split)
- **features**: section headline, 3-4 features each with a relevant Font Awesome icon name, title, and 1-2 sentence description
- **testimonials**: 3 realistic quotes with plausible names, job titles, and company names relevant to the industry
- **pricing**: 3 tiers with names, prices, feature lists, and which tier to highlight
- **faq**: 5 questions and answers relevant to the specific business
- **team**: 3-4 team members with names, roles, and one-sentence bios
- **contact-form**: headline, subheadline, style (simple or split), contact details if split
- **cta**: headline, subheadline, primary button, optional secondary button, theme (primary/dark)
- **footer**: tagline, 3 link columns with relevant headings and links, social platforms, copyright line

---

## Step 8 — Write site.json

Write `[SITE_DIR]/site.json` using the Write tool:
```json
{
  "title": "[brand name]",
  "sections": ["navbar", "hero", ... ordered list of chosen sections ...]
}
```

---

## Step 9 — Generate each partial

For each section in the chosen list, generate the HTML and write it to `[SITE_DIR]/partials/[section].html` using the Write tool.

Follow these Bootstrap 5 rules for every partial:
- Bootstrap 5 classes only — no custom CSS, no inline styles (except the scroll-top-btn fixed positioning)
- Every section element must have `id="[section-name]"` on its outermost tag (except navbar and scroll-top-btn)
- All nav links must use `href="#[section-id]"` — never `href="#"` alone
- Font Awesome 6 solid icons: `fa-solid fa-[icon]`
- Font Awesome 6 brand icons: `fa-brands fa-[icon]`
- Hero image: use the URL from `[SITE_DIR]/image.json` — do NOT use placehold.co for the hero
- All other placeholder images (team avatars, testimonial avatars): `https://placehold.co/[width]x[height]`
- Section padding: `py-5` on all sections
- Cards: `shadow-sm border-0 h-100`
- contact-form: the `<form>` element MUST include `action="https://formspree.io/f/YOUR_FORM_ID" method="POST"` — never a bare `<form>` tag
- scroll-top-btn: already written to `[SITE_DIR]/partials/scroll-top-btn.html` in Step 6 — do NOT regenerate it here, skip it in this step

Refer to the skill files in `.claude/commands/` for the exact HTML structure of each component. Generate content that is specific, on-brand, and consistent in tone across all sections.

---

## Step 10 — Run the assembly script

Run the following command using the Bash tool:
```
python scripts/assemble.py [SITE_DIR]/site.json
```

---

## Step 11 — Build additional pages (if requested)

Skip this step entirely if `additional_pages` is empty.

If additional pages were requested, do the following for each page type in the list:

### 11a — Invoke the page-builder agent

Read `.claude/agents/page-builder.md` and execute it with:
- `page_type`: the page type (e.g. "about")
- `brand`: the brand name from Step 1
- `industry`: the industry from Step 1
- `tone`: the tone from Step 1
- `SITE_DIR`: `[SITE_DIR]`
- `all_pages`: a list of all pages in the site, including the landing page and every additional page. Format:
  ```
  [{"label": "Home", "url": "index.html"}, {"label": "About", "url": "about.html"}, ...]
  ```
  Use a capitalised label for each page type (About, Contact, Services, etc.).

The agent will generate partials, write `[SITE_DIR]/[page_type]-site.json`, and produce `[SITE_DIR]/[page_type].html`.

### 11b — Update the landing page navbar

After ALL additional pages have been built, regenerate `[SITE_DIR]/partials/navbar.html` so it links to every page in the site using full filenames:
- Landing page sections become `href="index.html#section-id"` (so they still work from other pages)
- Additional pages get their own `<li>` with `href="[page].html"`

Then re-run the landing page assembly to pick up the new navbar:
```
python scripts/assemble.py [SITE_DIR]/site.json
```

---

## Step 12 — Generate SEO meta tags

Now that all pages (landing page and any additional pages) have been assembled, run the SEO meta skill so every page gets meta tags.

Read `.claude/commands/seo-meta.md` and execute it with `SITE_DIR` set to `[SITE_DIR]`. It will:
- Discover all pages from `[SITE_DIR]/site.json` and any `[SITE_DIR]/*-site.json` files
- Write `[SITE_DIR]/site-meta.json` with descriptions and Open Graph tags for every page
- Re-assemble all pages so meta tags appear in the `<head>` of each HTML file

If a base URL was mentioned in $ARGUMENTS (e.g. "use domain mybrand.com"), pass it to the skill. Otherwise it will use `https://example.com` as a placeholder.

---

## Step 13 — Run the review agent

Read `.claude/agents/review.md` and execute it with `SITE_DIR` set to `[SITE_DIR]`. The agent will audit all assembled HTML files, run 10 checks, auto-fix simple issues (copyright year, font mismatches), and output a PASS/WARN/FAIL report.

---

## Step 14 — Report to the user

Before reporting, record this build as the most recent site so standalone agents can discover it automatically:
```
python -c "open('output/.last-build', 'w').write('[slug]'); print('Recorded last build: [slug]')"
```

After successful assembly and review, report:
1. Site folder: `[SITE_DIR]/` (e.g. "Your site was built in `output/serenity-flow/`")
2. Files assembled (e.g. "`index.html`, `about.html`, `contact.html`")
3. A brief list of which sections were included on the landing page
4. Which additional pages were generated and what sections each contains
5. One short sentence on any sections that were intentionally left out and why
6. A summary of the review report (how many PASS/WARN/FAIL, and the most important action items)
7. A suggestion for what to refine next (e.g., "replace placeholder images with real photos", "run restyle agent to change the visual theme")
