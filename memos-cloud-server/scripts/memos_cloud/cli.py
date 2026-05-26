from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .client import MemosClient
from .config import load_config
from .errors import MemosCloudError, ValidationError, print_error
from .files import build_file_payloads, build_stdin_file_payload
from .operations import add_feedback, add_kb_doc, add_message, delete_memory, search_memory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MemOS Cloud Server API Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_search = subparsers.add_parser("search", help="Search memory")
    p_search.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_search.add_argument("query", help="Search query string")
    p_search.add_argument("--conversation-id", help="Optional conversation ID")

    p_add = subparsers.add_parser("add_message", help="Add a message memory")
    p_add.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_add.add_argument("conversation_id", help="Conversation ID")
    p_add.add_argument(
        "messages",
        help='Messages as a JSON string. e.g. \'[{"role":"user","content":"hello"}]\'',
    )

    p_del = subparsers.add_parser("delete", help="Delete memory")
    p_del.add_argument("memory_ids", help="Comma-separated list of memory IDs to delete (Required)")

    p_fb = subparsers.add_parser("add_feedback", help="Add feedback")
    p_fb.add_argument("user_id", nargs="?", default=None, help="User ID (falls back to MEMOS_USER_ID env var)")
    p_fb.add_argument("conversation_id", help="Conversation ID")
    p_fb.add_argument("feedback_content", help="Feedback content text")
    p_fb.add_argument("--allow-knowledgebase-ids", help="Comma-separated list of knowledgebase IDs")

    p_kb = subparsers.add_parser("add_kb_doc", help="Upload files to knowledge base")
    p_kb.add_argument("knowledgebase_id", help="Target knowledge base ID")
    p_kb.add_argument(
        "files",
        nargs="*",
        help="Files to upload: URLs (http/https) or local file paths (auto-converted to base64)",
    )
    p_kb.add_argument(
        "--type",
        dest="file_type",
        default="document",
        choices=["document", "skill"],
        help="File type: document (default) or skill",
    )
    p_kb.add_argument("--name", help="Filename for stdin content (recommended with --stdin)")
    p_kb.add_argument(
        "--stdin",
        action="store_true",
        help="Read base64 content from stdin (pipe-friendly, avoids context overhead)",
    )

    return parser


def main(
    argv: Optional[Sequence[str]] = None,
    stdin_buffer=None,
    client: Optional[MemosClient] = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        active_client = client or MemosClient(load_config())
        result = dispatch(args, active_client, stdin_buffer or sys.stdin.buffer)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except MemosCloudError as exc:
        print_error(exc)
        return 1
    except Exception as exc:
        print(json.dumps({"error": "Unexpected Error", "message": str(exc)}), file=sys.stderr)
        return 1


def _resolve_user_id(args: argparse.Namespace, client: MemosClient) -> str:
    user_id = getattr(args, "user_id", None) or client.config.user_id
    if not user_id:
        raise ValidationError(
            "user_id is required. Provide it as an argument or set MEMOS_USER_ID env var."
        )
    return user_id


def dispatch(args: argparse.Namespace, client: MemosClient, stdin_buffer):
    if args.command == "search":
        return search_memory(client, _resolve_user_id(args, client), args.query, args.conversation_id)

    if args.command == "add_message":
        return add_message(client, _resolve_user_id(args, client), args.conversation_id, args.messages)

    if args.command == "delete":
        return delete_memory(client, args.memory_ids)

    if args.command == "add_feedback":
        return add_feedback(
            client,
            _resolve_user_id(args, client),
            args.conversation_id,
            args.feedback_content,
            args.allow_knowledgebase_ids,
        )

    if args.command == "add_kb_doc":
        file_list = _build_kb_files(args, stdin_buffer)
        return add_kb_doc(client, args.knowledgebase_id, file_list)

    parser = build_parser()
    parser.error(f"Unknown command: {args.command}")


def _build_kb_files(args: argparse.Namespace, stdin_buffer):
    if args.stdin:
        return [build_stdin_file_payload(stdin_buffer, args.file_type, args.name)]

    if args.files:
        return build_file_payloads(args.files, args.file_type)

    raise ValidationError("Either provide files or use --stdin")
