# breakble-tcolorbox

[English](README.md) | [日本語](README.ja.md)

`breakble-tcolorbox` is an unofficial modified distribution of
[`tcolorbox`](https://github.com/T-F-S/tcolorbox) 6.10.0.

It keeps the public `tcolorbox` interface, but changes one narrow behavior:
ordinary nested `breakable` boxes can break when their immediate parent
`tcolorbox` is also `breakable`.

The intended result is:

- ordinary non-nested `tcolorbox` output stays the same as upstream;
- existing upstream examples and manual sources still render the same;
- a long `breakable` box nested inside another `breakable` box can use the
  remaining space on the current page instead of being pushed to the next page
  as one large unbreakable block.

This repository is not affiliated with, maintained by, or endorsed by the
upstream `tcolorbox` maintainer.

## Quick Use

Load this package instead of loading `tcolorbox` directly:

```tex
\usepackage[most]{breakble-tcolorbox}
```

After that, keep using the usual `tcolorbox` commands:

```tex
\begin{tcolorbox}[breakable,title={Outer box}]
  Text before the nested box.

  \begin{tcolorbox}[breakable,title={Nested box}]
    Long nested content...
  \end{tcolorbox}
\end{tcolorbox}
```

Do not write both of these in the same document:

```tex
\usepackage{tcolorbox}
\usepackage{breakble-tcolorbox}
```

`breakble-tcolorbox` is a wrapper. It passes package options such as `most`,
`skins`, and `breakable` to the modified `tcolorbox` files shipped in this
repository.

## What Changes Visually

With upstream `tcolorbox`, a normal nested `breakable` box is effectively not
allowed to break. If the nested box does not fit in the remaining part of the
current page, it may be moved to the next page, leaving a large blank area.

With `breakble-tcolorbox`, the nested box is split into fragments managed by the
parent breakable box, so the first fragment can start in the remaining space.

The following comparison uses the same A4 document. The only meaningful
difference is the package being loaded: upstream `tcolorbox` on the left,
`breakble-tcolorbox` on the right. Page 1 shows the actual problem: upstream
leaves the page remainder blank, while the breakble version starts the nested
box immediately. Page 2 shows that the nested box really continued across the
page break.

![Nested breakable comparison page 1](docs/readme-demo/images/nested-breakable-comparison-page-000001.png)

![Nested breakable comparison page 2](docs/readme-demo/images/nested-breakable-comparison-page-000002.png)

The same comparison is also available as a PDF:

- `docs/readme-demo/nested-breakable-comparison.pdf`

The core of the sample is ordinary `tcolorbox` code:

```tex
\begin{outerdemo}
Text before the nested box.

\begin{innerdemo}
Nested breakable content begins here.

% Long ordinary prose follows.
% In upstream tcolorbox this nested box is moved to the next page.
% In breakble-tcolorbox it starts here and continues on the next page.
\end{innerdemo}

Text after the nested box.
\end{outerdemo}
```

The full sample sources are in `docs/readme-demo/`:

- `nested-breakable-original.tex`: uses upstream `tcolorbox`
- `nested-breakable-breakble.tex`: uses `breakble-tcolorbox`
- `nested-breakable-body.tex`: shared document body
- `nested-breakable-comparison.pdf`: side-by-side output, original left and
  breakble right

In the breakble version, the document starts with:

```tex
\documentclass[a4paper,11pt]{article}
\usepackage[margin=24mm]{geometry}
\usepackage[most]{breakble-tcolorbox}

\input{nested-breakable-body.tex}
```

The original comparison version uses the same body, but loads:

```tex
\usepackage[most]{tcolorbox}
```

To rebuild the two demo PDFs from this repository root:

```sh
cd docs/readme-demo
TEXINPUTS="$PWD:$PWD/../../vendor/tcolorbox-original//:" \
  latexmk -pdf -outdir=../../build/readme-demo/original nested-breakable-original.tex
TEXINPUTS="$PWD:$PWD/../..:$PWD/../../tcolorbox//:" \
  latexmk -pdf -outdir=../../build/readme-demo/breakble nested-breakable-breakble.tex
```

## Which Files Are Used

For normal use, the user-facing entry point is:

- `breakble-tcolorbox.sty`

The directory below is also required at compile time:

- `tcolorbox/`

That `tcolorbox/` directory is a modified copy of upstream runtime files. It
contains `tcolorbox.sty`, library files such as `tcbbreakable.code.tex` and
`tcbskins.code.tex`, and image assets used by some skins. It is not a separate
package that you load by hand, and it should not be copied only partially.

In a document, load only:

```tex
\usepackage[most]{breakble-tcolorbox}
```

Do not load `tcolorbox/` directly. The wrapper loads the modified runtime files.

## Project-Local Installation

This is the safest way to try the package because it affects only one project.

Keep this repository somewhere on disk, then compile your document with this
repository at the front of TeX's input path:

```sh
TEXINPUTS="/path/to/breakble-tcolorbox//:" latexmk -pdf main.tex
```

For example, if this repository is next to your document:

```sh
TEXINPUTS="../breakble-tcolorbox//:" latexmk -pdf main.tex
```

The `//` is important: it tells TeX to search the repository recursively, so it
can find both `breakble-tcolorbox.sty` and the files inside `tcolorbox/`.

You can verify what TeX will find with:

```sh
TEXINPUTS="/path/to/breakble-tcolorbox//:" kpsewhich breakble-tcolorbox.sty
TEXINPUTS="/path/to/breakble-tcolorbox//:" kpsewhich tcolorbox.sty
```

Both paths should point into this repository.

## Personal TEXMF Installation

If you want TeX to find the package without setting `TEXINPUTS` every time,
install it into your personal TEXMF tree.

Find the personal TEXMF root:

```sh
kpsewhich -var-value=TEXMFHOME
```

On MacTeX this is commonly:

```text
~/Library/texmf
```

Create a package directory and copy the runtime files:

```sh
TEXMFHOME="$(kpsewhich -var-value=TEXMFHOME)"
mkdir -p "$TEXMFHOME/tex/latex/breakble-tcolorbox"

cp breakble-tcolorbox.sty "$TEXMFHOME/tex/latex/breakble-tcolorbox/"
cp -R tcolorbox "$TEXMFHOME/tex/latex/breakble-tcolorbox/"
```

For `TEXMFHOME`, TeX Live usually notices files without rebuilding a filename
database. If TeX does not find the package, run:

```sh
mktexlsr "$TEXMFHOME"
```

Then check:

```sh
kpsewhich breakble-tcolorbox.sty
kpsewhich tcolorbox.sty
```

When this package is installed this way, `kpsewhich tcolorbox.sty` should also
point to the modified copy under `breakble-tcolorbox/tcolorbox/`. This is
expected: the wrapper works by loading a modified `tcolorbox.sty`.

## Site-Wide TEXMF Installation

For a shared TeX Live installation, use `TEXMFLOCAL`:

```sh
kpsewhich -var-value=TEXMFLOCAL
```

Then copy the same two items into:

```text
<TEXMFLOCAL>/tex/latex/breakble-tcolorbox/
```

For example:

```sh
TEXMFLOCAL="$(kpsewhich -var-value=TEXMFLOCAL)"
sudo mkdir -p "$TEXMFLOCAL/tex/latex/breakble-tcolorbox"
sudo cp breakble-tcolorbox.sty "$TEXMFLOCAL/tex/latex/breakble-tcolorbox/"
sudo cp -R tcolorbox "$TEXMFLOCAL/tex/latex/breakble-tcolorbox/"
sudo mktexlsr
```

Use a site-wide install only if you are comfortable with this modified
`tcolorbox` being found before the upstream copy for documents compiled in that
TeX installation.

## If Another Package Loads `tcolorbox`

There are two common cases.

If you can control the preamble, load `breakble-tcolorbox` before packages that
use `tcolorbox` internally:

```tex
\usepackage[most]{breakble-tcolorbox}
\usepackage{some-package-that-uses-tcolorbox}
```

When that later package calls `\RequirePackage{tcolorbox}`, LaTeX sees that
`tcolorbox` is already loaded. It will use the modified copy that
`breakble-tcolorbox` loaded.

If a document class or package loads `tcolorbox` before you have a chance to
load `breakble-tcolorbox`, the wrapper cannot replace it afterward. In that
case, put this repository before the system `tcolorbox` on TeX's search path and
do not load the wrapper later:

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/tcolorbox//:" latexmk -pdf main.tex
```

Then a direct internal `\RequirePackage{tcolorbox}` will resolve to the modified
runtime copy. Confirm this in the `.log` file or with:

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/tcolorbox//:" kpsewhich tcolorbox.sty
```

If a later package loads `tcolorbox` with package options, load a sufficiently
broad option set early, for example:

```tex
\usepackage[most]{breakble-tcolorbox}
```

This avoids most option-clash situations because `most` loads the usual
`tcolorbox` libraries.

## Status

- Upstream base: `tcolorbox` 6.10.0, tag `v6.10.0`
- Upstream commit used for this copy: `057ff62f77aeef399251ac4fca98d1a20c36ab32`
- License: LPPL 1.3c or later, matching upstream `tcolorbox`
- Maintenance: unofficial; not maintained by the upstream `tcolorbox` author

## Verification

The nested-breakable requirements used for development are recorded in
`docs/nested-breakable-requirements.md`.

The upstream standalone examples and the upstream manual source are compiled
twice:

- original `tcolorbox` 6.10.0
- this `breakble-tcolorbox` distribution

The rendered pages are compared pixel-by-pixel, and side-by-side PDFs are
generated with original output on the left and breakble output on the right.

Standalone example report:

- `verification/example-parity/report.md`
- `verification/example-parity/side-by-side/tcolorbox-example/tcolorbox-example__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-example-poster/tcolorbox-example-poster__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-tutorial-poster/tcolorbox-tutorial-poster__original-side-by-side.pdf`

Nested behavior evidence:

- `verification/nested-behavior/report.md`
- `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf`
- `verification/nested-behavior/pdf/a4-nested-title-mix.pdf`
- `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf`
- `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf`
- `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf`

Manual parity output is generated under `verification/manual-parity/` by the
manual parity script. The manual check compiles `docs/tcolorbox/tcolorbox.tex`,
including the documented `tcolorbox.doc.*.tex` fragments, and compares all
rendered pages.

To regenerate standalone example parity:

```sh
scripts/check-upstream-example-parity.py
```

To regenerate manual parity:

```sh
scripts/check-upstream-manual-parity.py
```

To run the public verification scripts together:

```sh
scripts/run-full-verification.sh
```

The scripts expect `latexmk`, `pdflatex`, `biber`, `makeindex`, `pdfinfo`, and
`pdftopng`. If `pygmentize` is not on `PATH`, they install Pygments into `/tmp`
for the current run only.

## Repository Layout

- `breakble-tcolorbox.sty`: public wrapper package
- `tcolorbox/`: modified runtime package files used by the wrapper
- `vendor/tcolorbox-original/`: unmodified upstream runtime files used for parity checks
- `docs/nested-breakable-requirements.md`: development requirements for nested
  breakable behavior
- `docs/tcolorbox/`: upstream documentation, standalone example sources, and assets used by parity checks
- `docs/readme-demo/`: small A4 sample used for the README comparison image
- `docs/samples/`: additional small samples, including titleless nested boxes
- `verification/example-parity/`: generated parity report, source copies, and side-by-side PDFs
- `verification/nested-behavior/`: generated nested-breakable behavior reports and PDFs
- `verification/manual-parity/`: generated manual parity report, source copies, rendered pages, and side-by-side PDF

## Upstream

This package is based on Thomas F. Sturm's `tcolorbox`.

Upstream project:
<https://github.com/T-F-S/tcolorbox>

This repository is not affiliated with or endorsed by the upstream maintainer.
