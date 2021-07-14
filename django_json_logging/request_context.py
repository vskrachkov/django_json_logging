from threading import local
from typing import Optional, Any, TypeVar

_T = TypeVar("_T")


class RequestContext:
    _thread_local = local()

    REQUEST_ID_VARIABLE = "_request_id"
    USE_SESSION_ID_VARIABLE = "_user_session_id"
    USER = "_user"

    @classmethod
    def set_request_id(cls, request_id: Optional[str] = None) -> None:
        cls._set_thread_variable(cls.REQUEST_ID_VARIABLE, request_id)

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        return cls._get_thread_variable(cls.REQUEST_ID_VARIABLE)

    @classmethod
    def set_user_session_id(cls, user_session_id: Optional[str] = None) -> None:
        cls._set_thread_variable(cls.USE_SESSION_ID_VARIABLE, user_session_id)

    @classmethod
    def get_user_session_id(cls) -> Optional[str]:
        return cls._get_thread_variable(cls.USE_SESSION_ID_VARIABLE)

    @classmethod
    def set_user(cls, user: Optional[Any]) -> None:
        cls._set_thread_variable(cls.USER, user)

    @classmethod
    def get_user(cls) -> Optional[Any]:
        return cls._get_thread_variable(cls.USER)

    @classmethod
    def _set_thread_variable(cls, key: str, val: Optional[Any]) -> None:
        setattr(cls._thread_local, key, val)

    @classmethod
    def _get_thread_variable(cls, key: Any, default: Optional[_T] = None) -> _T:
        return getattr(cls._thread_local, key, default)
