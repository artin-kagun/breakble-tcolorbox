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
BUILD_DIR = ROOT / "verification" / "manual-parity"
ORIGINAL_INPUTS = f".:{ROOT / 'vendor' / 'tcolorbox-original'}//:"
BREAKBLE_INPUTS = f".:{ROOT}:{ROOT / 'tcolorbox'}//:"
MAIN_TEX = "tcolorbox.tex"
S_MAIN_PACKAGE_LOAD = r"\RequirePackage{\tcbpkgprefix tcolorbox}"


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    stdout=None,
    stderr=None,
) -> None:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    subprocess.check_call(cmd, cwd=cwd, env=merged_env, stdout=stdout, stderr=stderr)


def ensure_pygmentize() -> Path | None:
    found = shutil.which("pygmentize")
    if found:
        return Path(found)

    target = Path("/tmp/tcb-manual-parity-pygments")
    bin_dir = Path("/tmp/tcb-manual-parity-bin")
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


def doc_tex_files() -> list[Path]:
    return sorted(DOC_DIR.glob("*.tex"))


def manual_include_files(main_text: str) -> list[str]:
    names: list[str] = []
    for command, arg in re.findall(r"\\(input|include)\{([^}]+)\}", main_text):
        path = arg if arg.endswith(".tex") else f"{arg}.tex"
        names.append(path)
    return names


def copy_doc_tree(dst: Path, variant: str) -> Path:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for src in DOC_DIR.iterdir():
        if src.is_file():
            if src.name == "tcolorbox.pdf":
                continue
            shutil.copy2(src, dst / src.name)

    main = dst / MAIN_TEX
    if variant == "breakble":
        style = dst / "tcolorbox.doc.s_main.sty"
        text = style.read_text(encoding="utf-8")
        if S_MAIN_PACKAGE_LOAD not in text:
            raise RuntimeError(f"could not find package load in {style}")
        style.write_text(
            text.replace(S_MAIN_PACKAGE_LOAD, r"\RequirePackage{breakble-tcolorbox}", 1),
            encoding="utf-8",
        )
    return main


