# Nested Breakable Behavior Report

- status: PASS
- source verification: current sample builds copied from `build/current-samples-*` and `build/engine/*`

## PDFs

| case | PDF |
| --- | --- |
| A4 nested behavior, case-by-case original/breakble comparison | `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf` |
| Title/no-title mixed continuations | `verification/nested-behavior/pdf/a4-nested-title-mix.pdf` |
| Deep title/no-title mixed continuations | `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf` |
| Nested breakable stress cases | `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf` |
| Nested display math regression | `verification/nested-behavior/pdf/a4-nested-display-math-overlap.pdf` |
| Nested display math regression, XeLaTeX build | `verification/nested-behavior/pdf/a4-nested-display-math-overlap-xelatex.pdf` |
| Japanese proof-style nested display math, upLaTeX build | `verification/nested-behavior/pdf/a4-proof-nested-overlap-uplatex.pdf` |
| Mixed title/no-title continuous nesting | `verification/nested-behavior/pdf/a4-nested-mixed-continuous.pdf` |
| Titleless nesting depths 2 through 6 | `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf` |
| Non-nested titleless reach reference | `verification/nested-behavior/pdf/a4-titleless-reach-reference.pdf` |
| Non-A4 B5 smoke sample | `verification/nested-behavior/pdf/b5-nested-breakable-smoke.pdf` |

## Checked Requirements

| requirement | evidence |
| --- | --- |
| Nested breakable boxes start in the remaining page space instead of being pushed as one unbreakable object. | `nested_behavior=ok` in `verification/nested-behavior/reports/nested-behavior-report.txt` |
| Continuation pages keep parent and child frame tops aligned instead of accumulating vertical inset through nesting. | `same-top-after ... ok` in `verification/nested-behavior/reports/nested-edge-alignment-report.txt` |
| First fragments reach the same lower edge as the surrounding breakable frames, including four-level nesting. | `same-bottom ... ok` in `verification/nested-behavior/reports/nested-edge-alignment-report.txt` |
| Title/no-title mixtures keep the intended clearance: title-adjacent cases get about 1 mm, titleless-to-titleless stays flush. | `title_mix_clearance=ok` in `verification/nested-behavior/reports/title-mix-clearance-report.txt` |
| Stress cases cover midpage starts, no-title continuation, four-level nesting, and decorated upper/lower content. | `stress_markers=ok` in `verification/nested-behavior/reports/stress-report.txt` |
| Display math inside nested breakable boxes keeps normal vertical spacing before the following paragraph. | `display_math_overlap_text=ok` in `verification/nested-behavior/reports/display-math-overlap-report.txt`; visual PDF: `verification/nested-behavior/pdf/a4-nested-display-math-overlap.pdf` |
| Fully titleless nesting is available for depths 2, 3, 4, 5, and 6, and its first-fragment bottom reach stays close to the non-nested reference. | Source: `docs/samples/titleless-nesting-depths.tex`; reports: `verification/nested-behavior/reports/titleless-reach-reference-report.txt` and `verification/nested-behavior/reports/titleless-nesting-depths-reach-report.txt` |
| The implementation is not tied to A4 dimensions. | `verification/nested-behavior/pdf/b5-nested-breakable-smoke.pdf` was rebuilt as a B5 non-A4 smoke sample. |
| Engine checks do not show an engine-specific drawing regression for the checked engines. | pdfLaTeX sample builds passed; XeLaTeX display-math build passed; upLaTeX Japanese proof-style build passed. LuaLaTeX could not be rendered in this local environment because `luaotfload` stopped before package loading with "no writeable cache path". |

## Key Measurements

- `case-f-title-to-titleless`: 1.016 mm, target 1.000 mm, tolerance 0.250 mm.
- `case-f-titleless-to-title`: 1.016 mm, target 1.000 mm, tolerance 0.250 mm.
- `case-h-titleless-to-titleless`: -0.042 mm, target 0.000 mm, tolerance 0.250 mm.
- Four-level continuation frame tops: span 0.50 pt, limit 3.00 pt.
- Four-level first-fragment frame bottoms: span 0.50 pt, limit 3.00 pt.
- Nested display math regression: 4 A4 pages, no visible marker artifacts in the inspected PNG pages, log clean.
- Titleless non-nested reference first fragment: 5.00 pt bottom gap.
- Titleless nested first fragments for depths 2, 3, 4, 5, and 6: 6.00 pt, 6.00 pt, 6.00 pt, 5.00 pt, and 10.00 pt bottom gaps.

## How to Read `a4-nested-behavior-side-by-side.pdf`

This PDF is intentionally case-by-case, not page-number-by-page-number. For each
case, the `start page` spread shows the original tcolorbox output on the left
and the breakble-tcolorbox output on the right at the point where the nested box
should start. The `following page` spread then shows the next relevant page for
the same case. This makes the original blank-space failure and the breakble
placement directly visible.
