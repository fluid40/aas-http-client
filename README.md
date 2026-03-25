
# AAS HTTP Client – Python Library

[![License: MIT](https://img.shields.io/badge/license-MIT-%23f8a602?label=License&labelColor=%23992b2e)](LICENSE)
[![CI](https://github.comclient)](https://github.com/fluid40/aas-http-client/actions)
[![PyPI version](https://img.shields.io/pypi/v/aas-http-client.svg)](https://pypi.org/project/aas-http-client/)

The **AAS HTTP Client** is a flexible and powerful Python library for communicating with Asset Administration Shell (AAS) servers over HTTP. It provides a clean API, type hints, and a consistent data model based on standard Python dictionaries.

> **Note:** Each client instance communicates with exactly one AAS server (1:1 mapping).
> For multiple servers, create multiple instances.

Version 1.0.0 includes implementations for all endpoints from BaSxy Java SDK 'aas-registry', 'submodel-registry' and 'aas-environment'.

---


## 🚀 Features

- ✅ Easy REST communication with AAS-compliant servers
- ✅ Full support for Registry, AAS, and Submodel Repository endpoints
- ✅ Optional wrapper for the Eclipse BaSyx Python SDK
- ✅ Built-in authentication (Bearer, OAuth, Basic)
- ✅ Pagination support
- ✅ Utility modules (encoding, model builder, SDK tools)
- ✅ Tested with multiple AAS server implementations

---

## 🏗️ Supported Servers

The client has been tested with:

- [Eclipse BaSyx .NET SDK (Fluid 4.0 fork)](https://github.com/fluid40/basyx-dotnet)
- [Eclipse BaSyx Java SDK](https://github.com/eclipse-basyx/basyx-java-sdk)
- [Eclipse BaSyx Python SDK](https://github.com/eclipse-basyx/basyx-python-sdk)

Compatibility depends on the server's adherence to the
[AAS Specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1.1/specification/interfaces.html).

## 📦 Installation

```bash
pip install aas-http-client


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

client = create_client_by_url(
    base_url="http://myaasserver:5043/"
)

print(client.shell.get_shells())
```

### BaSyx Python SDK Wrapper

```python
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_url

wrapper = create_wrapper_by_url(
    base_url="http://myaasserver:5043/"
)

print(wrapper.get_shells())
```
