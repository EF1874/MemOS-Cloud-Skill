from __future__ import annotations

from typing import Optional

from .client import MemosClient
from .payloads import (
    add_feedback_payload,
    add_kb_doc_payload,
    add_message_payload,
    delete_memory_payload,
    search_memory_payload,
)


def search_memory(
    client: MemosClient,
    user_id: str,
    query: str,
    conversation_id: Optional[str] = None,
):
    return client.post("/search/memory", search_memory_payload(user_id, query, conversation_id))


def add_message(
    client: MemosClient,
    user_id: str,
    conversation_id: str,
    messages_json_str: str,
):
    return client.post(
        "/add/message",
        add_message_payload(user_id, conversation_id, messages_json_str),
    )


def delete_memory(client: MemosClient, memory_ids_str: str):
    return client.post("/delete/memory", delete_memory_payload(memory_ids_str))


def add_feedback(
    client: MemosClient,
    user_id: str,
    conversation_id: str,
    feedback_content: str,
    allow_knowledgebase_ids: Optional[str] = None,
):
    return client.post(
        "/add/feedback",
        add_feedback_payload(
            user_id,
            conversation_id,
            feedback_content,
            allow_knowledgebase_ids,
        ),
    )


def add_kb_doc(client: MemosClient, knowledgebase_id: str, file_list: list[dict[str, str]]):
    return client.post(
        "/add/knowledgebase-file",
        add_kb_doc_payload(knowledgebase_id, file_list),
    )
