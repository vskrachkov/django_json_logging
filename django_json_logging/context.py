from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class RequestContext:
    request_id: Any
    user: Any
    user_session_id: Any
    ip: Any

    def to_dict(self) -> dict:
        return asdict(self)
