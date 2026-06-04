#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_ROOT = ROOT / "verification" / "nested-behavior" / "build" / "current-regression"
PDF_ROOT = ROOT / "verification" / "nested-behavior" / "pdf"
IMAGE_ROOT = ROOT / "verification" / "nested-behavior" / "images" / "current-regression"
REPORT_ROOT = ROOT / "verification" / "nested-behavior" / "reports"
TEXMFVAR = BUILD_ROOT / "texmf-var"


@dataclass(frozen=True)
class Job:
    key: str
    tex: str
    engine: str
    out_pdf: str
    required: bool = True


JOBS = [
    Job(
        "a4-proof-environment-continuous-inner-break-pdftex-viewable",
        "docs/samples/a4-proof-environment-continuous-inner-break-pdftex-viewable.tex",
        "pdflatex",
        "a4-proof-environment-continuous-inner-break-pdftex-viewable.pdf",
    ),
    Job(
        "a4-proof-environment-continuous-inner-break-uplatex",
        "docs/samples/a4-proof-environment-continuous-inner-break.tex",
        "uplatex",
        "a4-proof-environment-continuous-inner-break-uplatex.pdf",
    ),
    Job(
        "a4-proof-environment-continuous-inner-break-xelatex",
        "docs/samples/a4-proof-environment-continuous-inner-break.tex",
        "xelatex",
        "a4-proof-environment-continuous-inner-break-xelatex.pdf",
    ),
    Job(
        "a4-proof-environment-continuous-inner-break-lualatex",
        "docs/samples/a4-proof-environment-continuous-inner-break.tex",
        "lualatex",
        "a4-proof-environment-continuous-inner-break-lualatex.pdf",
        required=False,
    ),
    Job(
        "a4-proof-environment-nested-overlap-uplatex",
        "docs/samples/a4-proof-environment-nested-overlap.tex",
        "uplatex",
        "a4-proof-environment-nested-overlap-uplatex.pdf",
    ),
    Job(
        "a4-proof-environment-nested-overlap-xelatex",
        "docs/samples/a4-proof-environment-nested-overlap.tex",
        "xelatex",
        "a4-proof-environment-nested-overlap-xelatex.pdf",
    ),
    Job(
        "a4-japanese-nested-overlap-uplatex",
        "docs/samples/a4-japanese-nested-overlap.tex",
        "uplatex",
        "a4-japanese-nested-overlap-uplatex.pdf",
    ),
    Job(
        "a4-japanese-nested-overlap-xelatex",
        "docs/samples/a4-japanese-nested-overlap.tex",
        "xelatex",
        "a4-japanese-nested-overlap-xelatex.pdf",
    ),
    Job(
        "a4-japanese-nested-overlap-lualatex",
        "docs/samples/a4-japanese-nested-overlap.tex",
        "lualatex",
        "a4-japanese-nested-overlap-lualatex.pdf",
        required=False,
    ),
    Job(
        "a4-nested-display-math-overlap",
        "docs/samples/a4-nested-display-math-overlap.tex",
        "pdflatex",
        "a4-nested-display-math-overlap.pdf",
    ),
    Job(
        "a4-nested-display-math-overlap-xelatex",
        "docs/samples/a4-nested-display-math-overlap.tex",
        "xelatex",
        "a4-nested-display-math-overlap-xelatex.pdf",
    ),
    Job(
        "a4-nested-mixed-continuous",
        "docs/samples/a4-nested-mixed-continuous.tex",
        "pdflatex",
        "a4-nested-mixed-continuous.pdf",
    ),
    Job(
        "a4-titleless-nesting-depths",
        "docs/samples/titleless-nesting-depths.tex",
        "pdflatex",
        "a4-titleless-nesting-depths.pdf",
    ),
    Job(
        "a4-titleless-reach-reference",
        "docs/samples/titleless-reach-reference.tex",
        "pdflatex",
        "a4-titleless-reach-reference.pdf",
    ),
    Job(
        "b5-nested-breakable-smoke",
        "docs/samples/b5-nested-breakable-smoke.tex",
        "pdflatex",
        "b5-nested-breakable-smoke.pdf",
    ),
    Job(
        "a4-nested-parent-tail-regression-xelatex",
        "docs/samples/a4-nested-parent-tail-regression.tex",
        "xelatex",
        "a4-nested-parent-tail-regression-xelatex.pdf",
    ),
    Job(
        "a4-nested-parent-tail-regression-uplatex",
        "docs/samples/a4-nested-parent-tail-regression.tex",
        "uplatex",
        "a4-nested-parent-tail-regression-uplatex.pdf",
    ),
    Job(
        "a4-nested-parent-color-restore",
        "docs/samples/a4-nested-parent-color-restore.tex",
        "pdflatex",
        "a4-nested-parent-color-restore.pdf",
    ),
]


