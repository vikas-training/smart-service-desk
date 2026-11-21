from pathlib import Path

from application.request_service import RequestService
from domain.exceptions import (
    DomainError,
    RequestAlreadyResolvedError,
)
from infrastructure.file_repository import FileRepository, RepositoryError


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "data" / "requests.json"


def display_request(request) -> None:
    print("\nRequest Details")
    print("-" * 40)
    print(f"Request ID     : {request.request_id}")
    print(f"Employee Name  : {request.employee_name}")
    print(f"Issue          : {request.issue}")
    print(f"Priority       : {request.priority.value}")
    print(f"Status         : {request.status.value}")
    print("-" * 40)


def create_request(service: RequestService) -> None:
    request_id = input("Enter Request ID: ").strip()
    employee_name = input("Enter Employee Name: ").strip()
    issue = input("Enter Issue Description: ").strip()
    priority = input("Enter Priority (LOW/MEDIUM/HIGH): ").strip()

    request = service.create_request(request_id, employee_name, issue, priority)
    print(f"\nService request {request.request_id} created successfully.")


def view_requests(service: RequestService) -> None:
    requests = service.view_requests()
    if not requests:
        print("\nNo service requests found.")
        return

    print("\nAll Service Requests")
    print("-" * 90)
    print(f"{'REQUEST ID':<14} {'EMPLOYEE':<20} {'ISSUE':<28} {'PRIORITY':<10} STATUS")
    print("-" * 90)
    for request in requests:
        issue = request.issue if len(request.issue) <= 27 else request.issue[:24] + "..."
        print(
            f"{request.request_id:<14} {request.employee_name[:19]:<20} "
            f"{issue:<28} {request.priority.value:<10} {request.status.value}"
        )
    print("-" * 90)


def search_request(service: RequestService) -> None:
    request_id = input("Enter Request ID to search: ").strip()
    display_request(service.search_request(request_id))


def resolve_request(service: RequestService) -> None:
    request_id = input("Enter Request ID to resolve: ").strip()
    request = service.resolve_request(request_id)
    print(f"\nRequest {request.request_id} has been resolved successfully.")


def display_menu() -> None:
    print("\n========== SMART SERVICE DESK SYSTEM ==========")
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")


def run() -> None:
    repository = FileRepository(DATA_FILE)
    service = RequestService(repository)

    # Validate the persisted file once at startup rather than hiding data errors.
    try:
        service.view_requests()
    except RepositoryError as exc:
        print(f"Startup error: {exc}")
        print("Please correct the data file before restarting.")
        return

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                create_request(service)
            elif choice == "2":
                view_requests(service)
            elif choice == "3":
                search_request(service)
            elif choice == "4":
                resolve_request(service)
            elif choice == "5":
                print("\nThank you for using Smart Service Desk.")
                break
            else:
                print("\nInvalid menu choice. Please enter a number from 1 to 5.")
        except RequestAlreadyResolvedError as exc:
            print(f"\n{exc}")
        except DomainError as exc:
            print(f"\nError: {exc}")
        except RepositoryError as exc:
            print(f"\nStorage error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\n\nApplication interrupted. Goodbye.")
            break


if __name__ == "__main__":
    run()