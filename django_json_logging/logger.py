import logging
from datetime import datetime
from typing import Type

import json_log_formatter

from django_json_logging.request_context import RequestContext


class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        request_context = self.get_request_context()
        extra["time"] = datetime.utcnow()
        extra["level"] = record.levelname
        extra["name"] = record.name
        extra["message"] = message
        extra["exc_info"] = record.exc_info
        extra["exc_text"] = record.exc_text
        extra["request_id"] = request_context.get_request_id()
        extra["user"] = request_context.get_user()
        extra["user_session_id"] = request_context.get_user_session_id()
        return {k: str(v) for k, v in extra.items() if v is not None}

    @staticmethod
    def get_request_context() -> Type[RequestContext]:
        return RequestContext
