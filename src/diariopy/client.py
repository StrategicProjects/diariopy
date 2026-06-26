"""Python client for the Diário de Obras (diariodeobras.net) external API.

This mirrors the R 'diario' package: it stores an API token securely with
``keyring`` and performs authenticated requests with ``requests``.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional, Union

import keyring
import requests

__all__ = [
    "DiarioError",
    "store_token",
    "retrieve_token",
    "perform_request",
    "get_company",
    "get_entities",
    "get_projects",
    "get_project_details",
    "get_task_list",
    "get_task_details",
    "get_reports",
    "get_report_details",
]

logger = logging.getLogger("diariopy")

_SERVICE = "DiarioAPI_Token"
_USERNAME = "global"
_DEFAULT_BASE_URL = "https://apiexterna.diariodeobra.app/"
_VALID_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")

JSON = Union[dict, list]


class DiarioError(RuntimeError):
    """Raised when an API request fails or returns an unexpected response."""


def _base_url() -> str:
    """Return the API base URL, overridable via the ``DIARIO_BASE_URL`` env var."""
    return os.environ.get("DIARIO_BASE_URL", _DEFAULT_BASE_URL)


def _require_nonempty_str(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"`{name}` must be a non-empty string.")


def store_token(token: str) -> bool:
    """Store the API token securely using ``keyring``.

    Returns ``True`` on success, ``False`` if the keyring is not accessible.
    """
    _require_nonempty_str(token, "token")
    try:
        keyring.set_password(_SERVICE, _USERNAME, token)
    except Exception as exc:  # keyring backends raise a variety of errors
        logger.warning(
            "Could not store the token. Make sure keyring is accessible: %s", exc
        )
        return False
    logger.info("Token stored successfully.")
    return True


def retrieve_token(quiet: bool = False) -> Optional[str]:
    """Retrieve the stored API token, or ``None`` if none is found."""
    try:
        token = keyring.get_password(_SERVICE, _USERNAME)
    except Exception:
        token = None
    if token is None and not quiet:
        logger.info("No valid token found.")
    return token


def _error_message(response: requests.Response) -> Optional[str]:
    """Extract the API's own error message from a failed response, if present."""
    try:
        data = response.json()
    except ValueError:
        return None
    if isinstance(data, dict):
        msg = data.get("message") or data.get("error")
        if isinstance(msg, str) and msg:
            return msg
    return None


def perform_request(
    endpoint: str,
    query: Optional[dict] = None,
    method: str = "GET",
    body: Optional[JSON] = None,
    timeout: float = 30.0,
) -> Optional[JSON]:
    """Perform an authenticated request against the Diario API.

    Returns the parsed JSON body, or ``None`` when there is no stored token or
    the response has no body (e.g. ``204 No Content``). Raises :class:`DiarioError`
    on transport failures, HTTP errors, or unexpected content types.
    """
    _require_nonempty_str(endpoint, "endpoint")
    _require_nonempty_str(method, "method")
    method = method.upper()
    if method not in _VALID_METHODS:
        raise ValueError(f"`method` must be one of {', '.join(_VALID_METHODS)}.")
    if query is not None and not isinstance(query, dict):
        raise ValueError("`query` must be a dict of query parameters or None.")
    if body is not None and not isinstance(body, (dict, list)):
        raise ValueError("`body` must be a dict/list (JSON body) or None.")

    token = retrieve_token(quiet=True)
    if token is None:
        logger.warning(
            "No valid token found. Store your token with store_token()."
        )
        return None

    url = _base_url().rstrip("/") + "/" + endpoint.lstrip("/")
    headers = {"token": token, "Content-Type": "application/json"}
    try:
        response = requests.request(
            method, url, headers=headers, params=query, json=body, timeout=timeout
        )
    except requests.RequestException as exc:
        raise DiarioError(f"Failed to perform the request: {exc}") from exc

    if not response.ok:
        detail = _error_message(response)
        message = f"HTTP {response.status_code} for {endpoint}"
        if detail:
            message += f": {detail}"
        raise DiarioError(message)

    if not response.content:
        return None
    content_type = response.headers.get("Content-Type", "").lower()
    if "application/json" in content_type:
        return response.json()
    raise DiarioError(f"Unexpected content type: {content_type!r}")


def get_company() -> JSON:
    """Retrieve company details."""
    return perform_request("v1/empresa")


def get_entities() -> JSON:
    """Retrieve all registered entities (cadastros)."""
    return perform_request("v1/cadastros")


def get_projects() -> JSON:
    """Retrieve the list of projects (obras)."""
    return perform_request("v1/obras")


def get_project_details(project_id: str) -> JSON:
    """Retrieve details of a specific project by its ID."""
    _require_nonempty_str(project_id, "project_id")
    return perform_request(f"v1/obras/{project_id}")


def get_task_list(project_id: str) -> JSON:
    """Retrieve the task list (schedule items) of a specific project.

    The API wraps the schedule in a ``cronograma`` field alongside summary
    counters; this returns the schedule items themselves.
    """
    _require_nonempty_str(project_id, "project_id")
    data = perform_request(f"v1/obras/{project_id}/lista-de-tarefas")
    if isinstance(data, dict):
        return data.get("cronograma", [])
    return data


def get_task_details(project_id: str, task_id: str) -> JSON:
    """Retrieve details of a specific task within a project."""
    _require_nonempty_str(project_id, "project_id")
    _require_nonempty_str(task_id, "task_id")
    return perform_request(f"v1/obras/{project_id}/lista-de-tarefas/{task_id}")


def get_reports(project_id: str, limit: int = 50, order: str = "desc") -> JSON:
    """Retrieve reports of a specific project.

    ``limit`` is a positive integer; ``order`` is ``"asc"`` or ``"desc"``.
    """
    _require_nonempty_str(project_id, "project_id")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("`limit` must be a positive integer.")
    if order not in ("asc", "desc"):
        raise ValueError("`order` must be 'asc' or 'desc'.")
    return perform_request(
        f"v1/obras/{project_id}/relatorios",
        query={"limite": limit, "ordem": order},
    )


def get_report_details(project_id: str, report_id: str) -> JSON:
    """Retrieve details of a specific report within a project."""
    _require_nonempty_str(project_id, "project_id")
    _require_nonempty_str(report_id, "report_id")
    return perform_request(f"v1/obras/{project_id}/relatorios/{report_id}")
