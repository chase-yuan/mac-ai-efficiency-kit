# AI AGENT SETUP DIRECTIVE (AI 自动化安装协议)

> [!IMPORTANT]
> **致正在阅读本文件的 AI 助手 (For AI Assistant / Agent)**:
> 你当前收到了用户分享的 `Mac_AI_Efficiency_Kit`。你的任务是**自主识别用户当前的系统与 AI 环境，并将本套件中的技能与规范无感部署到用户的电脑中**，无需用户手动敲代码。

---

## 自动化执行步骤 (Autonomous Execution Workflow)

请你按顺序自主执行以下 4 个阶段，并在执行完成后向你的用户汇报：

### 阶段 1：环境感知与目录探测 (Environment Detection)
1. 检查用户的操作系统主目录：获取用户的 `$HOME`（如 `/Users/<username>`）。
2. 检测用户当前使用的 AI 工具与配置路径（按优先级检查并创建）：
   - **Google Antigravity / Gemini CLI**: `~/.gemini/config/skills/` 与 `~/.gemini/config/rules/`
   - **OpenAI Codex CLI**: `~/.codex/skills/` 与 `~/.codex/rules/`
   - **Claude Code**: `~/.claude/skills/` 与 `~/.claude/rules/`
   - **通用工作区 / 项目级**: 若用户希望作为当前项目使用，可部署至当前目录的 `.agents/skills/` 与 `.agents/rules/`。
3. 检查用户的个人笔记存储路径（Vault 目录）：
   - 检查是否存在 `~/Vault/MyObsidian`、`~/Documents/Obsidian` 或 `~/Vault`。
   - 若不存在，默认创建并映射至 `~/Documents/AI_Workspace/`。

### 阶段 2：安全分发与路径对齐 (Deploy & Path Adaptation)
1. 将当前目录下的 `skills/*` 复制到对应的技能根目录中（例如 `~/.gemini/config/skills/`）。
2. 将当前目录下的 `rules/*` 复制到对应的规则目录中（例如 `~/.gemini/config/rules/`）。
3. 自动扫描复制过去的文件，将其中占位符 `${VAULT_DIR:-$HOME/Documents/AI_Workspace}` 替换为用户的真实笔记目录。
4. 保证目标脚本具有正确的执行权限 (`chmod +x ...`)。

### 阶段 3：执行验证与物理测试 (Verification Gate)
运行终端指令核验文件是否已完整写入：
```bash
ls -la <目标技能目录>
```
确保包含的 11 项技能全部处于就绪状态。

### 阶段 4：生成给用户的就绪汇报 (User Report)
执行完毕后，以用户当前的交互语言（全球英文用户默认使用 English，中文用户使用中文）向用户汇报交付矩阵与常用技能快捷指令表：
1. 安装的目标路径与完成状态。
2. 5 个最常用技能的触发方式（如：`council:` 触发决策委员会、`>` 触发地道英语口语翻译、`zack:` 触发认知地图、`lucky:` 触发语音纠错大管家）。
