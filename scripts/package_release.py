#!/usr/bin/env python3
"""Build a UTF-8 ZIP and SHA-256 manifest from the public repository files."""

from pathlib import Path
import hashlib
import zipfile


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "dist", "__pycache__", "node_modules", ".venv", ".agents"}


def public_files():
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED for part in relative.parts):
            continue
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.name == ".env" or path.name.startswith(".env."):
            continue
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink: {relative}")
        if path.is_file() and path.name != "SHA256SUMS.txt":
            yield path


def main():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    files = list(public_files())
    manifest = ROOT / "SHA256SUMS.txt"
    manifest.write_text("".join(
        f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n"
        for p in files
    ), encoding="utf-8")
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"DX-ugc-workflows-v{version}.zip"
    prefix = f"DX-ugc-workflows-v{version}"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(files + [manifest]):
            bundle.write(path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = output / "SHA256SUMS.txt"
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Built {archive.name}: {len(files) + 1} files")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()
