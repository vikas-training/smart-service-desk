# Smart Service Desk Management System

A small command-line application for creating, viewing, searching, and resolving employee IT support requests. Requests are persisted in a JSON file so that data remains available after the application is restarted.

## Features

- Create requests with a unique Request ID, employee name, issue, and priority.
- View all saved requests.
- Search by Request ID.
- Resolve an open request (`OPEN -> RESOLVED`).
- Persist requests in `data/requests.json`.
- Friendly handling for duplicate IDs, missing requests, invalid priorities, and repeated resolution.