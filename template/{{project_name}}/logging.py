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
    def __init__(self, *, debug=False):
        self.debug = debug

    def build(self):
        dev_mode = self.debug

        console_rich = {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "level": "INFO",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        }

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
                "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
                "first_arg_only": {"()": FirstArgOnlyFilter},
            },
            "formatters": {
                "json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                },
                "rich": {"datefmt": "[%X]"},
                "rich_http": {"datefmt": "[%X]", "format": "%(status_code)s %(msg)s"},
            },
            "handlers": {
                "console_dev": console_rich,
                "console_http": {**console_rich, "formatter": "rich_http"},
                "console_prod": {
                    "class": "logging.StreamHandler",
                    "filters": ["require_debug_false"],
                    "formatter": "json",
                    "level": "INFO",
                },
                "null": {"class": "logging.NullHandler"},
            },
            "loggers": {
                "django": {
                    "handlers": ["console_dev" if dev_mode else "console_prod"],
                    "level": "INFO",
                    "propagate": False,
                },
                "django.server": {
                    "handlers": ["console_http" if dev_mode else "null"],
                    "level": "INFO",
                    "propagate": False,
                    "filters": ["first_arg_only"],
                },
                "django_structlog": {
                    "handlers": ["null" if dev_mode else "console_prod"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console_dev" if dev_mode else "console_prod"],
                "level": "INFO",
            },
        }
