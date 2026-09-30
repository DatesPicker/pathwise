import json
import logging
from datetime import datetime

from pathwise.core.logging import JsonFormatter


def test_json_formatter_emits_only_approved_structured_fields() -> None:
    record = logging.LogRecord(
        name="pathwise.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="foundation_event",
        args=(),
        exc_info=None,
    )
    record.environment = "test"
    record.not_allowed = "excluded"

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "pathwise.test"
    assert payload["message"] == "foundation_event"
    assert payload["environment"] == "test"
    assert "not_allowed" not in payload
    assert payload["timestamp"].endswith("Z")
    assert datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
