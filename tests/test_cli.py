import io
import json

from memos_cloud.cli import main


class RecordingClient:
    def __init__(self, response=None):
        self.response = response or {"ok": True}
        self.calls = []

    def post(self, endpoint, payload):
        self.calls.append((endpoint, payload))
        return self.response


def test_cli_search_prints_json_and_posts_payload(capsys):
    client = RecordingClient({"results": []})

    exit_code = main(["search", "user-1", "hello"], client=client)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"results": []}
    assert client.calls == [
        ("/search/memory", {"user_id": "user-1", "query": "hello"})
    ]


def test_cli_invalid_messages_prints_validation_json(capsys):
    exit_code = main(["add_message", "user-1", "conv-1", "not-json"], client=RecordingClient())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert json.loads(captured.err) == {
        "error": "Validation Error",
        "message": "messages must be a valid JSON string",
    }


def test_cli_add_kb_doc_stdin_posts_file_payload(capsys):
    client = RecordingClient({"uploaded": True})

    exit_code = main(
        ["add_kb_doc", "kb-1", "--stdin", "--name", "note.txt"],
        stdin_buffer=io.BytesIO(b"hello"),
        client=client,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"uploaded": True}
    assert client.calls == [
        (
            "/add/knowledgebase-file",
            {
                "knowledgebase_id": "kb-1",
                "file": [
                    {
                        "type": "document",
                        "name": "note.txt",
                        "content": "aGVsbG8=",
                    }
                ],
            },
        )
    ]


def test_cli_add_kb_doc_requires_files_or_stdin(capsys):
    exit_code = main(["add_kb_doc", "kb-1"], client=RecordingClient())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert json.loads(captured.err) == {
        "error": "Validation Error",
        "message": "Either provide files or use --stdin",
    }
