#Service request entity and its business rules

from dataclasses import dataclass
from enum import Enum

from domain.exceptions import InvalidPriorityError, InvalidRequestDataError, RequestAlreadyResolvedError


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RequestStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"


@dataclass
class ServiceRequest:
    """Represents one employee support request.

    The entity owns request validation and state-transition behavior.
    It deliberately knows nothing about JSON, files, or the CLI.
    """

    request_id: str
    employee_name: str
    issue: str
    priority: Priority
    status: RequestStatus = RequestStatus.OPEN

    def __post_init__(self) -> None:
        self.request_id = self._required_text(self.request_id, "Request ID")
        self.employee_name = self._required_text(self.employee_name, "Employee name")
        self.issue = self._required_text(self.issue, "Issue description")
        self.priority = self._coerce_priority(self.priority)
        self.status = self._coerce_status(self.status)

    @staticmethod
    def _required_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidRequestDataError(f"{field_name} cannot be empty.")
        return value.strip()

    @staticmethod
    def _coerce_priority(value: Priority | str) -> Priority:
        try:
            return value if isinstance(value, Priority) else Priority(str(value).strip().upper())
        except ValueError as exc:
            allowed = ", ".join(item.value for item in Priority)
            raise InvalidPriorityError(f"Priority must be {allowed}.") from exc

    @staticmethod
    def _coerce_status(value: RequestStatus | str) -> RequestStatus:
        try:
            return value if isinstance(value, RequestStatus) else RequestStatus(str(value).strip().upper())
        except ValueError as exc:
            allowed = ", ".join(item.value for item in RequestStatus)
            raise InvalidRequestDataError(f"Status must be one of: {allowed}.") from exc

    def resolve(self) -> None:
        """Apply the only permitted status transition: OPEN -> RESOLVED."""
        if self.status is RequestStatus.RESOLVED:
            raise RequestAlreadyResolvedError(
                f"Request {self.request_id} is already resolved."
            )
        self.status = RequestStatus.RESOLVED

    def to_dict(self) -> dict[str, str]:
        """Return a persistence-friendly representation."""
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority.value,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ServiceRequest":
        """Reconstruct an entity from repository data."""
        if not isinstance(data, dict):
            raise InvalidRequestDataError("Each saved request must be a JSON object.")
        required = {"request_id", "employee_name", "issue", "priority"}
        missing = required.difference(data)
        if missing:
            raise InvalidRequestDataError(
                f"Saved request is missing fields: {', '.join(sorted(missing))}."
            )
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", RequestStatus.OPEN.value),
        )