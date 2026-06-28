# diariopy

<p align="center">
  <img src="assets/diariopy-hex.svg" alt="diariopy hex logo" width="200">
</p>

**diariopy** is a Python interface to the [diariodeobras.net](https://diariodeobras.net)
("Diário de Obras") platform — the Python counterpart of the R package
[`diario`](https://github.com/StrategicProjects/diario). It securely stores an API
token and wraps authenticated requests to retrieve projects, tasks, reports, and more.

!!! note "Disclaimer"
    This package is a wrapper for the API provided by the **Diário de Obras**
    platform, which owns the data. Function and argument names are in English, but
    because the source API is in Portuguese, **response keys and some data values are
    returned in Portuguese**. Access requires a valid authentication token issued by
    the platform.

## Installation

```bash
pip install diariopy
```

## Quick start

```python
import diariopy

# Store your API token securely (uses the system keyring)
diariopy.store_token("YOUR_API_TOKEN_HERE")

# Make authenticated requests
company = diariopy.get_company()
projects = diariopy.get_projects()
```

See [Usage](usage.md) for more examples and the [API reference](reference.md) for the
full function list.

## Links

- PyPI: <https://pypi.org/project/diariopy/>
- Source: <https://github.com/StrategicProjects/diariopy>
- R sibling package: <https://github.com/StrategicProjects/diario>
