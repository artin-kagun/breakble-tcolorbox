# Modifications

This repository contains an unofficial modification of `tcolorbox` 6.10.0.

Base upstream:

- Project: <https://github.com/T-F-S/tcolorbox>
- Tag: `v6.10.0`
- Commit: `057ff62f77aeef399251ac4fca98d1a20c36ab32`
- Original license: LPPL 1.3c or later

Changed or added files:

- `breakble-tcolorbox.sty`
  - New wrapper package.
  - Passes options to the modified `tcolorbox` runtime.
  - Errors if `tcolorbox` was already loaded directly.
  - Loads the modified runtime from a package-specific filename so TEXMF installs do not shadow ordinary `tcolorbox.sty`.
- `breakble-tcolorbox-runtime.sty` and `breakble-tcb*.code.tex`
  - Generated from the modified runtime sources under `tcolorbox/`.
  - Use package-specific filenames instead of upstream names such as `tcolorbox.sty` and `tcbbreakable.code.tex`.
  - Allow personal or site-wide TEXMF installation without redirecting ordinary `\usepackage{tcolorbox}`.
- `tcolorbox/tcolorbox.sty`
  - Marks the package as an unofficial `breakble-tcolorbox` modification in `\ProvidesPackage`.
  - Tracks whether each active tcolorbox layer is breakable.
  - Allows the normal `breakable` key for a nested box only when the immediate parent layer is breakable.
  - Tracks whether a nested breakable child should use the new parent-managed behavior.
  - Preserves `enforce breakable` as the upstream explicit escape hatch.
- `tcolorbox/tcbbreakable.code.tex`
  - Caps parent-managed nested fragments using the parent breakable context.
  - Suppresses the child fragment's own physical page breaks only for the new normal nested-breakable case.
  - Adjusts fragment edge accounting so parent and child break fragments do not create large vertical gaps.
- `texmf/tex/latex/breakble-tcolorbox/`
  - Copy-ready TEXMF installation tree using the renamed runtime files.
- `drop-in/breakble-tcolorbox/`
  - Copy-ready project-local tree using the renamed runtime files.
- `scripts/build-safe-runtime-tree.py`
  - Regenerates the renamed runtime files from `tcolorbox/`.

Files copied unchanged from upstream are kept under `vendor/tcolorbox-original/`
for verification.

Generated verification artifacts are in `verification/example-parity/` and
`verification/manual-parity/`.
