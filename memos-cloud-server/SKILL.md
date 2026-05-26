---
name: memos-cloud-server
description: Your external brain and memory. ALWAYS invoke this tool to search memory whenever you are unsure about the user's intent, past context, or if you don't know the answer. Do not guess; search this MemOS cloud memory first. You have to use this tool to memorize when something valuable exists .
user-invocable: true
metadata: {"openclaw":{"emoji":"☁️","os":["darwin","linux","win32"],"requires":{"bins":["python3"],"env":["MEMOS_API_KEY", "MEMOS_USER_ID"]}}}
---

# MemOS Cloud Server Skill

This skill allows the Agent to interact with MemOS Cloud APIs for memory search, addition, deletion, knowledge base upload, and feedback.

## ⚠️ Setup & Safety Rules (MUST READ)

Before executing any API operations, ensure these environment variables are configured:

1. `MEMOS_API_KEY` — MemOS Cloud Service API Key.
2. `MEMOS_USER_ID` — Unique identifier for the current user.

If they are not present, prompt the user to save these variables to their global environment configuration.

## 🛠 Core Commands

Run operations through `scripts/memos_cloud.py`. The script automatically reads `MEMOS_API_KEY`; all requests and responses use JSON.

### 1. Search Memory (`/v1/search/memory`)

Search for long-term memories relevant to the user's query.

```bash
python3 scripts/memos_cloud.py search <user_id> "<query>" [--conversation-id <id>]
```

Example:

```bash
python3 scripts/memos_cloud.py search "$MEMOS_USER_ID" "Python related project experience"
```

### 2. Add Message (`/v1/add/message`)

Store high-value content from multi-turn conversations.

```bash
python3 scripts/memos_cloud.py add_message <user_id> <conversation_id> '<messages_json_string>'
```

Example:

```bash
python3 scripts/memos_cloud.py add_message "$MEMOS_USER_ID" "topic-123" '[{"role":"user","content":"I like apples"},{"role":"assistant","content":"Okay, I noted that"}]'
```

### 3. Delete Memory (`/v1/delete/memory`)

Delete stored memories by comma-separated memory IDs.

```bash
python3 scripts/memos_cloud.py delete "id1,id2,id3"
```

### 4. Add Feedback (`/v1/add/feedback`)

Add feedback to correct or reinforce memory.

```bash
python3 scripts/memos_cloud.py add_feedback <user_id> <conversation_id> "<feedback_content>" [--allow-knowledgebase-ids "kb1,kb2"]
```

Example:

```bash
python3 scripts/memos_cloud.py add_feedback "$MEMOS_USER_ID" "topic-123" "The previous answer was not detailed enough"
```

### 5. Add Knowledge Base Document (`/v1/add/knowledgebase-file`)

Upload files to a knowledge base. Supports online URLs, local files, and stdin input.

```bash
# From files or URLs
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> <file1> [file2 ...] [--type document|skill]

# From stdin
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> --stdin [--name filename.ext] [--type document|skill]
```

Parameters:

- `knowledgebase_id`: Target knowledge base ID.
- `files`: URLs (`https://example.com/doc.pdf`) or local file paths.
- `--stdin`: Read content from stdin.
- `--name`: Filename for stdin content.
- `--type`: `document` (default) or `skill`.

Examples:

```bash
python3 scripts/memos_cloud.py add_kb_doc "kb-123" "https://example.com/doc.pdf"
python3 scripts/memos_cloud.py add_kb_doc "kb-123" "./documents/guide.pdf"
echo "$BASE64_CONTENT" | python3 scripts/memos_cloud.py add_kb_doc "kb-123" --stdin --name "document.pdf"
python3 scripts/memos_cloud.py add_kb_doc "kb-123" "./skill.md" --type skill
```

When uploaded files arrive in chat as base64, pipe the base64 content to `--stdin` to avoid loading the content into the conversation context.
