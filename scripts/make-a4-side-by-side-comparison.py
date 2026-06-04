#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from pathlib import Path


LOG_PATTERN = re.compile(
    r"(^!|LaTeX Error|Package .*Warning|Package .*Error|Fatal|Emergency stop|"
    r"Overfull|Underfull|Undefined control sequence|LaTeX Warning|Font Warning)",
    re.MULTILINE,
)


def pdf_pages(pdf: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    if not match:
        raise RuntimeError(f"could not read page count from {pdf}")
    return int(match.group(1))


def latex_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/")


def include_page(pdf: str, page: int, total_pages: int, missing_label: str) -> str:
    if page <= total_pages:
        return (
            rf"\fcolorbox{{black!45}}{{white}}{{\includegraphics[page={page},"
            rf"width=0.96\linewidth,height=0.86\textheight,keepaspectratio]{{{pdf}}}}}"
        )
    return (
        r"\fcolorbox{black!20}{black!3}{"
        r"\begin{minipage}[c][0.86\textheight][c]{0.86\linewidth}"
        rf"\centering\small {missing_label}: no page {page}"
        r"\end{minipage}}"
    )


def include_image(path: Path, label: str) -> str:
    if path.exists():
        return (
            rf"\fcolorbox{{black!45}}{{white}}{{\includegraphics["
            rf"width=0.96\linewidth,height=0.86\textheight,keepaspectratio]"
            rf"{{{latex_path(path)}}}}}"
        )
    return (
        r"\fcolorbox{black!20}{black!3}{"
        r"\begin{minipage}[c][0.86\textheight][c]{0.86\linewidth}"
        rf"\centering\small {label}: missing image"
        r"\end{minipage}}"
    )


def write_comparison_tex(
    original_pdf: Path,
    breakble_pdf: Path,
    out_dir: Path,
    stem: str,
    original_pages: int,
    breakble_pages: int,
) -> Path:
    tex = out_dir / f"{stem}.tex"
    original = latex_path(original_pdf)
    breakble = latex_path(breakble_pdf)
    pages = max(original_pages, breakble_pages)
    parts = [
        r"\documentclass[a4paper,landscape]{article}",
        r"\usepackage[margin=8mm]{geometry}",
        r"\usepackage{graphicx}",
        r"\usepackage{xcolor}",
        r"\pagestyle{empty}",
        r"\setlength{\parindent}{0pt}",
        r"\setlength{\fboxsep}{1.5mm}",
        r"\setlength{\fboxrule}{0.35pt}",
        r"\begin{document}",
    ]
    for page in range(1, pages + 1):
        parts.extend(
            [
                rf"\noindent\textbf{{A4 comparison page {page}: original left, breakble right}}\par\smallskip",
                r"\noindent",
                r"\begin{minipage}[t]{0.492\linewidth}\centering",
                r"\textbf{Original tcolorbox}\par\smallskip",
                include_page(original, page, original_pages, "Original tcolorbox"),
                r"\end{minipage}\hfill",
                r"\begin{minipage}[t]{0.492\linewidth}\centering",
                r"\textbf{breakble-tcolorbox}\par\smallskip",
                include_page(breakble, page, breakble_pages, "breakble-tcolorbox"),
                r"\end{minipage}",
            ]
        )
        if page != pages:
            parts.append(r"\clearpage")
    parts.append(r"\end{document}")
    tex.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return tex


def render_pdf_to_pngs(pdf: Path, out_dir: Path) -> list[Path]:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / "page"
    subprocess.check_call(["pdftopng", "-r", "120", str(pdf), str(prefix)], stdout=subprocess.DEVNULL)
    return sorted(out_dir.glob("page-*.png"))


def write_png_comparison_tex(
    original_pngs: list[Path],
    breakble_pngs: list[Path],
    out_dir: Path,
    stem: str,
) -> Path:
    tex = out_dir / f"{stem}.tex"
    pages = max(len(original_pngs), len(breakble_pngs))
    parts = [
        r"\documentclass[a4paper,landscape]{article}",
        r"\usepackage[margin=8mm]{geometry}",
        r"\usepackage{graphicx}",
        r"\usepackage{xcolor}",
        r"\pagestyle{empty}",
        r"\setlength{\parindent}{0pt}",
        r"\setlength{\fboxsep}{1.5mm}",
        r"\setlength{\fboxrule}{0.35pt}",
        r"\begin{document}",
    ]
    for page in range(1, pages + 1):
        original = original_pngs[page - 1] if page <= len(original_pngs) else Path()
        breakble = breakble_pngs[page - 1] if page <= len(breakble_pngs) else Path()
        parts.extend(
            [
                rf"\noindent\textbf{{A4 comparison page {page}: original left, breakble right}}\par\smallskip",
                r"\noindent",
                r"\begin{minipage}[t]{0.492\linewidth}\centering",
                r"\textbf{Original tcolorbox}\par\smallskip",
                include_image(original, f"Original tcolorbox page {page}"),
                r"\end{minipage}\hfill",
                r"\begin{minipage}[t]{0.492\linewidth}\centering",
                r"\textbf{breakble-tcolorbox}\par\smallskip",
                include_image(breakble, f"breakble-tcolorbox page {page}"),
                r"\end{minipage}",
            ]
        )
        if page != pages:
            parts.append(r"\clearpage")
    parts.append(r"\end{document}")
    tex.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return tex


def check_log(log: Path) -> None:
    text = log.read_text(encoding="utf-8", errors="replace")
    match = LOG_PATTERN.search(text)
    if match:
        raise RuntimeError(f"log problem in {log}: {match.group(0)}")


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: make-a4-side-by-side-comparison.py ORIGINAL.pdf BREAKBLE.pdf OUT_DIR",
            file=sys.stderr,
        )
        return 2

    original_pdf = Path(sys.argv[1])
    breakble_pdf = Path(sys.argv[2])
    out_dir = Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    original_pages = pdf_pages(original_pdf)
    breakble_pages = pdf_pages(breakble_pdf)

    stem = original_pdf.stem + "-side-by-side"
    tex = write_comparison_tex(
        original_pdf,
        breakble_pdf,
        out_dir,
        stem,
        original_pages,
        breakble_pages,
    )
    latexmk_cmd = [
        "latexmk",
        "-pdf",
        "-g",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={out_dir}",
        str(tex),
    ]
    use_png_fallback = max(original_pages, breakble_pages) > 100
    try:
        if use_png_fallback:
            raise subprocess.CalledProcessError(1, latexmk_cmd)
        subprocess.check_call(latexmk_cmd, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        original_pngs = render_pdf_to_pngs(original_pdf, out_dir / "render-original")
        breakble_pngs = render_pdf_to_pngs(breakble_pdf, out_dir / "render-breakble")
        stem = original_pdf.stem + "-side-by-side-png"
        tex = write_png_comparison_tex(original_pngs, breakble_pngs, out_dir, stem)
        subprocess.check_call(
            [
                "latexmk",
                "-pdf",
                "-g",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-outdir={out_dir}",
                str(tex),
            ],
            stdout=subprocess.DEVNULL,
        )
    check_log(out_dir / f"{stem}.log")
    print(out_dir / f"{stem}.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
