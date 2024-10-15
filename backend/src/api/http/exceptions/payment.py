from typing import Any, Dict

from fastapi import HTTPException


class InvalidPaymentError(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid payment.")
        