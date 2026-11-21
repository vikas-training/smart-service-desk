#Application use cases for managing service requests
from domain.exceptions import DuplicateRequestError, RequestNotFoundError
from domain.service_request import Priority, ServiceRequest
from application.request_repository import RequestRepository


class RequestService:

    def __init__(self, repository: RequestRepository) -> None:
        self._repository = repository

    def create_request(
        self, request_id: str, employee_name: str, issue: str, priority: str
    ) -> ServiceRequest:
        requests = self._repository.get_all()
        normalized_id = request_id.strip().upper()

        if any(item.request_id.casefold() == normalized_id.casefold() for item in requests):
            raise DuplicateRequestError(f"Request ID '{normalized_id}' already exists.")

        request = ServiceRequest(
            request_id=normalized_id,
            employee_name=employee_name,
            issue=issue,
            priority=priority,
        )
        requests.append(request)
        self._repository.save_all(requests)
        return request

    def view_requests(self) -> list[ServiceRequest]:
        return self._repository.get_all()

    def search_request(self, request_id: str) -> ServiceRequest:
        normalized_id = request_id.strip()
        for request in self._repository.get_all():
            if request.request_id.casefold() == normalized_id.casefold():
                return request
        raise RequestNotFoundError(f"Request '{normalized_id}' was not found.")

    def resolve_request(self, request_id: str) -> ServiceRequest:
        requests = self._repository.get_all()
        normalized_id = request_id.strip()

        for request in requests:
            if request.request_id.casefold() == normalized_id.casefold():
                request.resolve()
                self._repository.save_all(requests)
                return request

        raise RequestNotFoundError(f"Request '{normalized_id}' was not found.")