FATAL_LOG_PATTERNS = [
    re.compile(r"^!"),
    re.compile(r"Fatal error", re.I),
    re.compile(r"Emergency stop", re.I),
    re.compile(r"TeX capacity exceeded", re.I),
    re.compile(r"BTCDBG"),
]


def run(cmd: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None, stdout=None) -> None:
    subprocess.run(cmd, cwd=cwd, env=env, stdout=stdout, stderr=subprocess.STDOUT, check=True)


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env["TEXINPUTS"] = f"{ROOT}//:"
    env["TEXMFVAR"] = str(TEXMFVAR)
    env["LUATEX_CACHE"] = str(TEXMFVAR / "luatex-cache")
    return env


def compile_job(job: Job) -> tuple[Path | None, str | None]:
    tex = ROOT / job.tex
    build = BUILD_ROOT / job.key
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)
    TEXMFVAR.mkdir(parents=True, exist_ok=True)
    PDF_ROOT.mkdir(parents=True, exist_ok=True)
    stdout_path = build / "stdout.log"
    env = base_env()
    try:
        with stdout_path.open("w", encoding="utf-8") as stdout:
            if job.engine == "uplatex":
                run(
                    [
                        "uplatex",
                        "-interaction=nonstopmode",
                        "-halt-on-error",
                        "-file-line-error",
                        "-output-directory",
                        str(build),
                        str(tex),
                    ],
                    env=env,
                    stdout=stdout,
                )
                dvi = build / (tex.stem + ".dvi")
                run(["dvipdfmx", "-o", str(build / (tex.stem + ".pdf")), str(dvi)], env=env, stdout=stdout)
            else:
                run(
                    [
                        job.engine,
                        "-interaction=nonstopmode",
                        "-halt-on-error",
                        "-file-line-error",
                        "-output-directory",
                        str(build),
                        str(tex),
                    ],
                    env=env,
                    stdout=stdout,
                )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        if job.required:
            raise
        return None, f"optional {job.engine} build skipped/failed: {exc}"

    built_pdf = build / (tex.stem + ".pdf")
    if not built_pdf.exists():
        raise RuntimeError(f"missing PDF after {job.key}: {built_pdf}")
    out_pdf = PDF_ROOT / job.out_pdf
    shutil.copy2(built_pdf, out_pdf)
    scan_logs(build)
    render_pdf(job.key, out_pdf)
    return out_pdf, None


def scan_logs(build: Path) -> None:
    for path in list(build.glob("*.log")) + [build / "stdout.log"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            if any(pattern.search(line) for pattern in FATAL_LOG_PATTERNS):
                raise RuntimeError(f"{path.relative_to(ROOT)}: fatal log line: {line}")


def render_pdf(key: str, pdf: Path) -> None:
    out_dir = IMAGE_ROOT / key
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    prefix = out_dir / "page"
    run(["pdftoppm", "-q", "-r", "144", str(pdf), str(prefix)])
    for ppm in sorted(out_dir.glob("*.ppm")):
        png = ppm.with_suffix(".png")
        run(["sips", "-s", "format", "png", str(ppm), "--out", str(png)], stdout=subprocess.DEVNULL)
        ppm.unlink()


def pdf_pages(pdf: Path) -> int:
    out = subprocess.check_output(["pdfinfo", str(pdf)], cwd=ROOT, text=True)
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1])
    raise RuntimeError(f"could not read page count from {pdf}")


def render_ppm_for_metrics(pdf: Path, key: str, dpi: int = 72) -> list[Path]:
    out_dir = BUILD_ROOT / "metric-render" / key
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    prefix = out_dir / "page"
    run(["pdftoppm", "-q", "-r", str(dpi), str(pdf), str(prefix)])
    return sorted(out_dir.glob("*.ppm"))


