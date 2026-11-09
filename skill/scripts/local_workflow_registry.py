#!/usr/bin/env python3
"""Read the captured Higgsfield UGC workflow tree through a small JSON CLI."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
from pathlib import Path


MAX_DIRECTORY_BYTES = 2_000_000


def find_source_root(script_path: Path) -> Path:
    skill_root = script_path.resolve().parents[1]
    embedded = skill_root / "workflows"
    if embedded.is_dir():
        return embedded.resolve()

    for parent in script_path.resolve().parents:
        candidate = parent / "higgs -ugc" / "higgsfield-ugc-workflows-v1.0"
        if candidate.is_dir():
            return candidate.resolve()
    raise FileNotFoundError("Cannot locate embedded workflows or the legacy v1.0 workflow snapshot")


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"Missing YAML frontmatter: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"Unclosed YAML frontmatter: {path}") from exc

    result: dict[str, str] = {}
    i = 1
    while i < end:
        line = lines[i]
        if line.startswith("description: |"):
            i += 1
            block: list[str] = []
            while i < end and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            result["description"] = "\n".join(block).strip()
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
        i += 1
    return result


def workflow_dirs(root: Path) -> list[Path]:
    return sorted(
        path for path in root.iterdir()
        if path.is_dir()
        and path.name.startswith("ugc-")
        and path.name.endswith("flow")
        and (path / "SKILL.md").is_file()
    )


def workflow_map(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for directory in workflow_dirs(root):
        meta = parse_frontmatter(directory / "SKILL.md")
        name = meta.get("name", directory.name)
        result[name] = directory.resolve()
    return result


def visible_files(workflow_root: Path) -> list[Path]:
    return sorted(
        path for path in workflow_root.rglob("*")
        if path.is_file() and not any(part.startswith(".") for part in path.relative_to(workflow_root).parts)
    )


def available_directories(workflow_root: Path, files: list[Path]) -> list[str]:
    directories = {"."}
    for path in files:
        parent = path.relative_to(workflow_root).parent
        while parent != Path("."):
            directories.add(parent.as_posix())
            parent = parent.parent
    return sorted(directories)


def catalog(root: Path) -> dict:
    workflows = []
    for directory in workflow_dirs(root):
        meta = parse_frontmatter(directory / "SKILL.md")
        item = {
            "name": meta.get("name", directory.name),
            "description": meta.get("description", ""),
        }
        if meta.get("version"):
            item["version"] = meta["version"]
        workflows.append(item)
    return {
        "mode": "catalog",
        "source": "local_snapshot",
        "workflows": workflows,
        "how_to_load_more": "Run instructions <workflow> to load its local SKILL.md.",
    }


def instructions(root: Path, workflow: str) -> dict:
    workflows = workflow_map(root)
    if workflow not in workflows:
        return {"mode": "error", "source": "local_snapshot", "error": f"Unknown workflow: {workflow}"}
    workflow_root = workflows[workflow]
    files = visible_files(workflow_root)
    meta = parse_frontmatter(workflow_root / "SKILL.md")
    result = {
        "mode": "workflow",
        "source": "local_snapshot",
        "workflow": workflow,
        "instructions_markdown": (workflow_root / "SKILL.md").read_text(encoding="utf-8"),
        "available_paths": [path.relative_to(workflow_root).as_posix() for path in files],
        "available_directories": available_directories(workflow_root, files),
    }
    if meta.get("version"):
        result["version"] = meta["version"]
    return result


def resolve_bundle_path(root: Path, workflow: str, relative_path: str) -> tuple[Path, Path]:
    workflows = workflow_map(root)
    if workflow not in workflows:
        raise ValueError(f"Unknown workflow: {workflow}")
    workflow_root = workflows[workflow]
    target = (workflow_root / relative_path).resolve()
    try:
        target.relative_to(workflow_root)
    except ValueError as exc:
        raise ValueError("Path traversal outside the selected workflow is forbidden") from exc
    if any(part.startswith(".") for part in target.relative_to(workflow_root).parts):
        raise ValueError("Hidden files are not available")
    if not target.exists():
        raise ValueError(f"Path does not exist: {relative_path}")
    return workflow_root, target


def file_record(workflow_root: Path, path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    return {
        "path": path.relative_to(workflow_root).as_posix(),
        "content": content,
        "mime_type": mimetypes.guess_type(path.name)[0] or "text/plain",
        "size_bytes": len(content.encode("utf-8")),
    }


def bundle(root: Path, workflow: str, relative_path: str, include_contents: bool) -> dict:
    workflow_root, target = resolve_bundle_path(root, workflow, relative_path)
    normalized = target.relative_to(workflow_root).as_posix() or "."
    if target.is_file():
        record = file_record(workflow_root, target)
        return {"kind": "file", "workflow": workflow, **record}

    files = visible_files(target)
    total = sum(path.stat().st_size for path in files)
    if include_contents and total > MAX_DIRECTORY_BYTES:
        raise ValueError(f"Directory content exceeds {MAX_DIRECTORY_BYTES} bytes")
    result = {
        "kind": "directory",
        "workflow": workflow,
        "path": normalized,
        "entries": sorted(path.name for path in target.iterdir() if not path.name.startswith(".")),
        "file_count": len(files),
        "total_bytes": total,
        "max_directory_bytes": MAX_DIRECTORY_BYTES,
    }
    if include_contents:
        result["files"] = [file_record(workflow_root, path) for path in files]
    return result


def presets(root: Path, kind: str) -> dict:
    preset_path = root / "marketing-studio-public-presets.json"
    data = json.loads(preset_path.read_text(encoding="utf-8"))
    keys = ["hooks", "settings"] if kind == "all" else [kind]
    return {
        "mode": "presets",
        "source": "local_snapshot",
        "captured_at": data.get("captured_at"),
        "scope": data.get("scope"),
        "items": {key: data.get(key, []) for key in keys},
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, help="Override the captured workflow root")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("catalog")
    instructions_parser = subparsers.add_parser("instructions")
    instructions_parser.add_argument("workflow")
    bundle_parser = subparsers.add_parser("bundle")
    bundle_parser.add_argument("workflow")
    bundle_parser.add_argument("path")
    bundle_parser.add_argument("--include-contents", action="store_true")
    presets_parser = subparsers.add_parser("presets")
    presets_parser.add_argument("kind", choices=("all", "hooks", "settings"), default="all", nargs="?")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = (args.source_root or find_source_root(Path(__file__))).resolve()
    try:
        if args.command == "catalog":
            result = catalog(root)
        elif args.command == "instructions":
            result = instructions(root, args.workflow)
        elif args.command == "bundle":
            result = bundle(root, args.workflow, args.path, args.include_contents)
        else:
            result = presets(root, args.kind)
    except (FileNotFoundError, UnicodeDecodeError, ValueError) as exc:
        result = {"mode": "error", "source": "local_snapshot", "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
