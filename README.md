# Naturheilpraxis Cornelia Dinger — Homepage-Redesign

Redesign of the homepage for [naturheilpraxis-dinger.de](https://naturheilpraxis-dinger.de/),
a naturopathic practice (Heilpraktikerin) in Bad Schönborn, Baden-Württemberg.

Single hand-written HTML file. **No framework, no build step, no external
requests at all** — the webfont is self-hosted — 31 KB of CSS, 3.3 KB of vanilla JS, 32 custom properties
carrying the entire design system.

## Run it

```bash
python3 -m http.server 4173
# then open http://localhost:4173
```

`.claude/launch.json` is included if you use Claude Code's preview.

## Files

| file | what it is |
| --- | --- |
| `index.html` | **the source.** Edit this one. References `assets/clean/*` by path |
| `index.inlined.html` | *(not in repo)* generated self-contained build — run `build-inline.py` |
| `build-inline.py` | generates `index.inlined.html` (every image as a data URI) |
| `assets/` | original images pulled from the live site |
| `assets/clean/` | repaired crops — baked-in pink frames and baked-in German text removed |
| `assets/fonts/` | self-hosted Figtree (variable woff2, latin + latin-ext, roman + italic) and its OFL licence |
| `index.v2-backup.html` | earlier warm/serif direction, kept for comparison |

## Design language

Ported from the Clireo healthcare template, remapped onto the practice's own
brand plum (sampled from the real logo, `#7B2255`):

- Light, airy grounds. **Ink is the brand hue, not black** (`#3A1F30`)
- Every surface and hairline is that plum at low alpha (2% / 5% / 13%) rather
  than neutral grey — this is what makes it read as one system
- Big type at light weight; 20px dominant radius; pill CTAs
- Two deliberate dark bands: the services slider and the footer

Motion follows Emil Kowalski's design-engineering rules: custom easing
(`--ease-out: cubic-bezier(.23,1,.32,1)`), press feedback on every interactive
element, all hover transforms behind `@media (hover:hover) and (pointer:fine)`.

## Sections

Hero (100vh, gradient over photo, falling-droplet scroll cue) · statement +
three fact cards · symptom checklist · services slider (dark, full-bleed,
masked edges) · Ablauf · Über mich · Diagnostik & Therapien · voice wall
(sticky 90svh stage, scroll-driven quote cards) · Kosten & FAQ · contact ·
dark footer with the phone number as the closing CTA.

## Known gotchas

Two things will break if changed carelessly:

- **`overflow` must be `clip`, never `hidden`,** on `body` and `.vwall`.
  `hidden` makes an element a scroll container, which disables
  `position: sticky` inside it.
- The voice wall's cards live **inside** the 90svh sticky stage and are moved
  by scroll position, not document flow. That is what lets the stage clip them.

## Outstanding before launch

- [ ] **Licence or replace the hero image.** Excluded from this repo — see `.gitignore`
- [ ] **A photo of Cornelia.** The single highest-value asset for a Heilpraktiker site
- [ ] **Two prices** — `Betrag einsetzen` placeholders in the Kosten block
- [ ] **Wire the contact form.** Front-end only; it shows the thank-you panel without sending
- [ ] Re-shoot or re-export photography at 2× displayed size (sources are 167–251px wide)
- [ ] Opening hours, if she wants them public
