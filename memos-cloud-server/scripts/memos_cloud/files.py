from __future__ import annotations

import base64
import os
from typing import BinaryIO, Dict, Iterable, Optional

from .errors import FilePayloadError, ValidationError


def build_file_payloads(
    files: Iterable[str],
    file_type: str = "document",
) -> list[Dict[str, str]]:
    file_list: list[Dict[str, str]] = []

    for file_spec in files:
        if is_url(file_spec):
            file_list.append({"type": file_type, "content": file_spec})
            continue

        if os.path.isfile(file_spec):
            file_list.append(build_local_file_payload(file_spec, file_type))
            continue

        raise ValidationError(
            f"Invalid file: '{file_spec}'. Must be a URL (http/https) or existing file path."
        )

    return file_list


def build_stdin_file_payload(
    stdin_buffer: BinaryIO,
    file_type: str = "document",
    name: Optional[str] = None,
) -> Dict[str, str]:
    try:
        raw = stdin_buffer.read()
        file_info = {
            "type": file_type,
            "content": normalize_base64_content(raw),
        }
        if name:
            file_info["name"] = name
        return file_info
    except Exception as exc:
        if isinstance(exc, FilePayloadError):
            raise
        raise FilePayloadError("Stdin Error", f"Failed to read from stdin: {str(exc)}") from exc


def build_local_file_payload(file_spec: str, file_type: str = "document") -> Dict[str, str]:
    try:
        with open(file_spec, "rb") as file:
            file_data = file.read()
    except Exception as exc:
        raise FilePayloadError(
            "File Error",
            f"Failed to read file '{file_spec}': {str(exc)}",
        ) from exc

    return {
        "type": file_type,
        "name": os.path.basename(file_spec),
        "content": encode_base64(file_data),
    }


def normalize_base64_content(raw: bytes) -> str:
    try:
        b64_content = raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        return encode_base64(raw)

    try:
        base64.b64decode(b64_content, validate=True)
        return b64_content
    except Exception:
        return encode_base64(raw)


def encode_base64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("utf-8")


def is_url(file_spec: str) -> bool:
    return file_spec.startswith(("http://", "https://"))
