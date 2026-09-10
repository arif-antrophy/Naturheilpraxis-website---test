---
name: praxis-design-system
description: The design system and structural contract for the Naturheilpraxis Cornelia Dinger site (index.html). Load before editing, extending, or restyling anything in this repo — adding a section or component, touching CSS, changing type/color/spacing/motion, adding images, or building a second page. It carries the token contract, the type and weight discipline, the motion rules, the two load-bearing structural gotchas, the image constraints, and the build/verify loop. Read it before writing CSS here, not after.
---

# Naturheilpraxis Dinger — design system

One hand-written file, no framework, no build step: `index.html` is the source.
`README.md` documents *what the site is*; this skill is *what you may not break*.

## The core rule

**Every surface, hairline, and text tone is one plum hue at a different alpha.**
That single derivation is what makes the page read as one system rather than a
collection of sections. `--ink` is a deep plum (`#3A1F30`), never black or a
tinted near-black. Neutral grey appears nowhere.

So: **never introduce a raw color value.** If you need a tone that does not
exist yet, derive it from the plum and add it to `:root` as a token with a
comment saying what alpha it represents. Adding `#f5f5f5` or `#333` anywhere in
this file is a defect, not a shortcut.

## Token contract (`:root`, line ~46)

Use the variable, never the literal. The full set:

| group | tokens |
| --- | --- |
| grounds | `--canvas` `--wash-1` (2%) `--wash-2` (5%) `--wash-3` (9%) |
| lines | `--hairline` (.13) `--hairline-soft` (.07) |
| text | `--ink` `--body` `--muted` `--faint` |
| voltage | `--accent` `--accent-hover` `--accent-wash` `--bright` `--on-accent` |
| radius | `--r-sm:12` `--r-md:16` `--r-lg:20` `--r-xl:26` `--r-pill` |
| shadow | `--shadow-card` `--shadow-panel` `--shadow-cta` |
| layout | `--measure:1200px` `--gutter:clamp(20,5vw,46)` `--sect:clamp(62,7.5vw,112)` |
| motion | `--ease-out` `--ease-in-out` |

`--r-lg` (20px) is the dominant radius. Reach for a different one only when the
element's size genuinely calls for it — a pill button, a large panel — not to
add variety. One radius on everything regardless of hierarchy is the
generic-SaaS tell; so is four radii chosen at random.

Shadows are plum-tinted, not `rgba(0,0,0,.1)`. Keep it that way.

## Type and weight discipline

Figtree only, one family for everything. The system is **big sizes at light
weights** — that is the whole personality:

- `h1` `clamp(2.55rem,5.6vw,4.25rem)` / **400** / `-.032em`
- `h2` `clamp(1.85rem,3.5vw,2.7rem)` / **400** / `-.026em`
- `h3` `1.3rem` / 600 / `-.014em`
- body `17px` / 400 / `1.62`
- `.lede` `clamp(1.08rem,1.6vw,1.3rem)` / `max-width:56ch`
- hero `h1` `clamp(2.9rem,6.5vw,5.4rem)` / 500 — the one place weight rises
- hero stat numerals **300** — the lightest weight on the page, deliberately

Rules that follow from this:
- **Never set a headline to 700.** Large type here gets its presence from size
  and negative tracking, not weight. 600 is the ceiling for headings (`h3`).
- Negative letter-spacing scales with size. New large type needs it too.
- Numerals in any tabular context get `font-variant-numeric:tabular-nums`.
- Body measures cap at 56–64ch. `.fact__d` caps at 30ch, `.hero .lede` at 34ch.
- `text-wrap:balance` is on all headings already; don't add manual `<br>`.

## Motion rules

Follows Emil Kowalski's design-engineering rules. Non-negotiable:

1. **Custom easing only.** `var(--ease-out)` / `var(--ease-in-out)`. Never
   `ease`, `ease-out`, or `linear` — the built-ins are too weak to read as
   intentional.
2. **Every hover transform sits behind `@media (hover:hover) and (pointer:fine)`.**
   No exceptions; touch devices get the sticky-hover bug otherwise.
3. **Press feedback on every interactive element**, declared *after* the hover
   rules so a press always wins over a hover lift (`.btn:active{transform:scale(.97)}`).
4. Durations: 160ms for press/hover, 180–240ms for state, 320–450ms for reveals.
5. `prefers-reduced-motion` block at the end of the stylesheet already clamps
   everything. If you add a keyframe animation that *ends* hidden or offscreen,
   add an explicit resting state there — see `.scrollcue__drop`, which uses
   `animation:none` plus a visible resting transform rather than inheriting the
   `.01ms` clamp and vanishing.
