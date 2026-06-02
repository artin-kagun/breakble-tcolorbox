#!/usr/bin/env python3
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "tcolorbox"
DROP_IN_DIR = ROOT / "drop-in" / "breakble-tcolorbox"
TEXMF_DIR = ROOT / "texmf" / "tex" / "latex" / "breakble-tcolorbox"
RUNTIME_NAME = "breakble-tcolorbox-runtime.sty"


def library_files() -> list[Path]:
    return sorted(SOURCE_DIR.glob("tcb*.code.tex"))


def prefixed(name: str) -> str:
    return f"breakble-{name}"


def patched_runtime() -> str:
    text = (SOURCE_DIR / "tcolorbox.sty").read_text(encoding="utf-8")
    for src in library_files():
        text = text.replace(src.name, prefixed(src.name))
    return clean_text(text)


def clean_text(text: str) -> str:
    return text.rstrip() + "\n"


def copy_text(src: Path, dst: Path) -> None:
    dst.write_text(clean_text(src.read_text(encoding="utf-8")), encoding="utf-8")


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def wrapper_text(*, drop_in: bool) -> str:
    text = (ROOT / "breakble-tcolorbox.sty").read_text(encoding="utf-8")
    if drop_in:
        text = text.replace(
            r"\ProvidesPackage{breakble-tcolorbox}",
            r"\ProvidesPackage{breakble-tcolorbox/breakble-tcolorbox}",
            1,
        )
    return text


def write_tree(path: Path, *, include_wrapper: bool, drop_in: bool = False) -> None:
    clean_dir(path)
    if include_wrapper:
        (path / "breakble-tcolorbox.sty").write_text(clean_text(wrapper_text(drop_in=drop_in)), encoding="utf-8")
    (path / RUNTIME_NAME).write_text(patched_runtime(), encoding="utf-8")
    for src in library_files():
        copy_text(src, path / prefixed(src.name))


def write_root_runtime() -> None:
    (ROOT / RUNTIME_NAME).write_text(patched_runtime(), encoding="utf-8")
    for src in library_files():
        copy_text(src, ROOT / prefixed(src.name))


def assert_no_shadow_names(path: Path) -> None:
    forbidden = {"tcolorbox.sty", *(src.name for src in library_files())}
    found = sorted(p.relative_to(path) for p in path.rglob("*") if p.name in forbidden)
    if found:
        joined = "\n".join(str(item) for item in found)
        raise SystemExit(f"shadow-prone upstream filenames remain in {path}:\n{joined}")


def assert_runtime_patched(path: Path) -> None:
    runtime = path / RUNTIME_NAME
    text = runtime.read_text(encoding="utf-8")
    missing = []
    for src in library_files():
        old = re.escape(src.name)
        new = prefixed(src.name)
        if re.search(rf"\{{{old}\}}", text):
            missing.append(src.name)
        if new not in text:
            missing.append(new)
    if missing:
        raise SystemExit(f"runtime library mapping is incomplete in {runtime}: {missing}")


def main() -> int:
    write_root_runtime()
    write_tree(DROP_IN_DIR, include_wrapper=True, drop_in=True)
    write_tree(TEXMF_DIR, include_wrapper=True)
    assert_no_shadow_names(DROP_IN_DIR)
    assert_no_shadow_names(TEXMF_DIR)
    assert_runtime_patched(ROOT)
    assert_runtime_patched(DROP_IN_DIR)
    assert_runtime_patched(TEXMF_DIR)
    print(f"wrote safe runtime files to {DROP_IN_DIR.relative_to(ROOT)}")
    print(f"wrote safe TEXMF tree to {TEXMF_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
