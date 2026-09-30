from collections.abc import Iterator

import pytest

from pathwise.core.config import get_settings


@pytest.fixture(autouse=True)
def test_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("PATHWISE_ENVIRONMENT", "test")
    monkeypatch.setenv("PATHWISE_APP_NAME", "Pathwise Test API")
    monkeypatch.setenv("PATHWISE_CORS_ALLOWED_ORIGIN", "http://test.local")
    get_settings.cache_clear()

    yield

    get_settings.cache_clear()
