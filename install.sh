#!/usr/bin/env bash
set -e

echo "=== 开始安装 Mac AI Efficiency Kit ==="

# 检测目标主目录
TARGET_CONFIG="${HOME}/.gemini/config"
TARGET_SKILLS="${TARGET_CONFIG}/skills"
TARGET_RULES="${TARGET_CONFIG}/rules"
DEFAULT_VAULT="${HOME}/Documents/AI_Workspace"

mkdir -p "${TARGET_SKILLS}"
mkdir -p "${TARGET_RULES}"
mkdir -p "${DEFAULT_VAULT}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "1. 正在同步技能至 ${TARGET_SKILLS}..."
cp -R "${SCRIPT_DIR}/skills/"* "${TARGET_SKILLS}/"

echo "2. 正在同步规则至 ${TARGET_RULES}..."
cp -R "${SCRIPT_DIR}/rules/"* "${TARGET_RULES}/"

echo "3. 正在适配本地路径..."
find "${TARGET_SKILLS}" "${TARGET_RULES}" -type f \( -name "*.md" -o -name "*.py" -o -name "*.json" \) \
  -exec sed -i '' "s|\${VAULT_DIR:-$HOME/Documents/AI_Workspace}|${DEFAULT_VAULT}|g" {} +

echo "4. 赋予脚本执行权限..."
find "${TARGET_SKILLS}" -name "*.py" -exec chmod +x {} + 2>/dev/null || true

echo "=== 安装完成！共部署 12 项技能与全局规则规范 ==="
echo "工作空间默认位于: ${DEFAULT_VAULT}"
