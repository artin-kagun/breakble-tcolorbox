# breakble-tcolorbox

`breakble-tcolorbox` is an unofficial modified distribution of
[`tcolorbox`](https://github.com/T-F-S/tcolorbox) 6.10.0.

The goal of this package is narrow: allow a normal nested `breakable`
`tcolorbox` to participate in page breaking when its immediate parent
`tcolorbox` is also `breakable`, while preserving the original `tcolorbox`
output for non-nested and existing documented examples.

## Status

- Upstream base: `tcolorbox` 6.10.0, tag `v6.10.0`
- Upstream commit used for this copy: `057ff62f77aeef399251ac4fca98d1a20c36ab32`
- License: LPPL 1.3c or later, matching upstream `tcolorbox`
- Maintenance: unofficial; not maintained by the upstream `tcolorbox` author

## Usage

Put this repository on TeX's input path and load:

```tex
\usepackage[most]{breakble-tcolorbox}
```

Do not also load `tcolorbox` directly in the same document. The wrapper passes
package options through and loads this repository's modified `tcolorbox` copy.

Example from this repository root:

```sh
TEXINPUTS="$PWD//:" latexmk -pdf your-document.tex
```

## What Changed

The upstream package disables normal nested `breakable` boxes. This distribution
keeps that behavior unless the immediate parent box is also `breakable`.

When the parent is breakable and a child uses the ordinary `breakable` key, the
child is split into parent-managed fragments instead of forcing its own physical
page break. This avoids the large blank area that occurs before a nested box
which cannot start in the remaining space of the current parent fragment.

`enforce breakable` remains an explicit escape hatch and is not treated as the
new parent-managed nested behavior. This matters for existing upstream features
such as the `poster` library.

See `MODIFICATIONS.md` for the file-level summary.

## Verification

The upstream standalone examples are compiled twice:

- original `tcolorbox` 6.10.0
- this `breakble-tcolorbox` distribution

The rendered pages are compared pixel-by-pixel, and side-by-side PDFs are
generated with original output on the left and breakble output on the right.

Current report:

- `verification/example-parity/report.md`
- `verification/example-parity/side-by-side/tcolorbox-example/tcolorbox-example__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-example-poster/tcolorbox-example-poster__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-tutorial-poster/tcolorbox-tutorial-poster__original-side-by-side.pdf`

To regenerate:

```sh
scripts/check-upstream-example-parity.py
```

The script expects `latexmk`, `pdflatex`, `pdfinfo`, and `pdftopng`. If
`pygmentize` is not on `PATH`, it installs Pygments into `/tmp` for the current
run only.

## Repository Layout

- `breakble-tcolorbox.sty`: public wrapper package
- `tcolorbox/`: modified runtime package files
- `vendor/tcolorbox-original/`: unmodified upstream runtime files used for parity checks
- `docs/tcolorbox/`: upstream standalone example sources and assets used by parity checks
- `verification/example-parity/`: generated parity report, source copies, and side-by-side PDFs

## Upstream

This package is based on Thomas F. Sturm's `tcolorbox`.

Upstream project:
<https://github.com/T-F-S/tcolorbox>

This repository is not affiliated with or endorsed by the upstream maintainer.
