#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "用法: bash install.sh <项目目录> [--replace]" >&2
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 2
fi

target_project="$1"
replace_mode="${2:-}"
if [[ -n "$replace_mode" && "$replace_mode" != "--replace" ]]; then
  usage
  exit 2
fi

if [[ ! -d "$target_project" ]]; then
  echo "目标项目不存在或不是目录: $target_project" >&2
  exit 2
fi

package_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_skill="$package_dir/skill"
skills_dir="$(cd "$target_project" && pwd)/.agents/skills"
destination="$skills_dir/higgsfield-ugc-workflows"

if [[ ! -f "$source_skill/SKILL.md" || ! -d "$source_skill/workflows" ]]; then
  echo "安装包不完整：缺少 skill/SKILL.md 或 skill/workflows。" >&2
  exit 2
fi

mkdir -p "$skills_dir"

if [[ -e "$destination" && "$replace_mode" != "--replace" ]]; then
  echo "目标已存在: $destination" >&2
  echo "确认更新后重新运行，并在末尾添加 --replace。" >&2
  exit 2
fi

stage_dir="$(mktemp -d "$skills_dir/.higgsfield-ugc-workflows.install.XXXXXX")"
cleanup() {
  if [[ -d "$stage_dir" ]]; then
    rm -rf "$stage_dir"
  fi
}
trap cleanup EXIT

cp -R "$source_skill/." "$stage_dir/"
python3 "$stage_dir/scripts/local_workflow_registry.py" catalog >/dev/null
python3 "$stage_dir/scripts/check_mode_contracts.py" >/dev/null

backup_path=""
if [[ -e "$destination" ]]; then
  backup_dir="$(cd "$target_project" && pwd)/.agents/skill-backups"
  mkdir -p "$backup_dir"
  backup_path="$(mktemp -d "$backup_dir/higgsfield-ugc-workflows.$(date +%Y%m%d%H%M%S).XXXXXX")/skill"
  mv "$destination" "$backup_path"
fi

mv "$stage_dir" "$destination"
trap - EXIT

echo "安装完成: $destination"
if [[ -n "$backup_path" ]]; then
  echo "旧版本备份: $backup_path"
fi
echo "请重新加载项目 Skills，然后使用 \$higgsfield-ugc-workflows。"
