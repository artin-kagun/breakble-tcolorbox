# Nested Breakable Behavior Report

- status: PASS for the currently checked nested-breakable regression set
- source verification: PDFs below were rebuilt from `docs/samples/*.tex` with the current `breakble-tcolorbox` runtime tree
- log check: the current builds listed under "Current Regression Builds" have no `Package tcolorbox Warning`, `Overfull \vbox`, `Overfull \hbox`, `Underfull \vbox`, TeX error lines, or `BTCDBG` debug lines in the checked logs. Some engine/font-package warnings remain in the proof-style Japanese samples and are unrelated to the breakable drawing logic.

## PDFs

| case | PDF |
| --- | --- |
| A4 nested behavior, case-by-case original/breakble comparison | `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf` |
| Title/no-title mixed continuations | `verification/nested-behavior/pdf/a4-nested-title-mix.pdf` |
| Deep title/no-title mixed continuations | `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf` |
| Nested breakable stress cases | `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf` |
| Nested display math regression | `verification/nested-behavior/pdf/a4-nested-display-math-overlap.pdf` |
| Nested display math regression, XeLaTeX build | `verification/nested-behavior/pdf/a4-nested-display-math-overlap-xelatex.pdf` |
| Continuous SubProof page break, pdfLaTeX viewable Japanese build | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-pdftex-viewable.pdf` |
| Continuous SubProof page break, upLaTeX build | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-uplatex.pdf` |
| Continuous SubProof page break, XeLaTeX build | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-xelatex.pdf` |
| Continuous SubProof page break, LuaLaTeX build | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-lualatex.pdf` |
| Proof/SubProof nested overlap, upLaTeX build | `verification/nested-behavior/pdf/a4-proof-environment-nested-overlap-uplatex.pdf` |
| Proof/SubProof nested overlap, XeLaTeX build | `verification/nested-behavior/pdf/a4-proof-environment-nested-overlap-xelatex.pdf` |
| Japanese nested overlap, upLaTeX build | `verification/nested-behavior/pdf/a4-japanese-nested-overlap-uplatex.pdf` |
| Japanese nested overlap, XeLaTeX build | `verification/nested-behavior/pdf/a4-japanese-nested-overlap-xelatex.pdf` |
| Japanese nested overlap, LuaLaTeX build | `verification/nested-behavior/pdf/a4-japanese-nested-overlap-lualatex.pdf` |
| Mixed title/no-title continuous nesting | `verification/nested-behavior/pdf/a4-nested-mixed-continuous.pdf` |
| Titleless nesting depths 2 through 6 | `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf` |
| Non-nested titleless reach reference | `verification/nested-behavior/pdf/a4-titleless-reach-reference.pdf` |
| Non-A4 B5 smoke sample | `verification/nested-behavior/pdf/b5-nested-breakable-smoke.pdf` |
| Parent-tail text after nested box, upLaTeX build | `verification/nested-behavior/pdf/a4-nested-parent-tail-regression-uplatex.pdf` |
| Parent-tail text after nested box, XeLaTeX build | `verification/nested-behavior/pdf/a4-nested-parent-tail-regression-xelatex.pdf` |
| Parent color restoration after nested box | `verification/nested-behavior/pdf/a4-nested-parent-color-restore.pdf` |

## Current Regression Builds

