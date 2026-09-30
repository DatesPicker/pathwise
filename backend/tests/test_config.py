import pytest
from pydantic import ValidationError

from pathwise.core.config import Settings, get_settings


def test_test_environment_is_accepted() -> None:
    settings = get_settings()

    assert settings.environment == "test"
    assert settings.app_name == "Pathwise Test API"
    assert settings.cors_allowed_origin == "http://test.local"


def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PATHWISE_ENVIRONMENT", "staging")
    get_settings.cache_clear()

    with pytest.raises(ValidationError):
        get_settings()


def test_cors_origin_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PATHWISE_CORS_ALLOWED_ORIGIN")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_cors_origin_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(cors_allowed_origin="")
