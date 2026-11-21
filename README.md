# Smart Service Desk Management System

A Python-based command-line application for managing employee IT support requests. The application follows a layered architecture, applies object-oriented programming principles, and uses JSON-based file storage for persistent data management.

## 1. Project Overview

The Smart Service Desk Management System helps organizations manage employee IT support requests through a simple command-line interface.

Employees can create support requests, view all requests, search for a specific request, and resolve open requests.

The application is designed with separation of concerns, maintainability, and testability in mind.

## 2. Features

- Create employee IT support requests.
- Generate and manage unique request IDs.
- Assign request priorities (LOW, MEDIUM, HIGH).
- View all registered service requests.
- Search requests using Request ID.
- Resolve open service requests.
- Prevent duplicate request IDs.
- Prevent resolving an already resolved request.
- Validate user input and request data.
- Handle application errors using custom exceptions.
- Store application data in a JSON file.
- Preserve data across application restarts.
- Unit testing using Python's built-in unittest framework.

## 3. Project Architecture

The application follows a layered architecture to separate business logic, application operations, infrastructure and user interaction.

```text
smart-service-desk/
│
├── application/
│   ├── __init__.py
│   ├── request_repository.py
│   └── request_service.py
│
├── domain/
│   ├── __init__.py
│   ├── exceptions.py
│   └── service_request.py
│
├── infrastructure/
│   ├── __init__.py
│   └── file_repository.py
│
├── data/
│   └── requests.json
│
├── tests/
│   ├── __init__.py
│   ├── test_request_service.py
│   └── test_service_request.py
│
├── main.py
├── README.md
└── .gitignore
```

### Layer Responsibilities

**Domain Layer**

Contains the core business entities and business rules.

- `service_request.py` – Defines the ServiceRequest entity, priority, status, validations and status transition rules.
- `exceptions.py` – Defines custom domain exceptions.

**Application Layer**

Coordinates application use cases.

- `request_service.py` – Implements request creation, searching, viewing and resolution.
- `request_repository.py` – Defines the repository contract using Python Protocol.

**Infrastructure Layer**

Handles external storage operations.

- `file_repository.py` – Implements JSON file reading, writing, serialization and data reconstruction.

**Presentation Layer**

- `main.py` – Provides the command-line interface and handles user input, output and application-level error handling.

**Data Layer**

- `requests.json` – Stores service request records persistently.

**Testing Layer**

- `test_service_request.py` – Tests domain entity validation and business rules.
- `test_request_service.py` – Tests application operations, duplicate prevention, searching and persistence.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| OOP | Encapsulation and object-oriented design |
| Dataclasses | Entity implementation |
| Enum | Request priority and status management |
| JSON | Data persistence |
| pathlib | File and directory management |
| Protocol | Repository abstraction |
| unittest | Automated testing |
| Git | Version control |
| GitHub | Source code management and collaboration |

No external Python packages are required for the current implementation.

## 5. Business Rules

The application follows these business rules:

1. Every service request must have a valid Request ID.
2. Employee name and issue description cannot be empty.
3. Request priority must be LOW, MEDIUM or HIGH.
4. Every newly created request starts with OPEN status.
5. Request IDs must be unique, regardless of letter casing.
6. Only OPEN requests can be resolved.
7. A RESOLVED request cannot be resolved again.
8. Request changes must be saved to persistent storage.

### Request Status Lifecycle

```text
       CREATE REQUEST
              |
              v
          +-------+
          | OPEN  |
          +-------+
              |
              | Resolve Request
              v
        +------------+
        |  RESOLVED  |
        +------------+
              |
              v
       Further resolution
          NOT ALLOWED
```

## 6. Custom Exception Handling

The application uses custom exceptions to handle business-related errors.

| Exception | Description |
|---|---|
| DomainError | Base class for domain exceptions |
| DuplicateRequestError | Raised when a request ID already exists |
| RequestNotFoundError | Raised when a request cannot be found |
| InvalidPriorityError | Raised when an unsupported priority is provided |
| InvalidRequestDataError | Raised when request information is invalid |
| RequestAlreadyResolvedError | Raised when an already resolved request is resolved again |
| RepositoryError | Raised when JSON storage operations fail |

