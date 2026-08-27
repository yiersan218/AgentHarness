import pytest

from agent_harness.config import Settings


def test_settings_are_loaded_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MODEL_NAME", "test-model")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com/v1")

    settings = Settings.from_env()

    assert settings == Settings(
        model_name="test-model",
        api_key="test-key",
        base_url="https://example.com/v1",
    )


def test_missing_required_settings_raise_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MODEL_NAME", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="MODEL_NAME, OPENAI_API_KEY"):
        Settings.from_env()
