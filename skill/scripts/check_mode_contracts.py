#!/usr/bin/env python3
"""Check that zero-credit and low-credit workflow contracts remain complete."""

from __future__ import annotations

import json
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
WORKSPACE = SKILL_DIR.parents[2]
EMBEDDED = SKILL_DIR / "workflows"
LEGACY = WORKSPACE / "higgs -ugc" / "higgsfield-ugc-workflows-v1.0"
SNAPSHOT = EMBEDDED if EMBEDDED.is_dir() else LEGACY


def require_text(path: Path, needles: list[str], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path}")
        return
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{path}: missing contract text: {needle}")


def main() -> int:
    errors: list[str] = []
    entry = SKILL_DIR / "SKILL.md"
    zero = SKILL_DIR / "references" / "reference-only-prompt-mode.md"
    low = SKILL_DIR / "references" / "soul-only-prompt-mode.md"

    require_text(
        entry,
        [
            "reference-only-prompt",
            "soul-only-prompt",
            "A low-credit request with both existing local images",
            "explicitly permits generating one creator image",
        ],
        errors,
    )
    require_text(
        zero,
        [
            "Make no Higgsfield or other remote generation calls",
            "character_local_path",
            "product_source_path",
            "structured text board",
            "final video-generation prompt",
            "post-generation QA checklist",
            "content_color_evidence",
        ],
        errors,
    )
    require_text(
        low,
        [
            "generate_image",
            "model: soul_2",
            "save_creator_image.py",
            "structured text board",
            "final video-generation prompt",
            "post-generation QA checklist",
            "content_color_evidence",
        ],
        errors,
    )

    child_files = {
        "ugc-flow": ["ugc-board.md", "ugc-clip.md"],
        "ugc-try-on-flow": ["ugc-try-board.md", "ugc-try-clip.md"],
        "ugc-tutorial-flow": ["ugc-tutorial-boards.md", "ugc-tutorial-clip-prompt.md"],
        "ugc-unboxing-flow": ["ugc-unboxing-board.md", "ugc-unboxing-clip.md"],
    }
    for workflow, files in child_files.items():
        root = SNAPSHOT / workflow
        if not (root / "SKILL.md").is_file():
            errors.append(f"missing child workflow: {workflow}")
        if not (root / "references" / "product-intake.md").is_file():
            errors.append(f"missing product intake: {workflow}")
        for filename in files:
            if not (root / "references" / filename).is_file():
                errors.append(f"missing {workflow} reference: {filename}")

    result = {
        "valid": not errors,
        "modes": ["reference-only-prompt", "soul-only-prompt"],
        "supported_workflows": list(child_files),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
