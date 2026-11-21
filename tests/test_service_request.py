import unittest

from domain.exceptions import InvalidPriorityError, RequestAlreadyResolvedError
from domain.service_request import Priority, RequestStatus, ServiceRequest


class ServiceRequestTests(unittest.TestCase):
    def setUp(self):
        self.request = ServiceRequest("SR101", "Rahul", "Laptop is not starting", "HIGH")

    def test_new_request_starts_open(self):
        self.assertEqual(self.request.status, RequestStatus.OPEN)

    def test_priority_is_normalized(self):
        request = ServiceRequest("SR102", "Priya", "Wi-Fi issue", "medium")
        self.assertEqual(request.priority, Priority.MEDIUM)

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(InvalidPriorityError):
            ServiceRequest("SR103", "Asha", "VPN issue", "URGENT")

    def test_resolve_changes_status(self):
        self.request.resolve()
        self.assertEqual(self.request.status, RequestStatus.RESOLVED)

    def test_resolving_twice_is_rejected(self):
        self.request.resolve()
        with self.assertRaises(RequestAlreadyResolvedError):
            self.request.resolve()


if __name__ == "__main__":
    unittest.main()
