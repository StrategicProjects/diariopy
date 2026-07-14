# diariopy

Python port of the R package [`diario`](https://github.com/StrategicProjects/diario):
a thin client for the [diariodeobras.net](https://diariodeobras.net) ("Diário de
Obras") construction-log API. Stores an API token securely and performs
authenticated requests.

- PyPI distribution **and** import name: `diariopy` (the name `diario` was taken on
  PyPI). Repo: `StrategicProjects/diariopy` (public).
- The R sibling lives in `../diario`. Keep behaviour in parity when changing either.
  Both READMEs cross-link.

**Current status (2026-07-14):** v0.1.1 (Zenodo archival release); docs site live at
https://strategicprojects.github.io/diariopy/ ; CI green on Python 3.9–3.13. GitHub
Actions already pinned to Node-24 majors (checkout@v5, setup-uv@v7,
upload/download-artifact@v5). Author list corrected and expanded to 7 (parity with
the R sibling `diario`); Marcos's display surname is "Wasiliew" (email keeps
"wasilew"). Archived to Zenodo via the GitHub integration — `CITATION.cff` and
`.zenodo.json` present; DOI badge in README.

Hex sticker logo added: `docs/assets/diariopy-hex.svg` (tower crane building over a
structure, teal palette matching the docs theme, amber `py` accent). Wired into the
README header, `docs/index.md`, and the MkDocs theme `logo`/`favicon`. The R sibling
`../diario` got a matching twin logo (same scene; `diario` wordmark with an R-blue `R`
accent) at `man/figures/diario-hex.svg` + regenerated `logo.png`/pkgdown favicons —
keep the two hex logos in visual parity.

## Layout (src layout)

- `src/diariopy/client.py` — the entire implementation (all public functions).
- `src/diariopy/__init__.py` — re-exports the public API and `__version__`.
- `src/diariopy/py.typed` — PEP 561 marker (the package is typed).
- `tests/test_validation.py` — argument checks (no network).
- `tests/test_request.py` — request layer, HTTP mocked with `responses`.
- `pyproject.toml` — hatchling build; version is set here.
- `.github/workflows/` — `ci.yml` (pytest matrix) and `publish.yml` (PyPI).

## Conventions

- **Libraries, not CLIs**: raise exceptions, do not print. `ValueError` for bad
  arguments; `DiarioError` for transport/HTTP/content failures. Use the `diariopy`
  `logging` logger for info/warnings (e.g. token stored, no token found).
- **Token storage**: `keyring`, service `"DiarioAPI_Token"`, username `"global"`
  (same as the R package, so they interoperate on one machine).
- **HTTP**: `requests`, centralized in `perform_request()`. Auth header is `token`
  (not `Authorization`). Base URL defaults to
  `https://apiexterna.diariodeobra.app/` and is overridable via the
  `DIARIO_BASE_URL` env var (used to mock in tests).
- **Return types**: parsed JSON (`dict`/`list`) — not pandas, to stay dependency
  light. `get_task_list()` unwraps the API's `cronograma` envelope.
- Empty bodies (e.g. `204`) return `None`; non-JSON content raises `DiarioError`.
- Support Python >= 3.9. Use `from __future__ import annotations`.

## Dev workflow

```bash
uv sync --extra test          # create .venv and install deps + test extras
uv run pytest -q              # tests mock the network; no token/keyring needed
uv build                      # build sdist + wheel into dist/
uv run python -c "import diariopy; print(diariopy.__version__)"
```

Tests stub the token with `monkeypatch.setattr(client, "retrieve_token", ...)` and
mock HTTP with the `responses` library — never hit the real API or keyring.

## Release / publishing

PyPI publishing uses **trusted publishing (OIDC)** — no API token stored. One-time
setup on PyPI: add a trusted publisher for project `diariopy`, owner
`StrategicProjects`, repo `diariopy`, workflow `publish.yml`, environment `pypi`.
Then:

1. Bump `version` in `pyproject.toml`.
2. Commit, push, and create a GitHub Release (tag `vX.Y.Z`).
3. `publish.yml` builds and uploads to PyPI automatically.
