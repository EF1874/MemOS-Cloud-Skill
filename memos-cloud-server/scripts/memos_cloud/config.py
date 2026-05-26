from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional

from .errors import ConfigurationError


DEFAULT_BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"


@dataclass(frozen=True)
class MemosConfig:
    base_url: str
    api_key: str

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
        }


def load_config(env: Optional[Mapping[str, str]] = None) -> MemosConfig:
    source = env if env is not None else os.environ
    api_key = source.get("MEMOS_API_KEY")
    if not api_key:
        raise ConfigurationError("MEMOS_API_KEY environment variable is not set.")

    return MemosConfig(
        base_url=source.get("MEMOS_CLOUD_URL", DEFAULT_BASE_URL).rstrip("/"),
        api_key=api_key,
    )
