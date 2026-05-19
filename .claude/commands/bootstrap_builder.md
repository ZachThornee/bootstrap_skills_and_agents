You are a Bootstrap 5 website orchestrator. Your job is to take a user's plain English description and produce a complete, assembled Bootstrap 5 website. You coordinate every step from content planning to final assembly.

## Input
$ARGUMENTS — a natural language description of the website the user wants to build.

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

## Step 2 — Decide which sections to include

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

---

## Step 3 — Source the hero image

Before building content, find a relevant image for the hero section.

Check $ARGUMENTS for a user-provided image URL or file path first. If found, use it directly.

If no image is provided, extract 2-3 image keywords from the prompt (e.g. "personal trainer fitness", "coffee shop interior", "SaaS team working") and run the `/find-image` skill by reading `.claude/commands/find-image.md` and executing it with those keywords.

After the skill runs, read `output/image.json` to get the `hero_image` URL and `alt` text. Use these in the hero partial in Step 5. If `output/image.json` does not exist or the URL is empty, fall back to:
`https://source.unsplash.com/800x500/?[keywords-joined-by-plus]`

---

## Step 4 — Run the design profile agent

Before writing any HTML, establish the visual identity for the site.

Check $ARGUMENTS for explicit color or font preferences. If the user has specified colors or fonts, skip this step and use them directly when generating `output/custom.css` later.

If no design preferences are given, invoke the design profile agent by reading `.claude/agents/design-profile.md` and executing it with:
- `industry`: the industry extracted in Step 1
- `tone`: the tone extracted in Step 1
- `brand`: the brand name extracted in Step 1

The agent will write `output/design.json` and `output/custom.css`. After it completes, read `output/design.json` to confirm the primary color, fonts, and vibe. Use the vibe and tone to inform the copy written in Step 5 — a "playful" vibe should produce warmer, more energetic copy than a "minimal" vibe.

---

## Step 5 — Build content plan

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

## Step 6 — Write site.json

Write `output/site.json` using the Write tool:
```json
{
  "title": "[brand name]",
  "sections": ["navbar", "hero", ... ordered list of chosen sections ...]
}
```

---

## Step 7 — Generate each partial

For each section in the chosen list, generate the HTML and write it to `output/partials/[section].html` using the Write tool.

Follow these Bootstrap 5 rules for every partial:
- Bootstrap 5 classes only — no custom CSS, no inline styles (except the scroll-top-btn fixed positioning)
- Every section element must have `id="[section-name]"` on its outermost tag (except navbar and scroll-top-btn)
- All nav links must use `href="#[section-id]"` — never `href="#"` alone
- Font Awesome 6 solid icons: `fa-solid fa-[icon]`
- Font Awesome 6 brand icons: `fa-brands fa-[icon]`
- Hero image: use the URL from `output/image.json` — do NOT use placehold.co for the hero
- All other placeholder images (team avatars, testimonial avatars): `https://placehold.co/[width]x[height]`
- Section padding: `py-5` on all sections
- Cards: `shadow-sm border-0 h-100`

Refer to the skill files in `.claude/commands/` for the exact HTML structure of each component. Generate content that is specific, on-brand, and consistent in tone across all sections.

---

## Step 8 — Run the assembly script

Run the following command using the Bash tool:
```
python scripts/assemble.py
```

---

## Step 9 — Report to the user

After successful assembly, report:
1. "Website assembled at output/index.html"
2. A brief list of which sections were included
3. One short sentence on any sections that were intentionally left out and why
4. A suggestion for what to refine next (e.g., "replace placeholder images with real photos", "swap the primary color", "add a gallery section")
