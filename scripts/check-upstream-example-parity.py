#!/usr/bin/env python3
import filecmp
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "docs" / "tcolorbox"
BUILD_DIR = ROOT / "verification" / "example-parity"
ORIGINAL_INPUTS = f"{ROOT / 'vendor' / 'tcolorbox-original'}//:"
BREAKBLE_INPUTS = f"{ROOT}:"
USEPACKAGE_TCOLORBOX = re.compile(r"\\usepackage(\s*(?:\[[^\]]*\])?\s*)\{tcolorbox\}")


def run(cmd, *, cwd=None, env=None, stdout=None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    subprocess.check_call(cmd, cwd=cwd, env=merged_env, stdout=stdout)


def ensure_pygmentize() -> Path | None:
    found = shutil.which("pygmentize")
    if found:
        return Path(found)

    target = Path("/tmp/tcb-example-parity-pygments")
    bin_dir = Path("/tmp/tcb-example-parity-bin")
    marker = target / "pygments"
    if not marker.exists():
        run([sys.executable, "-m", "pip", "install", "--quiet", "--target", str(target), "Pygments"])
    bin_dir.mkdir(parents=True, exist_ok=True)
    wrapper = bin_dir / "pygmentize"
    wrapper.write_text(
        "#!/bin/sh\n"
        f"PYTHONPATH={target} exec {sys.executable} -m pygments.cmdline \"$@\"\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return wrapper


def discover_examples() -> list[Path]:
    candidates = sorted(
        set(DOC_DIR.glob("*example*.tex")) | set(DOC_DIR.glob("*tutorial*.tex"))
    )
    examples: list[Path] = []
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="replace")
        if "\\documentclass" in text and "\\begin{document}" in text:
            examples.append(path)
    return examples


def copy_doc_files(dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for src in DOC_DIR.iterdir():
        if src.is_file():
            shutil.copy2(src, dst / src.name)


def make_source_copy(src: Path, variant: str, work_dir: Path) -> Path:
    copy_doc_files(work_dir)
    stem = src.stem
    out = work_dir / f"{stem}__{variant}.tex"
    text = src.read_text(encoding="utf-8")
    if variant == "breakble":
        text, count = USEPACKAGE_TCOLORBOX.subn(
            r"\\usepackage\1{breakble-tcolorbox}", text, count=1
        )
        if count != 1:
            raise RuntimeError(f"could not rewrite tcolorbox package load in {src}")
    out.write_text(text, encoding="utf-8")
    return out


def compile_tex(tex: Path, texinputs: str, pygmentize: Path | None) -> Path:
    path = os.environ.get("PATH", "")
    if pygmentize:
        path = f"{pygmentize.parent}:{path}"
    (tex.parent / "_minted").mkdir(parents=True, exist_ok=True)
    run(
        [
            "latexmk",
            "-pdf",
            "-g",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={tex.parent}",
            tex.name,
        ],
        cwd=tex.parent,
        env={"TEXINPUTS": texinputs, "PATH": path},
        stdout=subprocess.DEVNULL,
    )
    pdf = tex.with_suffix(".pdf")
    if not pdf.exists():
        raise RuntimeError(f"missing PDF after compile: {pdf}")
    return pdf


def pdf_pages(pdf: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    if not match:
        raise RuntimeError(f"could not read page count from {pdf}")
    return int(match.group(1))


def render_pdf(pdf: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / "page"
    run(["pdftopng", "-r", "160", str(pdf), str(prefix)], stdout=subprocess.DEVNULL)
    return sorted(out_dir.glob("page-*.png"))


def make_side_by_side(original_pdf: Path, breakble_pdf: Path, out_dir: Path) -> Path:
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "make-a4-side-by-side-comparison.py"),
            str(original_pdf),
            str(breakble_pdf),
            str(out_dir),
        ],
        stdout=subprocess.DEVNULL,
    )
    return out_dir / f"{original_pdf.stem}-side-by-side.pdf"


def main() -> int:
    pygmentize = ensure_pygmentize()
    examples = discover_examples()
    if not examples:
        raise RuntimeError(f"no standalone examples found in {DOC_DIR}")

    (BUILD_DIR / "sources").mkdir(parents=True, exist_ok=True)
    manifest = BUILD_DIR / "example-manifest.txt"
    manifest.write_text(
        "\n".join(str(path.relative_to(ROOT)) for path in examples) + "\n",
        encoding="utf-8",
    )

    rows: list[dict[str, str]] = []
    failures: list[str] = []
    for src in examples:
        stem = src.stem
        original_dir = BUILD_DIR / "sources" / stem / "original"
        breakble_dir = BUILD_DIR / "sources" / stem / "breakble"
        original_tex = make_source_copy(src, "original", original_dir)
        breakble_tex = make_source_copy(src, "breakble", breakble_dir)

        row = {
            "example": str(src.relative_to(ROOT)),
            "original_tex": str(original_tex.relative_to(ROOT)),
            "breakble_tex": str(breakble_tex.relative_to(ROOT)),
        }
        try:
            original_pdf = compile_tex(original_tex, ORIGINAL_INPUTS, pygmentize)
            breakble_pdf = compile_tex(breakble_tex, BREAKBLE_INPUTS, pygmentize)
            row["original_pdf"] = str(original_pdf.relative_to(ROOT))
            row["breakble_pdf"] = str(breakble_pdf.relative_to(ROOT))

            original_pages = pdf_pages(original_pdf)
            breakble_pages = pdf_pages(breakble_pdf)
            row["pages"] = f"{original_pages}/{breakble_pages}"
            if original_pages != breakble_pages:
                failures.append(f"{stem}: page count differs original={original_pages} breakble={breakble_pages}")
                row["pixel"] = "not checked"
            else:
                original_pngs = render_pdf(original_pdf, BUILD_DIR / "render" / stem / "original")
                breakble_pngs = render_pdf(breakble_pdf, BUILD_DIR / "render" / stem / "breakble")
                differing = []
                for page, (left, right) in enumerate(zip(original_pngs, breakble_pngs), start=1):
                    if not filecmp.cmp(left, right, shallow=False):
                        differing.append(page)
                if differing:
                    failures.append(f"{stem}: pixel differs on pages {differing}")
                    row["pixel"] = "DIFF " + ",".join(map(str, differing))
                else:
                    row["pixel"] = "match"

            side_by_side = make_side_by_side(
                original_pdf,
                breakble_pdf,
                BUILD_DIR / "side-by-side" / stem,
            )
            row["side_by_side"] = str(side_by_side.relative_to(ROOT))
        except Exception as exc:
            failures.append(f"{stem}: {exc}")
            row["error"] = str(exc)
        rows.append(row)

    report_lines = [
        "# Upstream Example Parity Report",
        "",
        f"- upstream base: tcolorbox 6.10.0",
        f"- example count: {len(examples)}",
        f"- pygmentize: {pygmentize if pygmentize else 'system default'}",
        f"- status: {'PASS' if not failures else 'FAIL'}",
        "",
        "| example | pages original/breakble | pixel | side-by-side |",
        "| --- | ---: | --- | --- |",
    ]
    for row in rows:
        report_lines.append(
            "| {example} | {pages} | {pixel} | {side_by_side} |".format(
                example=row["example"],
                pages=row.get("pages", "-"),
                pixel=row.get("pixel", row.get("error", "-")).replace("|", "\\|"),
                side_by_side=row.get("side_by_side", "-"),
            )
        )
    if failures:
        report_lines.extend(["", "## Failures", ""])
        report_lines.extend(f"- {failure}" for failure in failures)
    (BUILD_DIR / "report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(BUILD_DIR / "report.md")
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
