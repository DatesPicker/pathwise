import json
import logging
from datetime import UTC, datetime
from logging.config import dictConfig

_ALLOWED_EXTRA_FIELDS = ("environment",)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=UTC)
        payload = {
            "timestamp": timestamp.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for field in _ALLOWED_EXTRA_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = str(value)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                }
            },
            "handlers": {
                "pathwise_stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "level": "INFO",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "pathwise": {
                    "handlers": ["pathwise_stdout"],
                    "level": "INFO",
                    "propagate": False,
                }
            },
        }
    )
