# Bootstrap Website Generator — Agentic System

An agentic system that takes a user prompt and generates a complete, demo-ready Bootstrap website. Designed to minimize token usage through reusable skills and scripts.

## Architecture

```
User Prompt
    │
    ▼
Orchestrator Agent
    │  (interprets prompt, decides which components are needed, calls skills in order)
    ├──► Skill: navbar
    ├──► Skill: hero
    ├──► Skill: features-section
    ├──► Skill: pricing
    ├──► Skill: footer
    │    ... etc
    ▼
Scripts (assemble HTML partials, inject Bootstrap CDN, scaffold file structure)
    │
    ▼
Integration Agent (consistency pass — colors, spacing, class conflicts, seams between components)
    │
    ▼
Ready-to-run Bootstrap website
```

## Design Principles

- **Hyper-specific skills**: Each skill generates one Bootstrap component. Narrow scope = low token cost.
- **Reusable scripts**: Mechanical operations (file scaffolding, HTML assembly, CDN injection) are pure code — no LLM needed.
- **Orchestrator does the lifting**: The orchestrator reads the user prompt and decides which skills to call and in what order.
- **Integration agent at the end**: Cheaper to fix seams once at the end than to make every skill aware of every other skill's output.
- **Consistent skill interface**: Every component skill takes the same shape of input (JSON context + user intent) and returns a self-contained HTML partial. The orchestrator can call any skill the same way.

## Skill Interface Contract

Each component skill:
- **Input**: JSON context object + user intent string
- **Output**: Self-contained HTML partial (Bootstrap classes, no external dependencies beyond Bootstrap CDN)

## Planned Components (Minimum Viable Set)

| Skill | Component |
|---|---|
| `navbar` | Navigation bar with brand + links |
| `hero` | Hero / jumbotron section |
| `features` | Features or cards section |
| `testimonials` | Testimonials section |
| `pricing` | Pricing table |
| `cta` | Call-to-action section |
| `footer` | Page footer |

## Workflow

1. User provides a prompt describing the website they want
2. Orchestrator interprets the prompt and selects the appropriate components
3. Orchestrator calls each component skill in sequence
4. Scripts assemble the HTML partials into a complete page with Bootstrap CDN
5. Integration agent reviews the assembled page and fixes any inconsistencies
6. User receives a ready-to-run website they can open in a browser
7. User refines using Claude Code

## Delivery Goal

Get a working demo website running as fast as possible. Polish and refinement come after, interactively with Claude Code.
