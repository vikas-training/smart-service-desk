#JSON-backed implementation of the request repository contract

import json
import os
import tempfile
from pathlib import Path

from application.request_repository import RequestRepository
from domain.exceptions import DomainError
from domain.service_request import ServiceRequest


class RepositoryError(Exception):
    """Raised when persisted request data cannot be read or written."""


class FileRepository(RequestRepository):
    """Stores all requests in a JSON file using atomic replacement."""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)

    def get_all(self) -> list[ServiceRequest]:
        if not self._file_path.exists():
            return []

        try:
            raw_content = self._file_path.read_text(encoding="utf-8")
            if not raw_content.strip():
                return []

            payload = json.loads(raw_content)
            if not isinstance(payload, list):
                raise RepositoryError("The requests JSON file must contain a list.")

            return [ServiceRequest.from_dict(item) for item in payload]
        except json.JSONDecodeError as exc:
            raise RepositoryError(
                f"Cannot read '{self._file_path}': invalid JSON at line "
                f"{exc.lineno}, column {exc.colno}."
            ) from exc
        except OSError as exc:
            raise RepositoryError(f"Unable to read request data: {exc}") from exc
        except DomainError as exc:
            raise RepositoryError(f"Saved request data is invalid: {exc}") from exc

    def save_all(self, requests: list[ServiceRequest]) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [request.to_dict() for request in requests]
        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._file_path.parent,
                prefix=f".{self._file_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(payload, temporary_file, indent=4, ensure_ascii=False)
                temporary_file.write("\n")
                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            temporary_path.replace(self._file_path)
        except OSError as exc:
            raise RepositoryError(f"Unable to save request data: {exc}") from exc
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()