def compile_manual(tex: Path, texinputs: str, pygmentize: Path | None) -> Path:
    path = os.environ.get("PATH", "")
    if pygmentize:
        path = f"{pygmentize.parent}:{path}"
    (tex.parent / "_minted").mkdir(parents=True, exist_ok=True)
    (tex.parent / "external").mkdir(parents=True, exist_ok=True)
    (tex.parent / "solutions").mkdir(parents=True, exist_ok=True)
    stdout_log = tex.with_suffix(".manual-build.log")
    base_env = {"TEXINPUTS": texinputs, "PATH": path}

    def run_step(label: str, cmd: list[str], stream) -> None:
        stream.write(f"\n===== {label}: {' '.join(cmd)} =====\n")
        stream.flush()
        run(
            cmd,
            cwd=tex.parent,
            env=base_env,
            stdout=stream,
            stderr=subprocess.STDOUT,
        )

    with stdout_log.open("w", encoding="utf-8", errors="replace") as stream:
        try:
            run_step(
                "pdflatex pass 1",
                ["pdflatex", "-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-recorder", tex.name],
                stream,
            )
            run_step("biber", ["biber", tex.stem], stream)
            run_step("makeindex pass 1", ["makeindex", f"{tex.stem}.idx"], stream)
            for pass_no in range(2, 5):
                run_step(
                    f"pdflatex pass {pass_no}",
                    ["pdflatex", "-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-recorder", tex.name],
                    stream,
                )
                if pass_no < 4:
                    run_step(
                        f"makeindex pass {pass_no}",
                        ["makeindex", f"{tex.stem}.idx"],
                        stream,
                    )
        except subprocess.CalledProcessError as exc:
            log_tail = ""
            tex_log = tex.with_suffix(".log")
            if tex_log.exists():
                log_tail = "\n".join(tex_log.read_text(encoding="utf-8", errors="replace").splitlines()[-80:])
            stdout_tail = "\n".join(stdout_log.read_text(encoding="utf-8", errors="replace").splitlines()[-80:])
            raise RuntimeError(
                f"manual build failed with exit status {exc.returncode}\n"
                f"stdout tail:\n{stdout_tail}\n"
                f"tex log tail:\n{log_tail}"
            ) from exc
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
    if out_dir.exists():
        shutil.rmtree(out_dir)
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


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    main_src = DOC_DIR / MAIN_TEX
    if not main_src.exists():
        raise RuntimeError(f"manual source not found: {main_src}")

    main_text = main_src.read_text(encoding="utf-8")
    includes = manual_include_files(main_text)
    missing = [name for name in includes if not (DOC_DIR / name).exists()]
    if missing:
        raise RuntimeError(f"manual includes missing files: {', '.join(missing)}")

    pygmentize = ensure_pygmentize()
    source_root = BUILD_DIR / "sources"
    original_tex = copy_doc_tree(source_root / "original", "original")
    breakble_tex = copy_doc_tree(source_root / "breakble", "breakble")

    failures: list[str] = []
    rows: list[tuple[str, str]] = [
        ("upstream base", "tcolorbox 6.10.0"),
        ("doc tex files", str(len(doc_tex_files()))),
        ("manual include/input files", str(len(includes))),
        ("pygmentize", str(pygmentize if pygmentize else "system default")),
        ("original source", relative(original_tex)),
        ("breakble source", relative(breakble_tex)),
    ]

    try:
        original_pdf = compile_manual(original_tex, ORIGINAL_INPUTS, pygmentize)
        breakble_pdf = compile_manual(breakble_tex, BREAKBLE_INPUTS, pygmentize)
        rows.append(("original pdf", relative(original_pdf)))
        rows.append(("breakble pdf", relative(breakble_pdf)))

        original_pages = pdf_pages(original_pdf)
        breakble_pages = pdf_pages(breakble_pdf)
        rows.append(("pages original/breakble", f"{original_pages}/{breakble_pages}"))
        differing: list[int] = []
        if original_pages != breakble_pages:
            failures.append(f"page count differs original={original_pages} breakble={breakble_pages}")
        else:
            original_pngs = render_pdf(original_pdf, BUILD_DIR / "render" / "original")
            breakble_pngs = render_pdf(breakble_pdf, BUILD_DIR / "render" / "breakble")
            for page, (left, right) in enumerate(zip(original_pngs, breakble_pngs), start=1):
                if not filecmp.cmp(left, right, shallow=False):
                    differing.append(page)
            if differing:
                failures.append(f"pixel differs on pages {differing}")
                rows.append(("pixel", "DIFF " + ",".join(map(str, differing))))
            else:
                rows.append(("pixel", "match"))

        side_by_side = make_side_by_side(
            original_pdf,
            breakble_pdf,
            BUILD_DIR / "side-by-side" / "tcolorbox-manual",
        )
        rows.append(("side-by-side", relative(side_by_side)))
    except Exception as exc:
        failures.append(str(exc))

    manifest = BUILD_DIR / "manual-manifest.txt"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "\n".join(
            [
                "# all TeX files in docs/tcolorbox",
                *[relative(path) for path in doc_tex_files()],
                "",
                "# files read by tcolorbox.tex through input/include",
                *includes,
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    rows.append(("manifest", relative(manifest)))

    report_lines = [
        "# Upstream Manual Parity Report",
        "",
        f"- status: {'PASS' if not failures else 'FAIL'}",
        "",
        "| item | value |",
        "| --- | --- |",
    ]
    for key, value in rows:
        report_lines.append(f"| {key} | {value} |")
    if failures:
        report_lines.extend(["", "## Failures", ""])
        report_lines.extend(f"- {failure}" for failure in failures)
    report = BUILD_DIR / "report.md"
    report.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(report)
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
