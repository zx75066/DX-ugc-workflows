#!/usr/bin/env bash
set -euo pipefail

package_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$package_dir/skill"

if [[ ! -f "$skill_dir/SKILL.md" || ! -d "$skill_dir/workflows" ]]; then
  echo "安装包结构无效。" >&2
  exit 2
fi

python3 - "$package_dir" <<'PY'
from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1]).resolve()
manifest = root / "SHA256SUMS.txt"
if not manifest.is_file():
    raise SystemExit("缺少 SHA256SUMS.txt；维护者请先运行 python3 scripts/package_release.py。")
count = 0
for line in manifest.read_text(encoding="utf-8").splitlines():
    expected, relative = line.split("  ", 1)
    target = (root / relative).resolve()
    if root not in target.parents or not target.is_file():
        raise SystemExit(f"校验文件路径无效或不存在: {relative}")
    if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
        raise SystemExit(f"文件校验失败: {relative}")
    count += 1
print(f"SHA-256 文件校验通过: {count} 个文件")
PY

if find "$package_dir" -type l | grep -q .; then
  echo "安装包中不应包含符号链接。" >&2
  exit 2
fi

workflow_count="$(find "$skill_dir/workflows" -mindepth 1 -maxdepth 1 -type d -name 'ugc-*flow' | wc -l | tr -d ' ')"
if [[ "$workflow_count" != "6" ]]; then
  echo "工作流数量错误：预期 6，实际 ${workflow_count}。" >&2
  exit 2
fi

python3 "$skill_dir/scripts/local_workflow_registry.py" catalog
python3 "$skill_dir/scripts/check_mode_contracts.py"
echo "安装包验证通过。"
