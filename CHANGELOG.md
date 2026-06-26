# Changelog

All notable changes to **diariopy** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-26

Initial release — a Python port of the R package
[`diario`](https://github.com/StrategicProjects/diario).

### Added

- Secure API token storage via `keyring` (`store_token`, `retrieve_token`), using the
  same keyring service as the R package so they interoperate on one machine.
- Authenticated requests via `requests`, centralized in `perform_request`, with the
  `token` auth header and JSON handling.
- Convenience wrappers: `get_company`, `get_entities`, `get_projects`,
  `get_project_details`, `get_task_list`, `get_task_details`, `get_reports`,
  `get_report_details`.
- `get_task_list` unwraps the API's `cronograma` envelope (one item per task).
- Configurable base URL via the `DIARIO_BASE_URL` environment variable.
- Typed API (`py.typed`), idiomatic errors (`ValueError` for bad arguments,
  `DiarioError` for transport/HTTP/content failures), and `logging` instead of prints.
- Test suite with the network mocked (`responses`); CI across Python 3.9–3.13.
- Documentation site (MkDocs Material) and PyPI publishing via trusted publishing.

[Unreleased]: https://github.com/StrategicProjects/diariopy/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/StrategicProjects/diariopy/releases/tag/v0.1.0
