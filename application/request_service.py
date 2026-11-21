from typing import Protocol

from domain.service_request import ServiceRequest


class RequestRepository(Protocol):
    """Defines persistence operations without choosing a storage technology."""

    def get_all(self) -> list[ServiceRequest]:
        ...

    def save_all(self, requests: list[ServiceRequest]) -> None:
        ...