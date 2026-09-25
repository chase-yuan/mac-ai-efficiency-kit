#!/usr/bin/env python3
import sys, os, glob, re, subprocess

def get_latest_chat():
    chats = glob.glob('${VAULT_DIR:-$HOME/Documents/AI_Workspace}/CLI Chats/*/*.md')
    if not chats:
        return None
    chats.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return chats[0]

def distill(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract all You turns
    you_turns = re.findall(r'## You — [^\n]+\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    
    # Extract file links
    files_found = list(set(re.findall(r'(?:file:///|${HOME}/)[^\s\)\"\`\']+\.[a-zA-Z0-9]+', content)))
    
    # Extract last Assistant response
    assistant_turns = re.findall(r'## Assistant — [^\n]+\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    last_assistant = assistant_turns[-1].strip() if assistant_turns else ""
    last_you = you_turns[-1].strip() if you_turns else ""

    file_base = os.path.basename(file_path)
    
    capsule = f"""# 💊 【Context Capsule · 会话无损接力胶囊】

> **源会话**：[`{file_base}`](file://{file_path})
> **总交互轮数**：{len(you_turns)} 轮 | **关键物理资产**：{len(files_found)} 个

---

### 1. 🎯 核心演进与提问骨架 (Prompt Skeleton)
"""
    for i, t in enumerate(you_turns[-8:]):
        clean_t = t.strip().replace('\n', ' ')
        if len(clean_t) > 90:
            clean_t = clean_t[:90] + '...'
        capsule += f"- `[Step {i+1}]` {clean_t}\n"

    capsule += "\n### 2. 🗂️ 关联物理资产清单\n"
    for fp in files_found[:8]:
        clean_fp = fp.replace('file://', '')
        capsule += f"- 📄 [`{os.path.basename(clean_fp)}`](file://{clean_fp})\n"

    capsule += f"""
### 3. ⚡ 最新尾部断点与即刻接力目标
- **上一轮核心诉求**：{last_you[:180]}
- **下一步动作**：在新窗口中直接基于上述资产与断点，无缝继续工作。
"""
    return capsule

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else get_latest_chat()
    if not target or not os.path.exists(target):
        print("No valid chat file found.")
        sys.exit(1)
    
    capsule_text = distill(target)
    print(capsule_text)
    
    # Copy to clipboard
    try:
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
        p.communicate(input=capsule_text)
        print("\n✅ 已自动将【上下文胶囊】复制到系统剪贴板 (pbcopy)！在任意新窗口 ⌘+V 粘贴即可直接接力！")
    except Exception as e:
        pass
