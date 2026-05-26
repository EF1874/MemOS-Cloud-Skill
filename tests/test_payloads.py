import pytest

from memos_cloud.errors import ValidationError
from memos_cloud.payloads import (
    add_feedback_payload,
    add_message_payload,
    delete_memory_payload,
    search_memory_payload,
)


def test_search_memory_payload_omits_empty_conversation_id():
    assert search_memory_payload("user-1", "query") == {
        "user_id": "user-1",
        "query": "query",
    }


def test_search_memory_payload_includes_conversation_id():
    assert search_memory_payload("user-1", "query", "conv-1") == {
        "user_id": "user-1",
        "query": "query",
        "conversation_id": "conv-1",
    }


def test_add_message_payload_parses_json_messages():
    assert add_message_payload(
        "user-1",
        "conv-1",
        '[{"role":"user","content":"hello"}]',
    ) == {
        "user_id": "user-1",
        "conversation_id": "conv-1",
        "messages": [{"role": "user", "content": "hello"}],
    }


def test_add_message_payload_rejects_invalid_json():
    with pytest.raises(ValidationError, match="messages must be a valid JSON string"):
        add_message_payload("user-1", "conv-1", "not-json")


def test_delete_memory_payload_parses_csv():
    assert delete_memory_payload(" id1, id2 ,, id3 ") == {
        "memory_ids": ["id1", "id2", "id3"],
    }


def test_delete_memory_payload_requires_ids():
    with pytest.raises(ValidationError, match="memory_ids is required"):
        delete_memory_payload("")


def test_add_feedback_payload_preserves_legacy_csv_shape():
    assert add_feedback_payload("user-1", "conv-1", "feedback", " kb1, kb2 ") == {
        "user_id": "user-1",
        "conversation_id": "conv-1",
        "feedback_content": "feedback",
        "allow_knowledgebase_ids": ["kb1", "kb2"],
    }
