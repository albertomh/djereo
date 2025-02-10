import logging

import structlog


class FirstArgOnlyFilter(logging.Filter):
    """Extracts the first argument from args and sets it as the log message."""

    def filter(self, record):
        if record.args and isinstance(record.args, tuple):
            record.msg = record.args[0]
            record.args = ()
        return True


class LoggingConfigFactory:
    def __init__(self, debug=False):
        self.debug = debug

    def build(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "require_debug_true": {
                    "()": "django.utils.log.RequireDebugTrue",
                },
                "require_debug_false": {
                    "()": "django.utils.log.RequireDebugFalse",
                },
            },
            "formatters": {
                "json_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                },
                "rich": {
                    "datefmt": "[%X]",
                },
            },
            "handlers": {
                "null": {
                    "class": "logging.NullHandler",
                },
                "dev_log": {
                    "class": "rich.logging.RichHandler",
                    "filters": ["require_debug_true"],
                    "formatter": "rich",
                    "level": "INFO",
                    "rich_tracebacks": True,
                    "tracebacks_show_locals": True,
                },
                "prod_log": {
                    "class": "logging.StreamHandler",
                    "filters": ["require_debug_false"],
                    "formatter": "json_formatter",
                    "level": "INFO",
                },
            },
            "loggers": {
                "django": {
                    "handlers": ["dev_log" if self.debug else "prod_log"],
                    "level": "INFO",
                    "propagate": False,
                },
                "django.request": {
                    "handlers": ["dev_log" if self.debug else "null"],
                    "level": "INFO",
                    "propagate": True,
                },
                "django_structlog": {
                    "handlers": ["null" if self.debug else "prod_log"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["dev_log" if self.debug else "prod_log"],
                "level": "INFO",
            },
        }
