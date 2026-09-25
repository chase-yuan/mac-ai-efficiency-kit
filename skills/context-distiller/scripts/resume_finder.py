#!/usr/bin/env python3
import sys, os, glob, re, time

CHAT_DIR = '${VAULT_DIR:-$HOME/Documents/AI_Workspace}/CLI Chats'

def is_valid_user_chat(file_path):
    base = os.path.basename(file_path)
    ignored = [
        'Gemini Linguistic Analysis Contract',
        'What is ',
        'Hello, respond',
        'ping',
    ]
    return not any(k in base for k in ignored)

def get_recent_chats(limit=5):
    files = glob.glob(f'{CHAT_DIR}/**/*.md', recursive=True)
    if not files:
        return []
    # Filter out automated background worker tasks
    files = [f for f in files if is_valid_user_chat(f)]
    # Sort by modification time descending
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[:limit]

def format_relative_time(mtime):
    diff = time.time() - mtime
    if diff < 60:
        return "刚刚"
    elif diff < 3600:
        return f"{int(diff // 60)} 分钟前"
    elif diff < 86400:
        return f"{int(diff // 3600)} 小时前"
    else:
        return f"{int(diff // 86400)} 天前"

def extract_chat_topic(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extract title from # header or filename
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else os.path.basename(file_path)

        # Extract You turns
        you_turns = re.findall(r'## You — [^\n]+\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        
        # Last You prompt for topic summary
        last_you = you_turns[-1].strip().replace('\n', ' ') if you_turns else title
        if len(last_you) > 50:
            last_you = last_you[:50] + "..."
            
        mtime = os.path.getmtime(file_path)
        rel_time = format_relative_time(mtime)

        return {
            'file_path': file_path,
            'file_base': os.path.basename(file_path),
            'title': title,
            'last_you': last_you,
            'turn_count': len(you_turns),
            'mtime': mtime,
            'rel_time': rel_time
        }
    except Exception as e:
        return None

def list_candidates():
    files = get_recent_chats(4)
    candidates = []
    for f in files:
        info = extract_chat_topic(f)
        if info and info['turn_count'] > 0:
            candidates.append(info)
    return candidates

def find_by_query(query):
    candidates = list_candidates()
    if not query or not query.strip():
        return candidates[0] if candidates else None

    q = query.strip().lower()
    
    # 1. Check if user typed number index (1, 2, 3...)
    if q.isdigit():
        idx = int(q) - 1
        if 0 <= idx < len(candidates):
            return candidates[idx]

    # 2. Match in title or filename
    for c in candidates:
        if q in c['file_base'].lower() or q in c['title'].lower():
            return c

    # 3. Match in full recent files
    files = glob.glob(f'{CHAT_DIR}/**/*.md', recursive=True)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    for f in files[:20]:
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                txt = fp.read()
                if q in txt.lower():
                    return extract_chat_topic(f)
        except Exception:
            pass

    return candidates[0] if candidates else None

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if len(args) == 0 or args[0] == '--list':
        # Output candidate picker table
        cands = list_candidates()
        print("CANDIDATES_COUNT=" + str(len(cands)))
        for i, c in enumerate(cands):
            print(f"[{i+1}] {c['title']} | {c['last_you']} | {c['rel_time']} | {c['file_path']}")
    else:
        # Match target
        target = find_by_query(" ".join(args))
        if target:
            print(f"TARGET_FILE={target['file_path']}")
            print(f"TITLE={target['title']}")
            print(f"REL_TIME={target['rel_time']}")
            print(f"LAST_YOU={target['last_you']}")
        else:
            print("ERROR: No match found")
