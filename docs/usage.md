# Usage

## Authentication

Before any request, store your API token once. It is kept in the operating system's
keyring (service `DiarioAPI_Token`), so it persists across sessions and is shared with
the R `diario` package on the same machine.

```python
import diariopy

diariopy.store_token("YOUR_API_TOKEN_HERE")  # returns True on success
diariopy.retrieve_token()                    # -> the token, or None
```

## Retrieving data

All getters return parsed JSON (Python `dict`/`list`).

```python
project_id = "6717f864d163f517ae06e242"

diariopy.get_company()                          # company details
diariopy.get_entities()                         # registered entities (cadastros)
diariopy.get_projects()                         # list of projects (obras)
diariopy.get_project_details(project_id)        # one project

tasks = diariopy.get_task_list(project_id)      # schedule items (cronograma)
diariopy.get_task_details(project_id, task_id)

reports = diariopy.get_reports(project_id, limit=10, order="asc")
diariopy.get_report_details(project_id, report_id)
```

## Error handling

- Invalid arguments raise `ValueError`.
- Transport failures, HTTP errors, and unexpected content types raise
  `diariopy.DiarioError` (the API's own error message is included when available).
- When no token is stored, request functions log a warning and return `None`.

```python
from diariopy import DiarioError

try:
    diariopy.get_project_details("does-not-exist")
except DiarioError as exc:
    print("Request failed:", exc)
```

## Configuration

- **Base URL** — override with the `DIARIO_BASE_URL` environment variable (useful for
  staging environments or mocking in tests).
- **Logging** — the package logs through the `diariopy` logger and never prints. Enable
  it with:

    ```python
    import logging
    logging.basicConfig(level=logging.INFO)
    ```

## Low-level requests

For endpoints without a dedicated wrapper, call `perform_request` directly:

```python
diariopy.perform_request("v1/obras", query={"status": "active"}, method="GET")
```