| source | engine | output |
| --- | --- | --- |
| `docs/samples/a4-proof-environment-continuous-inner-break-pdftex-viewable.tex` | pdfLaTeX | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-pdftex-viewable.pdf` |
| `docs/samples/a4-proof-environment-continuous-inner-break.tex` | upLaTeX + dvipdfmx | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-uplatex.pdf` |
| `docs/samples/a4-proof-environment-continuous-inner-break.tex` | XeLaTeX | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-xelatex.pdf` |
| `docs/samples/a4-proof-environment-continuous-inner-break.tex` | LuaLaTeX | `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-lualatex.pdf` |
| `docs/samples/a4-proof-environment-nested-overlap.tex` | upLaTeX + dvipdfmx | `verification/nested-behavior/pdf/a4-proof-environment-nested-overlap-uplatex.pdf` |
| `docs/samples/a4-proof-environment-nested-overlap.tex` | XeLaTeX | `verification/nested-behavior/pdf/a4-proof-environment-nested-overlap-xelatex.pdf` |
| `docs/samples/a4-japanese-nested-overlap.tex` | upLaTeX + dvipdfmx | `verification/nested-behavior/pdf/a4-japanese-nested-overlap-uplatex.pdf` |
| `docs/samples/a4-japanese-nested-overlap.tex` | XeLaTeX | `verification/nested-behavior/pdf/a4-japanese-nested-overlap-xelatex.pdf` |
| `docs/samples/a4-japanese-nested-overlap.tex` | LuaLaTeX | `verification/nested-behavior/pdf/a4-japanese-nested-overlap-lualatex.pdf` |
| `docs/samples/a4-nested-display-math-overlap.tex` | pdfLaTeX | `verification/nested-behavior/pdf/a4-nested-display-math-overlap.pdf` |
| `docs/samples/a4-nested-display-math-overlap.tex` | XeLaTeX | `verification/nested-behavior/pdf/a4-nested-display-math-overlap-xelatex.pdf` |
| `docs/samples/a4-nested-mixed-continuous.tex` | pdfLaTeX | `verification/nested-behavior/pdf/a4-nested-mixed-continuous.pdf` |
| `docs/samples/titleless-nesting-depths.tex` | pdfLaTeX | `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf` |
| `docs/samples/titleless-reach-reference.tex` | pdfLaTeX | `verification/nested-behavior/pdf/a4-titleless-reach-reference.pdf` |
| `docs/samples/b5-nested-breakable-smoke.tex` | pdfLaTeX | `verification/nested-behavior/pdf/b5-nested-breakable-smoke.pdf` |
| `docs/samples/a4-nested-parent-tail-regression.tex` | XeLaTeX | `verification/nested-behavior/pdf/a4-nested-parent-tail-regression-xelatex.pdf` |
| `docs/samples/a4-nested-parent-tail-regression.tex` | upLaTeX + dvipdfmx | `verification/nested-behavior/pdf/a4-nested-parent-tail-regression-uplatex.pdf` |
| `docs/samples/a4-nested-parent-color-restore.tex` | pdfLaTeX | `verification/nested-behavior/pdf/a4-nested-parent-color-restore.pdf` |

## Checked Requirements

| requirement | evidence |
| --- | --- |
| Nested breakable boxes start in the remaining page space instead of being pushed as one unbreakable object. | `nested_behavior=ok` in `verification/nested-behavior/reports/nested-behavior-report.txt` |
| Continuation pages keep parent and child frame tops aligned instead of accumulating vertical inset through nesting. | `same-top-after ... ok` in `verification/nested-behavior/reports/nested-edge-alignment-report.txt` |
| First fragments reach the same lower edge as the surrounding breakable frames, including four-level nesting. | `same-bottom ... ok` in `verification/nested-behavior/reports/nested-edge-alignment-report.txt` |
| Title/no-title mixtures keep the intended clearance: title-adjacent cases get about 1 mm, titleless-to-titleless stays flush. | `title_mix_clearance=ok` in `verification/nested-behavior/reports/title-mix-clearance-report.txt` |
| Stress cases cover midpage starts, no-title continuation, four-level nesting, and decorated upper/lower content. | `stress_markers=ok` in `verification/nested-behavior/reports/stress-report.txt` |
| Display math inside nested breakable boxes keeps normal vertical spacing before the following paragraph. | `display_math_overlap_text=ok` in `verification/nested-behavior/reports/display-math-overlap-report.txt`; visual PDF: `verification/nested-behavior/pdf/a4-nested-display-math-overlap.pdf` |
| A continuous proof-style SubProof can start on the same page and continue without broken Japanese rendering in the review PDF. | Visual PDF: `verification/nested-behavior/pdf/a4-proof-environment-continuous-inner-break-pdftex-viewable.pdf`; engine builds: `...-uplatex.pdf`, `...-xelatex.pdf`, `...-lualatex.pdf`. |
| Fully titleless nesting is available for depths 2, 3, 4, 5, and 6, and its first-fragment bottom reach stays close to the non-nested reference. | Source: `docs/samples/titleless-nesting-depths.tex`; reports: `verification/nested-behavior/reports/titleless-reach-reference-report.txt` and `verification/nested-behavior/reports/titleless-nesting-depths-reach-report.txt` |
| The implementation is not tied to A4 dimensions. | `verification/nested-behavior/pdf/b5-nested-breakable-smoke.pdf` was rebuilt as a B5 non-A4 smoke sample. |
| Engine checks do not show an engine-specific drawing regression for the checked engines. | pdfLaTeX builds passed for the current sample set; upLaTeX + dvipdfmx, XeLaTeX, and LuaLaTeX passed for the Japanese proof-style samples selected for cross-engine checking. |

## Key Measurements

- `case-f-title-to-titleless`: 1.016 mm, target 1.000 mm, tolerance 0.250 mm.
- `case-f-titleless-to-title`: 1.016 mm, target 1.000 mm, tolerance 0.250 mm.
- `case-h-titleless-to-titleless`: -0.042 mm, target 0.000 mm, tolerance 0.250 mm.
- Four-level continuation frame tops: span 0.50 pt, limit 3.00 pt.
- Four-level first-fragment frame bottoms: span 0.50 pt, limit 3.00 pt.
- Nested display math regression: 3 A4 pages in the current pdfLaTeX build, no visible marker artifacts in the inspected PNG pages, and no `tcolorbox`/overfull/underfull/debug lines in the checked logs.
- Continuous proof-style SubProof: 4 pages in the pdfLaTeX viewable Japanese build, and 5 pages in each of the upLaTeX, XeLaTeX, and LuaLaTeX builds; inspected PNG pages show the nested SubProof starting on page 1 and continuing without the empty-parent-page symptom.
- Titleless non-nested reference first fragment: 5.00 pt bottom gap.
- Titleless nested first fragments for depths 2, 3, 4, 5, and 6: 6.00 pt, 6.00 pt, 6.00 pt, 5.00 pt, and 10.00 pt bottom gaps.

## How to Read `a4-nested-behavior-side-by-side.pdf`

This PDF is intentionally case-by-case, not page-number-by-page-number. For each
case, the `start page` spread shows the original tcolorbox output on the left
and the breakble-tcolorbox output on the right at the point where the nested box
should start. The `following page` spread then shows the next relevant page for
the same case. This makes the original blank-space failure and the breakble
placement directly visible.
