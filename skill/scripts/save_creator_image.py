#!/usr/bin/env python3
"""Archive one completed Soul creator image into the project-local model folder."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path


def project_root(script_path: Path) -> Path:
    return script_path.resolve().parents[4]


def safe_stem(url: str, job_id: str | None) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Creator image URL must use HTTPS")
    source = Path(parsed.path).name
    suffix = Path(source).suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
        suffix = ".png"
    stem = Path(source).stem or "soul-creator"
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-._")
    if not stem:
        stem = "soul-creator"
    if job_id and job_id[:8] not in stem:
        stem = f"{stem}-{job_id[:8]}"
    return stem, suffix


def validate_image(path: Path) -> str:
    size = path.stat().st_size
    if size < 1024:
        raise ValueError(f"Downloaded file is too small to be an image: {size} bytes")
    header = path.read_bytes()[:12]
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        return "webp"
    raise ValueError("Downloaded file does not have a supported image signature")


def download(url: str, destination: Path) -> tuple[int, str]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Codex creator archiver/1.0"})
    fd, temporary_name = tempfile.mkstemp(prefix=".creator-", dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as output, urllib.request.urlopen(request, timeout=120) as response:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        image_type = validate_image(temporary)
        os.replace(temporary, destination)
        return destination.stat().st_size, image_type
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Completed Soul image HTTPS URL")
    parser.add_argument("--job-id", help="Soul generation job id, used for stable naming")
    parser.add_argument("--output-dir", type=Path, help="Override the project-local archive folder")
    args = parser.parse_args()

    root = project_root(Path(__file__))
    output_dir = (args.output_dir or root / "higgs -ugc" / "模特图").resolve()
    stem, suffix = safe_stem(args.url, args.job_id)
    destination = output_dir / f"{stem}{suffix}"
    size, image_type = download(args.url, destination)
    print(json.dumps({
        "character_local_path": str(destination),
        "bytes": size,
        "image_type": image_type,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
