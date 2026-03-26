
# AAS HTTP Client


[![License: MIT](https://img.shields.io/badge/license-MIT-%23f8a602?label=License&labelColor=%23992b2e)](https://github.com/fluid40/aas-http-client/blob/dk/doxygen/LICENSE)

[![CI](https://github.com/fluid40/aas-http-client/actions/workflows/CI.yml/badge.svg?branch=main&cache-bust=1)](https://github.com/fluid40/aas-http-client/actions)

[![PyPI version](https://img.shields.io/pypi/v/aas-http-client.svg)](https://pypi.org/project/aas-http-client/)

AAS HTTP Client is a flexible Python library for interacting with Asset Administration Shell (AAS) and submodel repository servers over HTTP. It uses standard Python dictionaries for function inputs and outputs, making it easy to integrate with a variety of workflows. The client implements the most widely used endpoints defined in the [AAS server specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1.1/specification/interfaces.html), ensuring compatibility with multiple AAS repository server implementations. This allows you to connect to different AAS servers without changing your client code.


> **Note:** Each client instance communicates with exactly one AAS server (1-to-1 mapping).

> For multiple servers, create multiple instances.

> Version 1.0.0 includes implementations for all endpoints from BaSxy Java SDK 'aas-registry', 'submodel-registry' and 'aas-environment'.

---

## 🚀 Features

- ✅ Easy REST communication with AAS-compliant servers
- ✅ Support for Registry, AAS, and Submodel Repository endpoints
- ✅ Optional wrapper for the Eclipse BaSyx Python SDK
- ✅ Built-in authentication (Bearer, OAuth, Basic)
- ✅ Pagination support
- ✅ Utility modules (encoding, model builder, SDK tools)
- ✅ Tested with multiple AAS server implementations

---

## 🏗️ Supported Servers

The client has been tested with:

- <https://github.com/fluid40/basyx-dotnet>
- <https://github.com/eclipse-basyx/basyx-java-sdk>
- <https://github.com/eclipse-basyx/basyx-python-sdk>

Actual behavior depends on each server's implementation of the
AAS Specification:
<https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1.1/specification/interfaces.htm>

Currently available wrappers:

- [Eclipse BaSyx Python SDK](https://github.com/eclipse-basyx/basyx-python-sdk)

The AAS HTTP Client package also include some utility functions for for recurring tasks (provided by import 'aas_http_client.utilities'):

- encoder: base64 encoding and decoding
- sdk_tools: e.g. Framework object serialization and deserialization, basic submodel operations
- model_builder: creation of some basic AAS model elements

---

## Documentation

🚀 [Getting Started](docs/getting_started.md)

🛠️ [Configuration](docs/configuration.md)

📝 [Changelog](CHANGELOG.md)

## Resources

🤖 [Releases](http://github.com/fluid40/aas-http-client/releases)

📦 [Pypi Packages](https://pypi.org/project/aas-http-client/)

📜 [MIT License](LICENSE)

---

## ⚡ Quickstart

For a detailed introduction, please read [Getting Started](docs/getting_started.md).

```bash
pip install aas-http-client
````

### Client

```python
from aas_http_client import create_client_by_url

client = create_client_by_url("http://localhost:8081")

shells = client.shell.get_shells()
print(shells))
```

### BaSyx Python SDK Wrapper

```python
from aas_http_client import create_client_by_url

client = create_client_by_url("http://localhost:8081")

shells = client.shell.get_shells()
print(shells)
```
