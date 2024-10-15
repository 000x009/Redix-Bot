from typing import Dict
from fastapi import HTTPException


class NotAuthorizedError(HTTPException): ...


class MethodNotAllowedError(HTTPException):
    def __init__(self, headers: Dict[str, str] | None = None) -> None:
        super().__init__(
            status_code=403,
            detail=dict(error='Method not allowed.'),
            headers=headers,
        )