These exceptions provide meaningful error messages and prevent unexpected application termination for anticipated errors.

## 7. Installation and Execution

### Prerequisites

- Python 3.10 or later.
- Git.
- VS Code or any Python-compatible editor.

### Step 1: Clone the repository

```bash
git clone https://github.com/vikas-training/smart-service-desk.git
```

### Step 2: Navigate to the project directory

```bash
cd smart-service-desk
```

### Step 3: Run the application

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

## 8. Application Menu

```text
========== SMART SERVICE DESK SYSTEM ==========

1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit

Enter your choice:
```

### Sample Request Creation

```text
Enter your choice: 1

Enter Request ID: SR101
Enter Employee Name: Rahul
Enter Issue Description: Laptop is not starting
Enter Priority (LOW/MEDIUM/HIGH): HIGH

Service request SR101 created successfully.
```

### Sample Request Listing

```text
All Service Requests

REQUEST ID     EMPLOYEE     ISSUE                  PRIORITY   STATUS

SR101          Rahul        Laptop is not starting HIGH       OPEN
```

## 9. Data Persistence

The application stores all requests in:

```text
data/requests.json
```

Example JSON record:

```json
[
    {
        "request_id": "SR101",
        "employee_name": "Rahul",
        "issue": "Laptop is not starting",
        "priority": "HIGH",
        "status": "OPEN"
    }
]
```

The repository converts application entities into JSON-compatible dictionaries before saving.

When the application starts again, the repository reads the JSON file and reconstructs ServiceRequest objects.

The implementation also uses temporary-file writing and atomic replacement to improve file-write reliability.

## 10. Running Unit Tests

The project uses Python's built-in unittest framework.

Run all tests using:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- Default request status.
- Priority normalization.
- Invalid priority validation.
- Request resolution.
- Preventing repeated resolution.
- Request creation and searching.
- Duplicate request ID prevention.
- Handling missing requests.
- Persistence of resolved requests.

## 11. Git Branching Strategy

The project uses a feature-based branching strategy to organize development.

### Branch Structure

```text
main
  |
  └── development
         |
         ├── feature/domain-model
         ├── feature/application-model
         ├── feature/infrastructure-model
         └── feature/testing
```

### Development Workflow

1. Create a feature branch from development.
2. Implement the required functionality.
3. Commit the changes.
4. Push the feature branch to GitHub.
5. Create a Pull Request.
6. Review and merge the feature into development.
7. Test the integrated application.
8. Merge development into main.

### Useful Git Commands

```bash
# Fetch latest remote changes
git fetch --all

# Switch to development
git switch development

# Create a feature branch
git switch -c feature/new-feature

# Stage changes
git add .

# Commit changes
git commit -m "implemented new feature"

# Push feature branch
git push -u origin feature/new-feature

# View commit history
git log --oneline --graph --decorate --all
```

## 12. Design Principles Followed

The project applies the following software engineering principles:

- **Single Responsibility Principle:** Each component has a clearly defined responsibility.
- **Separation of Concerns:** Business logic, application operations and storage are maintained separately.
- **Dependency Inversion:** Application services depend on the repository abstraction rather than directly depending on JSON storage.
- **Encapsulation:** Request data and business behaviour are managed through the ServiceRequest entity.
- **DRY:** Common validations and business operations are centralized.
- **Testability:** Business logic and application operations can be tested independently.

## 13. Future Enhancements

Possible future improvements include:

- Replace JSON storage with SQLite or PostgreSQL.
- Introduce employee authentication and role-based access.
- Add request assignment to support engineers.
- Introduce additional statuses such as IN_PROGRESS and CLOSED.
- Add request creation timestamps and resolution timestamps.
- Implement logging and audit history.
- Develop a REST API using FastAPI or Flask.
- Build a web-based dashboard for service request management.

## 14. Conclusion

The Smart Service Desk Management System demonstrates practical Python application development using object-oriented programming, layered architecture, custom exception handling, repository abstraction, JSON persistence, automated testing and Git-based version control.

The project focuses on writing maintainable, modular and testable code while implementing the essential operations of an employee IT support management system.

---

**Repository:** https://github.com/vikas-training/smart-service-desk

**Language:** Python

**Project Type:** Command-Line Application

**Architecture:** Layered Architecture