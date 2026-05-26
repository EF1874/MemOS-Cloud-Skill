from __future__ import annotations

import json
from typing import Any, Dict, Optional

from .errors import ValidationError


def parse_csv(value: Optional[str]) -> list[str]:
    if not value:
        return []
    return [item for item in (s.strip() for s in value.split(",")) if item]


def search_memory_payload(
    user_id: str,
    query: str,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "user_id": user_id,
        "query": query,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id
    return payload


def add_message_payload(
    user_id: str,
    conversation_id: str,
    messages_json_str: str,
) -> Dict[str, Any]:
    try:
        messages = json.loads(messages_json_str)
    except json.JSONDecodeError as exc:
        raise ValidationError("messages must be a valid JSON string") from exc

    return {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "messages": messages,
    }


def delete_memory_payload(memory_ids_str: str) -> Dict[str, Any]:
    if not memory_ids_str:
        raise ValidationError("memory_ids is required")

    return {"memory_ids": parse_csv(memory_ids_str)}


def add_feedback_payload(
    user_id: str,
    conversation_id: str,
    feedback_content: str,
    allow_knowledgebase_ids: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "feedback_content": feedback_content,
    }

    knowledgebase_ids = parse_csv(allow_knowledgebase_ids)
    if knowledgebase_ids:
        payload["allow_knowledgebase_ids"] = knowledgebase_ids
    return payload


def add_kb_doc_payload(knowledgebase_id: str, file_list: list[Dict[str, str]]) -> Dict[str, Any]:
    return {
        "knowledgebase_id": knowledgebase_id,
        "file": file_list,
    }
