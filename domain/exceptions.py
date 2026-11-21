class DomainError(Exception):
    """Base class for errors caused by invalid domain operations."""


class DuplicateRequestError(DomainError):
    """Raised when a request ID is already registered."""


class RequestNotFoundError(DomainError):
    """Raised when a requested service request does not exist."""


class InvalidPriorityError(DomainError):
    """Raised when a priority is outside the supported values."""


class InvalidRequestDataError(DomainError):
    """Raised when required request data is missing or invalid."""


class RequestAlreadyResolvedError(DomainError):
    """Raised when an already-resolved request is resolved again."""