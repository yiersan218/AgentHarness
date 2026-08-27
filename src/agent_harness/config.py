"""Environment-based model configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """The only configuration required by the minimal agent."""

    model_name: str
    api_key: str
    base_url: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        model_name = os.getenv("MODEL_NAME", "").strip()
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None

        missing = [
            name
            for name, value in (
                ("MODEL_NAME", model_name),
                ("OPENAI_API_KEY", api_key),
            )
            if not value
        ]
        if missing:
            names = ", ".join(missing)
            raise ValueError(f"Missing required environment variable(s): {names}")

        return cls(model_name=model_name, api_key=api_key, base_url=base_url)

