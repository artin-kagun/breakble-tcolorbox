# Nested Breakable Behavior Report

- status: PASS
- source verification: root completion gate outputs copied from `build/compare`

## PDFs

| case | PDF |
| --- | --- |
| A4 nested behavior, original left / breakble right | `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf` |
| Title/no-title mixed continuations | `verification/nested-behavior/pdf/a4-nested-title-mix.pdf` |
| Deep title/no-title mixed continuations | `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf` |
| Nested breakable stress cases | `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf` |
| Titleless nesting depths 2 through 6 | `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf` |

## Checked Requirements

| requirement | evidence |
| --- | --- |
| Nested breakable boxes start in the remaining page space instead of being pushed as one unbreakable object. | `nested_behavior=ok` in `verification/nested-behavior/reports/nested-behavior-report.txt` |
| Continuation pages keep parent and child frame tops aligned instead of accumulating vertical inset through nesting. | `same-top-after ... ok` in `verification/nested-behavior/reports/nested-edge-alignment-report.txt` |
| First fragments reach the same lower edge as the surrounding breakable frames, including four-level nesting. | `same-bottom ... ok` in `verification/nested-behavior/reports/nested-edge-alignment-report.txt` |
| Title/no-title mixtures keep the intended clearance: title-adjacent cases get about 1 mm, titleless-to-titleless stays flush. | `title_mix_clearance=ok` in `verification/nested-behavior/reports/title-mix-clearance-report.txt` |
| Stress cases cover midpage starts, no-title continuation, four-level nesting, and decorated upper/lower content. | `stress_markers=ok` in `verification/nested-behavior/reports/stress-report.txt` |
| Fully titleless nesting is available for depths 2, 3, 4, 5, and 6. | Source: `docs/samples/titleless-nesting-depths.tex`; PDF: `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf` |

## Key Measurements

- `case-f-title-to-titleless`: 1.016 mm, target 1.000 mm, tolerance 0.250 mm.
- `case-f-titleless-to-title`: 1.016 mm, target 1.000 mm, tolerance 0.250 mm.
- `case-h-titleless-to-titleless`: -0.042 mm, target 0.000 mm, tolerance 0.250 mm.
- Four-level continuation frame tops: span 0.50 pt, limit 3.00 pt.
- Four-level first-fragment frame bottoms: span 0.50 pt, limit 3.00 pt.
