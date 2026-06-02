# breakble-tcolorbox

[English](README.md) | [日本語](README.ja.md)

`breakble-tcolorbox` is an unofficial modified distribution of
[`tcolorbox`](https://github.com/T-F-S/tcolorbox) 6.10.0.

It keeps the public `tcolorbox` interface while improving page breaking for
ordinary nested `breakable` boxes whose immediate parent `tcolorbox` is also
`breakable`.

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

The following comparison uses the same A4 document. The document body is the
same; the package load is what changes for the comparison: upstream
`tcolorbox` on the left, `breakble-tcolorbox` on the right. Page 1 shows the
actual problem: upstream leaves the page remainder blank, while the breakble
version starts the nested box immediately. Page 2 shows that the nested box
really continued across the page break.

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
TEXINPUTS="$PWD:$PWD/../../texmf/tex/latex//:" \
  latexmk -pdf -outdir=../../build/readme-demo/breakble nested-breakable-breakble.tex
```

## Which Files Are Used

For normal use, the user-facing entry point is:

- `breakble-tcolorbox.sty`

The following runtime files are also required in the same directory:

- `breakble-tcolorbox-runtime.sty`
- `breakble-tcb*.code.tex`

Those files are modified copies of upstream `tcolorbox` runtime files. Their
filenames are intentionally different from upstream filenames such as
`tcolorbox.sty` and `tcbbreakable.code.tex`. This allows the package to be
installed in a TEXMF tree while ordinary `\usepackage{tcolorbox}` continues to
find the upstream package.

The only file a document loads directly is `breakble-tcolorbox.sty`. Do not load
`breakble-tcolorbox-runtime.sty` or the `breakble-tcb*.code.tex` files by hand;
keep them next to the wrapper.

This repository also contains a development and verification copy named
`tcolorbox/`. Do not install the whole repository or that `tcolorbox/` directory
into a TEXMF tree. For TEXMF installation, use
`texmf/tex/latex/breakble-tcolorbox/`.

In a document, load:

```tex
\usepackage[most]{breakble-tcolorbox}
```

Do not load the runtime files directly. The wrapper loads them.

## Manual Copy Installation

If you want to try the package without setting TeX search paths, use:

- `drop-in/`

The `drop-in/` directory contains a copy-ready `breakble-tcolorbox/` directory.
Copy that directory next to the `.tex` file that you want to compile. This keeps
the `.sty` and `.code.tex` files out of the top level of your document folder.

For example:

```text
your-document/
  main.tex
  breakble-tcolorbox/
    breakble-tcolorbox.sty
    breakble-tcolorbox-runtime.sty
    breakble-tcbbreakable.code.tex
    breakble-tcbskins.code.tex
    ...
```

With that layout, the document can simply load:

```tex
\usepackage[most]{breakble-tcolorbox/breakble-tcolorbox}
```

This method does not require `TEXINPUTS` or `mktexlsr`. It is convenient for
trying the package in one project.

## Project-Local Installation

If you want to keep this repository intact instead of copying the files by
hand, put the packaged TEXMF tree at the front of TeX's input path when
compiling.

Keep this repository somewhere on disk, then compile your document with:

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/texmf/tex/latex//:" latexmk -pdf main.tex
```

For example, if this repository is next to your document:

```sh
TEXINPUTS="../breakble-tcolorbox/texmf/tex/latex//:" latexmk -pdf main.tex
```

The `//` is important: it tells TeX to search that directory recursively.

You can verify what TeX will find with:

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/texmf/tex/latex//:" kpsewhich breakble-tcolorbox.sty
TEXINPUTS="/path/to/breakble-tcolorbox/texmf/tex/latex//:" kpsewhich tcolorbox.sty
```

`breakble-tcolorbox.sty` should point into this repository's
`texmf/tex/latex/breakble-tcolorbox/` directory. `tcolorbox.sty` should normally
continue to point to upstream `tcolorbox` from TeX Live, MacTeX, or MiKTeX.

## Personal TEXMF Installation

If you want TeX to find the package without setting `TEXINPUTS` every time, you
can install it into your personal TEXMF tree. A personal TEXMF tree is the
user-specific directory that your TeX system searches automatically.

This repository includes a TEXMF-ready tree:

```text
texmf/tex/latex/breakble-tcolorbox/
```

That directory intentionally does not contain a file named `tcolorbox.sty`.
Therefore ordinary `\usepackage{tcolorbox}` continues to load upstream
`tcolorbox`, while documents that say `\usepackage{breakble-tcolorbox}` use the
modified runtime.

First, find your personal TEXMF root. For TeX Live and MacTeX, this command is
the usual starting point on both macOS and Windows:

```sh
kpsewhich -var-value=TEXMFHOME
```

Common locations are:

| Environment | Common `TEXMFHOME` |
| --- | --- |
| macOS / MacTeX | `~/Library/texmf` |
| Linux / TeX Live | `~/texmf` |
| Windows / TeX Live | `C:\Users\<username>\texmf` |

Always prefer the value printed by `kpsewhich` on your own machine.

### macOS / Linux / TeX Live

```sh
TEXMFHOME="$(kpsewhich -var-value=TEXMFHOME)"
mkdir -p "$TEXMFHOME/tex/latex"
cp -R texmf/tex/latex/breakble-tcolorbox "$TEXMFHOME/tex/latex/"
```

### Windows / TeX Live

In PowerShell:

```powershell
$TEXMFHOME = kpsewhich -var-value=TEXMFHOME
New-Item -ItemType Directory -Force "$TEXMFHOME\tex\latex"

Copy-Item .\texmf\tex\latex\breakble-tcolorbox "$TEXMFHOME\tex\latex\" -Recurse -Force
```

### Windows / MiKTeX

MiKTeX may also provide `kpsewhich`, but many users manage user TEXMF roots
through MiKTeX Console.

1. Create a directory such as `C:\Users\<username>\texmf`.
2. Inside it, create `tex\latex`.
3. Copy this repository's `texmf\tex\latex\breakble-tcolorbox` directory into
   that `tex\latex` directory.
4. In MiKTeX Console, add the `texmf` directory as a root directory.
5. Refresh the file name database.

Command-line equivalents often look like:

```powershell
initexmf --register-root=C:\Users\<username>\texmf
initexmf --update-fndb
```

### Check The Installation

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

`kpsewhich breakble-tcolorbox.sty` should point into your personal TEXMF tree.
`kpsewhich tcolorbox.sty` should normally continue to point to upstream
`tcolorbox`.

In other words, after this installation, ordinary

```tex
\usepackage{tcolorbox}
```

loads upstream `tcolorbox`, and only documents that say

```tex
\usepackage[most]{breakble-tcolorbox}
```

use this modified runtime.

Useful search terms:

- `TeX Live TEXMFHOME`
- `MacTeX TEXMFHOME Library texmf`
- `Windows TeX Live TEXMFHOME kpsewhich`
- `MiKTeX local texmf root`
- `MiKTeX register root update fndb`
- `mktexlsr texhash difference`

## Site-Wide TEXMF Installation

For a shared TeX Live installation, use `TEXMFLOCAL`:

```sh
kpsewhich -var-value=TEXMFLOCAL
```

Then copy the TEXMF-ready directory into:

```text
<TEXMFLOCAL>/tex/latex/breakble-tcolorbox/
```

For example:

```sh
TEXMFLOCAL="$(kpsewhich -var-value=TEXMFLOCAL)"
sudo mkdir -p "$TEXMFLOCAL/tex/latex"
sudo cp -R texmf/tex/latex/breakble-tcolorbox "$TEXMFLOCAL/tex/latex/"
sudo mktexlsr
```

A site-wide install also keeps ordinary `\usepackage{tcolorbox}` pointing to
upstream `tcolorbox`. Choose it only when the administrator intends
`breakble-tcolorbox` to be available to all users of that TeX installation.

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

The same idea applies to the `drop-in/` method:

```tex
\usepackage[most]{breakble-tcolorbox/breakble-tcolorbox}
\usepackage{some-package-that-uses-tcolorbox}
```

In that case, later packages share the modified `tcolorbox` already loaded by
the wrapper. So when you can control package order, the `drop-in/` and
project-local `TEXINPUTS` methods let one document use the modified copy without
changing the default `tcolorbox` for the whole TeX environment.

If a document class or package loads `tcolorbox` before you have a chance to
load `breakble-tcolorbox`, the wrapper cannot replace it afterward. In that
case, changing the load order is the normal fix.

If the load order cannot be changed and you must force the modified copy for one
document, you can put the development `tcolorbox/` directory before upstream
`tcolorbox` on TeX's search path. This is an intentional override: ordinary
`\usepackage{tcolorbox}` will also resolve to the modified copy for that
compilation. Do not use this as the normal installation method.

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/tcolorbox//:" latexmk -pdf main.tex
```

When using this override, always confirm the `tcolorbox.sty` path in the `.log`
file or with `kpsewhich`.

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

### PDFs To Inspect

To see concrete output, start with these PDFs. They are included in the
repository.

- `docs/readme-demo/nested-breakable-comparison.pdf`:
  the README demo, with upstream `tcolorbox` on the left and
  `breakble-tcolorbox` on the right.
- `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf`:
  case-by-case comparison of nested `breakable` behavior.
- `verification/nested-behavior/pdf/a4-nested-title-mix.pdf`:
  title and no-title continuation mixtures, used to check spacing and overlap.
- `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf`:
  deeper title and no-title continuation mixtures.
- `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf`:
  stress cases covering mid-page starts, no-title continuation, multi-level
  nesting, and decorated upper/lower content.
- `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf`:
  titleless nesting at depths 2, 3, 4, 5, and 6.
- `verification/nested-behavior/pdf/a4-titleless-reach-reference.pdf`:
  a non-nested reference for how far ordinary `tcolorbox` content reaches
  toward the page bottom.

For upstream standalone examples, these PDFs put original output on the left
and breakble output on the right:

- `verification/example-parity/side-by-side/tcolorbox-example/tcolorbox-example__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-example-poster/tcolorbox-example-poster__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-tutorial-poster/tcolorbox-tutorial-poster__original-side-by-side.pdf`

### Full Manual Check

The upstream manual source is:

- `docs/tcolorbox/tcolorbox.tex`

That file includes the `docs/tcolorbox/tcolorbox.doc.*.tex` fragments. To
compile the full manual with both upstream `tcolorbox` and this package, run:

```sh
scripts/check-upstream-manual-parity.py
```

After the script runs, the main outputs are:

- breakble manual PDF:
  `verification/manual-parity/sources/breakble/tcolorbox.pdf`
- original manual PDF:
  `verification/manual-parity/sources/original/tcolorbox.pdf`
- side-by-side manual comparison PDF:
  `verification/manual-parity/side-by-side/tcolorbox-manual/tcolorbox-side-by-side.pdf`
- report:
  `verification/manual-parity/report.md`

`verification/manual-parity/` is ignored by Git because it contains generated
manual PDFs and rendered page images. Run the script locally to regenerate it.

Nested behavior report:

- `verification/nested-behavior/report.md`

Standalone example parity report:

- `verification/example-parity/report.md`

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
for the current run.

## Repository Layout

- `breakble-tcolorbox.sty`: public wrapper package
- `breakble-tcolorbox-runtime.sty`, `breakble-tcb*.code.tex`: modified runtime
  files renamed to avoid upstream filename shadowing
- `texmf/tex/latex/breakble-tcolorbox/`: copy-ready directory for personal or
  site-wide TEXMF installation
- `tcolorbox/`: development and verification copy of the modified upstream
  runtime files
- `vendor/tcolorbox-original/`: unmodified upstream runtime files used for parity checks
- `docs/nested-breakable-requirements.md`: development requirements for nested
  breakable behavior
- `docs/tcolorbox/`: upstream documentation, standalone example sources, and assets used by parity checks
- `docs/readme-demo/`: A4 sample used for the README comparison image
- `docs/samples/`: additional samples, including titleless nested boxes
- `drop-in/`: copy-ready folder for manual use next to a `.tex` file
- `scripts/build-safe-runtime-tree.py`: regenerates the renamed runtime files
  from `tcolorbox/`
- `verification/example-parity/`: generated parity report, source copies, and side-by-side PDFs
- `verification/nested-behavior/`: generated nested-breakable behavior reports and PDFs
- `verification/manual-parity/`: generated manual parity report, source copies, rendered pages, and side-by-side PDF

## Upstream

This package is based on Thomas F. Sturm's `tcolorbox`.

Upstream project:
<https://github.com/T-F-S/tcolorbox>

This repository is not affiliated with or endorsed by the upstream maintainer.
