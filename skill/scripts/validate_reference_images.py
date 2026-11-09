#!/usr/bin/env python3
"""Validate the two local images required by reference-only-prompt mode."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def image_type(path: Path) -> str:
    header = path.read_bytes()[:16]
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    raise ValueError(f"Unsupported or invalid image signature: {path}")


def validate(path_text: str, workspace_root: Path, role: str) -> dict[str, object]:
    path = Path(path_text).expanduser().resolve()
    try:
        path.relative_to(workspace_root)
    except ValueError as exc:
        raise ValueError(f"{role} image is outside the workspace root: {path}") from exc
    if not path.is_file():
        raise ValueError(f"{role} image is not a regular file: {path}")
    size = path.stat().st_size
    if size <= 0:
        raise ValueError(f"{role} image is empty: {path}")
    return {
        "role": role,
        "absolute_path": str(path),
        "bytes": size,
        "image_type": image_type(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--creator", required=True)
    parser.add_argument("--product", required=True)
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).expanduser().resolve()
    if not workspace_root.is_dir():
        raise SystemExit(f"Workspace root is not a directory: {workspace_root}")

    try:
        result = {
            "mode": "reference-only-prompt",
            "valid": True,
            "references": [
                validate(args.creator, workspace_root, "creator"),
                validate(args.product, workspace_root, "product"),
            ],
        }
    except ValueError as exc:
        print(json.dumps({"mode": "reference-only-prompt", "valid": False, "error": str(exc)}))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
