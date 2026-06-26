"""Argument-validation tests. These run before any network access or token
lookup, so they need no API token or mock."""

import pytest

import diariopy


def test_store_token_rejects_invalid():
    for bad in (123, "", "   ", None):
        with pytest.raises(ValueError):
            diariopy.store_token(bad)


def test_perform_request_validates_arguments():
    with pytest.raises(ValueError):
        diariopy.perform_request("")
    with pytest.raises(ValueError):
        diariopy.perform_request(123)
    with pytest.raises(ValueError):
        diariopy.perform_request("v1/obras", method="FETCH")
    with pytest.raises(ValueError):
        diariopy.perform_request("v1/obras", method="")
    with pytest.raises(ValueError):
        diariopy.perform_request("v1/obras", query="status=1")
    with pytest.raises(ValueError):
        diariopy.perform_request("v1/obras", body="not-a-dict")


def test_project_scoped_getters_validate_ids():
    with pytest.raises(ValueError):
        diariopy.get_project_details("")
    with pytest.raises(ValueError):
        diariopy.get_task_list(None)
    with pytest.raises(ValueError):
        diariopy.get_task_details("p", "")
    with pytest.raises(ValueError):
        diariopy.get_report_details("p", 7)


def test_get_reports_validates_limit_and_order():
    with pytest.raises(ValueError):
        diariopy.get_reports("p", limit=0)
    with pytest.raises(ValueError):
        diariopy.get_reports("p", limit=-1)
    with pytest.raises(ValueError):
        diariopy.get_reports("p", limit="ten")
    with pytest.raises(ValueError):
        diariopy.get_reports("p", limit=True)  # bool is not a valid count
    with pytest.raises(ValueError):
        diariopy.get_reports("p", order="ascending")
    with pytest.raises(ValueError):
        diariopy.get_reports("p", order="ASC")
