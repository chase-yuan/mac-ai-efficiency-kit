---
name: zh-en-chat-translator
description: "Trigger when user input starts with '>', '.', or '【中文】' (e.g. '> 今天有空吗', '. 收到稍后看', 'translate:', 'chat-translate:'). Translates Chinese colloquial chat into natural, idiomatic American English for chatting with native speakers, generates 1 recommended version, 6-10 tone variations, and nuance warnings, silently pipes the recommended version to macOS clipboard via pbcopy, and appends the log to Obsidian."
---

# Zh-En Chat Translator

## Invocation Matrix

| Trigger | Mode | Input Arguments | Deterministic Action |
| :--- | :--- | :--- | :--- |
| `>` / `.` / `【中文】` prefix | Instant Chat Translation | Chinese colloquial message | Translate into 1 Best + 6-10 tone variants; pipe Best to `pbcopy`; append to Obsidian |
| `translate:` / `chat-translate:` | Explicit Chat Translation | Chinese text | Perform conversational translation with cultural nuance checks |

---

## Translation & Tone Architecture

Every response must provide:
1. **Recommended Best Version**: The most natural, culturally authentic American conversational version.
2. **Tone Variation Matrix (6-10 Variants)**:
   - `Formal / Polite`: Business-appropriate, deferential.
   - `Polished`: Clean, professional, well-crafted.
   - `Neutral`: Direct, natural, balanced.
   - `Casual`: Everyday friendly messaging.
   - `Spoken / Colloquial`: Authentic spoken idioms (`vibe`, `catch up`, `on it`).
   - `Humorous / Playful`: Lighthearted, conversational flair.
   - `Warm / Empathetic`: Caring, supportive tone.
   - `Ultra-Short`: Texting brevity (e.g. `Sounds good, on it`).
3. **Nuance & Cultural Safety Warning**: Highlights potential misinterpretations, tone harshness, or boundary risks when applicable.

---

## Obsidian Logging Protocol

Append translation entries to: `${VAULT_DIR:-$HOME/Documents/AI_Workspace}/English/Chat Translation/YYYY-MM-DD_Chat_Translations.md`

### Entry Layout
```markdown
## HH:mm - Chat Translation

- **Source Chinese**: `{{SOURCE_TEXT}}`
- **Recommended Best**: `{{RECOMMENDED_TEXT}}`
- **Tone Highlights**:
  - Casual: `{{CASUAL_TEXT}}`
  - Spoken: `{{SPOKEN_TEXT}}`
  - Short: `{{SHORT_TEXT}}`

---
```

---

## Invariants & Operational Boundaries

1. **Idiomatic Over Literal**: Strictly prohibit Chinglish and word-for-word literal translations.
2. **Automatic Clipboard Sync**: Silently execute `printf '%s' "{{RECOMMENDED_TEXT}}" | pbcopy` on every translation.
3. **Tone Preservation**: Accurately preserve the user's emotional intent, urgency, and relational context.

---

## Runnable Input/Output Contract

### Input
```text
> 好的，我稍后看一下，弄好了跟你说。
```

### Output Payload
```markdown
*Recommended version automatically copied to system clipboard (pbcopy).*

### Recommended Best
"Sounds good, I will take a look in a bit and keep you posted."

### Tone Variations
- Ultra-Short: "Got it, checking shortly."
- Casual: "Cool, on it in a second, will let ya know."
- Formal: "Acknowledged. I will review it shortly and update you."
- Warm: "No problem at all! I will check it out soon and get back to you."

### Nuance & Safety
- The phrase "keep you posted" is natural and cooperative, avoiding the stiffness of "I will tell you".
```

---

## Acceptance Criteria

1. **Clipboard Automation**: `pbcopy` execution must succeed with exit code 0.
2. **Obsidian Logging**: Translation log entry must be appended to the current date's Markdown log file.
3. **Tone Diversity**: Must generate at least 6 distinct, contextually accurate tone variations.