def ppm_bottom_gap(path: Path, *, usable_fraction: float = 0.925) -> tuple[int, int, int, int]:
    data = path.read_bytes()
    if not data.startswith(b"P6"):
        raise RuntimeError(f"unsupported PPM: {path}")
    index = 2

    def skip_ws_and_comments(i: int) -> int:
        while i < len(data):
            if data[i] in b" \t\r\n":
                i += 1
                continue
            if data[i] == ord("#"):
                while i < len(data) and data[i] not in b"\r\n":
                    i += 1
                continue
            break
        return i

    def read_int(i: int) -> tuple[int, int]:
        i = skip_ws_and_comments(i)
        j = i
        while j < len(data) and data[j] in b"0123456789":
            j += 1
        return int(data[i:j]), j

    width, index = read_int(index)
    height, index = read_int(index)
    maxval, index = read_int(index)
    if maxval != 255:
        raise RuntimeError(f"unsupported PPM maxval {maxval}: {path}")
    index = skip_ws_and_comments(index)
    pixels = data[index:]
    usable_bottom = min(height - 1, max(1, int(height * usable_fraction)))
    last_nonwhite = -1
    threshold = 246
    for y in range(usable_bottom + 1):
        row = pixels[y * width * 3 : (y + 1) * width * 3]
        for x in range(0, len(row), 3):
            r, g, b = row[x], row[x + 1], row[x + 2]
            if r < threshold or g < threshold or b < threshold:
                last_nonwhite = y
                break
    if last_nonwhite < 0:
        return height, usable_bottom, 0, usable_bottom
    return height, usable_bottom, last_nonwhite, usable_bottom - last_nonwhite


def write_reach_report(pdf: Path, key: str, report_name: str) -> None:
    ppms = render_ppm_for_metrics(pdf, key)
    lines = [
        f"pdf={pdf.relative_to(ROOT)}",
        "page image_height_px measured_area_bottom_y_px content_bottom_y_px bottom_gap_px",
    ]
    for page_no, ppm in enumerate(ppms, start=1):
        height, usable_bottom, bottom, gap = ppm_bottom_gap(ppm)
        lines.append(f"{page_no} {height} {usable_bottom} {bottom} {gap}")
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / report_name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def pdftotext(pdf: Path) -> str:
    return subprocess.check_output(["pdftotext", str(pdf), "-"], cwd=ROOT, text=True, errors="replace")


def assert_parent_tail_markers(pdf: Path) -> None:
    text = pdftotext(pdf)
    markers = [
        "MARK-L2-AFTER-DEEP",
        "MARK-L2-TAIL",
        "MARK-L1-AFTER-L2",
        "MARK-L1-TAIL",
        "MARK-OUTER-AFTER-L1",
        "MARK-OUTER-END",
    ]
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise RuntimeError(f"{pdf.relative_to(ROOT)} missing markers: {', '.join(missing)}")


def assert_proof_first_page_not_empty(pdf: Path, key: str) -> None:
    ppm = render_ppm_for_metrics(pdf, key + "-first-page", dpi=72)[0]
    _height, usable_bottom, bottom, gap = ppm_bottom_gap(ppm)
    if bottom < int(usable_bottom * 0.80):
        raise RuntimeError(
            f"{pdf.relative_to(ROOT)} page 1 looks too empty: content bottom {bottom}/{usable_bottom}, gap {gap}px"
        )


def main() -> int:
    run([sys.executable, "scripts/build-safe-runtime-tree.py"])
    rows: list[str] = []
    optional_notes: list[str] = []
    built: dict[str, Path] = {}
    for job in JOBS:
        pdf, note = compile_job(job)
        if note:
            optional_notes.append(f"{job.key}: {note}")
            continue
        assert pdf is not None
        built[job.key] = pdf
        rows.append(f"{job.key} {job.engine} pages={pdf_pages(pdf)} pdf={pdf.relative_to(ROOT)}")

    for key in [
        "a4-proof-environment-continuous-inner-break-pdftex-viewable",
        "a4-proof-environment-continuous-inner-break-uplatex",
        "a4-proof-environment-continuous-inner-break-xelatex",
    ]:
        if key in built:
            assert_proof_first_page_not_empty(built[key], key)

    for key in [
        "a4-nested-parent-tail-regression-xelatex",
        "a4-nested-parent-tail-regression-uplatex",
    ]:
        if key in built:
            assert_parent_tail_markers(built[key])

    if "a4-titleless-nesting-depths" in built:
        write_reach_report(built["a4-titleless-nesting-depths"], "a4-titleless-nesting-depths", "titleless-nesting-depths-image-report.txt")
    if "a4-titleless-reach-reference" in built:
        write_reach_report(built["a4-titleless-reach-reference"], "a4-titleless-reach-reference", "titleless-reach-reference-image-report.txt")

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    report = ["nested_behavior_builds=ok", *rows]
    if optional_notes:
        report.append("optional_build_notes:")
        report.extend(optional_notes)
    (REPORT_ROOT / "nested-regression-build-report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
