"""diariopy: Python interface to the Diário de Obras (diariodeobras.net) API."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .client import (
    DiarioError,
    get_company,
    get_entities,
    get_project_details,
    get_projects,
    get_report_details,
    get_reports,
    get_task_details,
    get_task_list,
    perform_request,
    retrieve_token,
    store_token,
)

try:
    __version__ = version("diariopy")
except PackageNotFoundError:  # package not installed (e.g. running from source)
    __version__ = "0.0.0"

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
    "__version__",
]
