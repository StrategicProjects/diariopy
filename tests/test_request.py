"""Tests for the request layer. HTTP is mocked with ``responses`` and the token
lookup is stubbed, so these tests never touch keyring or the real API."""

import pytest
import responses

import diariopy
from diariopy import client

API = "https://apiexterna.diariodeobra.app"


@pytest.fixture
def token(monkeypatch):
    """Stub the token lookup so requests proceed without keyring."""
    monkeypatch.setattr(client, "retrieve_token", lambda quiet=False: "fake-token")


@responses.activate
def test_perform_request_returns_json(token):
    responses.add(
        responses.GET, f"{API}/v1/empresa",
        json={"nome": "Empresa A"}, status=200,
    )
    assert diariopy.perform_request("v1/empresa") == {"nome": "Empresa A"}


@responses.activate
def test_perform_request_sends_token_header(token):
    responses.add(responses.GET, f"{API}/v1/empresa", json={}, status=200)
    diariopy.perform_request("v1/empresa")
    assert responses.calls[0].request.headers["token"] == "fake-token"


@responses.activate
def test_perform_request_empty_body_returns_none(token):
    responses.add(responses.DELETE, f"{API}/v1/empresa", status=204)
    assert diariopy.perform_request("v1/empresa", method="DELETE") is None


def test_perform_request_no_token_returns_none(monkeypatch):
    monkeypatch.setattr(client, "retrieve_token", lambda quiet=False: None)
    assert diariopy.perform_request("v1/empresa") is None


@responses.activate
def test_perform_request_raises_on_http_error(token):
    responses.add(
        responses.GET, f"{API}/v1/empresa",
        json={"message": "Token invalido"}, status=401,
    )
    with pytest.raises(diariopy.DiarioError, match="Token invalido"):
        diariopy.perform_request("v1/empresa")


@responses.activate
def test_get_reports_sends_query_params(token):
    responses.add(
        responses.GET, f"{API}/v1/obras/abc/relatorios", json=[], status=200,
    )
    diariopy.get_reports("abc", limit=3, order="asc")
    params = responses.calls[0].request.params
    assert params["limite"] == "3"
    assert params["ordem"] == "asc"


@responses.activate
def test_get_task_list_unwraps_cronograma(token):
    responses.add(
        responses.GET, f"{API}/v1/obras/abc/lista-de-tarefas",
        json={"totalTarefas": 2, "cronograma": [{"_id": "t1"}, {"_id": "t2"}]},
        status=200,
    )
    tasks = diariopy.get_task_list("abc")
    assert [t["_id"] for t in tasks] == ["t1", "t2"]


@responses.activate
def test_get_task_list_empty_when_no_schedule(token):
    responses.add(
        responses.GET, f"{API}/v1/obras/abc/lista-de-tarefas",
        json={"totalTarefas": 0}, status=200,
    )
    assert diariopy.get_task_list("abc") == []


@responses.activate
def test_base_url_override(token, monkeypatch):
    monkeypatch.setenv("DIARIO_BASE_URL", "https://staging.example/")
    responses.add(
        responses.GET, "https://staging.example/v1/empresa",
        json={"ok": True}, status=200,
    )
    assert diariopy.perform_request("v1/empresa") == {"ok": True}