6. Scattered fade-and-slide-up on every section is the AI-generated default.
   This page spends its motion budget on four orchestrated moments: the falling
   droplet scroll cue, the scroll-driven voice wall, the statement typing itself
   in word by word, and the Ablauf rail drawing 01 -> 02 -> 03 on a loop. That
   is the ceiling — the budget is spent. Do not add a fifth without removing one.
   The Ablauf loop is the only perpetual one; if motion ever needs trimming,
   gate it to play once on scroll-in and it stops being perpetual.

## Two structural gotchas — these will silently break the page

- **`overflow` must be `clip`, never `hidden`** on `body` and `.vwall`.
  `hidden` makes the element a scroll container, which disables
  `position:sticky` in every descendant.
- **The voice wall's cards live inside the 90svh sticky stage** and are moved by
  scroll position, not document flow. That is what lets the stage clip them.
  Do not "fix" them into normal flow.

## Images

Sources are small — the practice's own photos, 167–251px wide native.

- **Never place an image above its native size.** Check the file before
  choosing a display width.
- Always ship explicit `width`/`height` attributes (prevents CLS).
- Below the fold: `loading="lazy" decoding="async"`.
- Decorative images get `alt=""`; the footer mark also gets `aria-hidden="true"`.
- Meaningful images get **German** alt text.
- Reference `assets/clean/*` (repaired crops), never `assets/*` (originals with
  baked-in pink frames and baked-in German text).
- Icons are a single inline SVG sprite at the top of `<body>` — add a `<symbol>`
  there and `<use>` it; never paste a second copy of a path.

## The two dark bands

Exactly two sections invert: the services slider and the footer (plus the hero's
gradient-over-photo). This is a deliberate rhythm — light, airy, then two
punctuation marks. **Do not add a third dark section** without deciding the
rhythm is changing.

On dark grounds, text is white at a fixed alpha ladder: `.90` lede, `.84`
secondary, `.82` card body, `.76` footer body, `.66` attribution. Reuse those
values rather than inventing new ones. Buttons on dark invert to a white ground
with `--accent` text.

The header comment in `index.html` describes this correctly now; keep it in
sync if the rhythm changes.

## Copy

German, formal **Sie** throughout (`Sie` / `Ihre` / `Ihnen` — never `du`).
Medical claims stay careful: this is a Heilpraktiker practice, so describe
methods and process, never promise outcomes. CTAs name what happens
("Kostenloses Vorgespräch"), not "Submit".

`.eyebrow` is used 11 times as a pill with a `--bright` dot — that's the house
label pattern. Three `text-transform:uppercase` rules remain (scroll cue,
bigtel label, footer `h4`) and they are the only tracked-caps on the page;
they're small structural labels, not headline decoration. Don't add more — the
pullquote's `cite` was the fourth and is now sentence case.

## Quality floor

Already in place — keep it: `:focus-visible` with a 2.5px accent outline,
`@media (hover:hover)` guards, reduced-motion block, three breakpoints
(1140 / 900 / 740), `color-scheme:light` (light-only by design, no dark variant).

The head is now correct and should stay that way: `<!doctype html>` first (its
absence had the page in quirks mode), then `<html lang="de">`, then
`<meta charset="utf-8">` — the charset must stay above the documentation
comment so it lands inside the first 1024 bytes, since the server sends no
charset parameter of its own.

CSS specificity: this file mixes type-ish selectors (`.section`) with
element-ish ones (`.cta`). Section padding is the usual casualty. When adding a
rule that sets `padding-block` or margins on a section, check it isn't cancelled
by or cancelling `.section`.

## Build and verify loop

1. Edit **`index.html`**. Never edit `index.inlined.html` — it is generated.
2. Preview: `.claude/launch.json` defines `praxis-dinger` on port 4173. Use the
   Browser pane's `preview_start`, not a shell server.
3. Verify at all three breakpoints (`resize_window`), and check `:focus-visible`
   by tabbing, before calling a visual change done.
4. Ship a self-contained build with `python3 build-inline.py` → `index.inlined.html`.
   It exits nonzero on a missing asset, so a broken path fails loudly.

## Before launch

`README.md` holds the open list. The two that constrain *code* decisions:
**self-host Figtree** (the Google Fonts CDN request is a GDPR liability in
Germany — Munich regional court, 2022), and the hero image needs licensing or
replacing. Don't add a second CDN font request in the meantime.
