import tempfile
import unittest
from pathlib import Path

from application.request_service import RequestService
from domain.exceptions import DuplicateRequestError, RequestNotFoundError
from infrastructure.file_repository import FileRepository
from domain.service_request import RequestStatus


class RequestServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        repository = FileRepository(Path(self.temp_dir.name) / "requests.json")
        self.service = RequestService(repository)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_search_request(self):
        created = self.service.create_request("sr101", "Rahul", "Laptop issue", "HIGH")
        found = self.service.search_request("SR101")
        self.assertEqual(created.request_id, found.request_id)

    def test_duplicate_id_is_rejected_case_insensitively(self):
        self.service.create_request("SR101", "Rahul", "Laptop issue", "HIGH")
        with self.assertRaises(DuplicateRequestError):
            self.service.create_request("sr101", "Priya", "Wi-Fi issue", "LOW")

    def test_unknown_id_is_rejected(self):
        with self.assertRaises(RequestNotFoundError):
            self.service.search_request("SR999")

    def test_resolve_is_persisted(self):
        self.service.create_request("SR101", "Rahul", "Laptop issue", "HIGH")
        self.service.resolve_request("SR101")
        found = self.service.search_request("SR101")
        self.assertEqual(found.status, RequestStatus.RESOLVED)


if __name__ == "__main__":
    unittest.main()
