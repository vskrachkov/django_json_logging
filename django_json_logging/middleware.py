import base64
import logging
import uuid
from dataclasses import dataclass
from typing import Optional, Callable, Any

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, QueryDict

log = logging.getLogger(__name__)


@dataclass
class RequestContext:
    request_id: Any
    user: Any
    user_session_id: Any


class AccessLogMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_context = self.log_request(request)
        response: HttpResponse = self.get_response(request)
        self.log_response(response, request_context)
        return response

    def log_request(self, request: HttpRequest) -> RequestContext:
        request_context = RequestContext(
            request_id=self.get_request_id(request),
            user=self.get_user(request),
            user_session_id=self.get_user_session_id(request),
        )
        log.info(
            "RX",
            extra=dict(
                http_method=request.method,
                path=request.path,
                query_params=self.get_query_params(request),
                user_agent=self.get_user_agent(request),
                ip=self.get_ip(request),
                x_forwarded_for=self.get_x_forwarded_for(request),
                request_id=request_context.request_id,
                user=request_context.user,
                user_session_id=request_context.user_session_id,
            ),
        )
        return request_context

    @staticmethod
    def get_x_forwarded_for(request: HttpRequest) -> Optional[str]:
        return request.META.get("HTTP_X_FORWARDED_FOR")

    @staticmethod
    def get_ip(request: HttpRequest) -> Optional[str]:
        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def get_user_agent(request: HttpRequest) -> Optional[str]:
        return request.META.get("HTTP_USER_AGENT")

    @staticmethod
    def get_query_params(request: HttpRequest) -> Optional[QueryDict]:
        return request.GET if request.GET else None

    @staticmethod
    def get_user(request: HttpRequest) -> Optional[str]:
        return (
            str(request.user) if not str(request.user) == str(AnonymousUser()) else None
        )

    @staticmethod
    def get_request_id(request: HttpRequest) -> str:
        return request.META.get("HTTP_X_REQUEST_ID") or base64.urlsafe_b64encode(
            uuid.uuid4().bytes
        ).rstrip(b"=").decode("ascii")

    @staticmethod
    def get_user_session_id(request: HttpRequest) -> Optional[str]:
        session = getattr(request, "session", None)
        session_id = getattr(session, "session_key", None)
        return session_id

    @staticmethod
    def log_response(response: HttpResponse, request_context: RequestContext) -> None:
        log.info(
            "TX",
            extra=dict(
                status_code=response.status_code,
                cookies=response.cookies if response.cookies else None,
                request_id=request_context.request_id,
                user=request_context.user,
                user_session_id=request_context.user_session_id,
            ),
        )
