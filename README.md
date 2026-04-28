# AAS HTTP Client

[![PyPI version](https://img.shields.io/pypi/v/aas-http-client.svg)](https://pypi.org/project/aas-http-client/)
[![License: MIT](https://img.shields.io/badge/license-MIT-%23f8a602?label=License&labelColor=%23992b2e)](https://github.com/fluid40/aas-http-client/blob/dk/doxygen/LICENSE)
[![CI](https://github.com/fluid40/aas-http-client/actions/workflows/CI.yml/badge.svg?branch=main&cache-bust=1)](https://github.com/fluid40/aas-http-client/actions)

AAS HTTP Client is a flexible Python library for interacting with Asset Administration Shell (AAS) and submodel repository servers over HTTP. It uses standard Python dictionaries for function inputs and outputs, making it easy to integrate with a variety of workflows. The client implements the most widely used endpoints defined in the [AAS server specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1.1/specification/interfaces.html), ensuring compatibility with multiple AAS repository server implementations. This allows you to connect to different AAS servers without changing your client code.

**Notes:**

* Each client instance communicates with exactly one AAS server (1-to-1 mapping). For multiple servers, create multiple instances.
* From version 1.0.0 the client includes implementations for all endpoints from BaSxy Java SDK 'aas-registry', 'submodel-registry' and 'aas-environment'.

**Table of Contents:**

- [AAS HTTP Client](#aas-http-client)
  - [🚀 Features](#-features)
  - [🏗️ Supported Servers](#️-supported-servers)
  - [🧰 Wrappers](#-wrappers)
  - [🔧 Provided Utilities](#-provided-utilities)
  - [📚 Resources](#-resources)
  - [⚡ Quickstart](#-quickstart)

---

## 🚀 Features

* ✅ Easy REST communication with AAS-compliant servers
* ✅ Support for Registry, AAS, and Submodel Repository endpoints
* ✅ Optional wrapper for the Eclipse BaSyx Python SDK
* ✅ Built-in authentication (Bearer, OAuth, Basic)
* ✅ Pagination support
* ✅ Utility modules (encoding, model builder, SDK tools)
* ✅ Tested with multiple AAS server implementations

---

## 🏗️ Supported Servers

The client has been tested with:

* <https://github.com/fluid40/basyx-dotnet>
* <https://github.com/eclipse-basyx/basyx-java-sdk>
* <https://github.com/eclipse-basyx/basyx-python-sdk>

Actual behavior depends on each server's implementation of the [AAS Specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1.1/specification/interfaces.htm)

## 🧰 Wrappers

Wrappers provide a higher-level interface on top of the raw HTTP client. Use them when you want to work with SDK objects instead of plain Python dictionaries returned by the REST API.

Currently available wrappers:

* [Eclipse BaSyx Python SDK](https://github.com/eclipse-basyx/basyx-python-sdk)

What the BaSyx Wrapper Adds:

* Accepts and returns `basyx.aas.model` objects for common AAS and submodel operations
* Reuses the same connection and authentication settings as the base HTTP client
* Supports wrapper creation from a URL, a Python dictionary, or a configuration file
* Keeps low-level client access available through `wrapper.get_client()` when needed

## 🔧 Provided Utilities

The AAS HTTP Client package also include some utility functions for for recurring tasks (provided by import `aas_http_client.utilities` ):

* **encoder**: base64 encoding and decoding
* **sdk_tools**: e.g. Framework object serialization and deserialization, basic submodel operations
* **model_builder**: creation of some basic AAS model elements

See [Utilities API Reference](https://fluid40.github.io/aas-http-client/namespaceaas__http__client_1_1utilities.html)

---

## 📚 Resources

📘 [Documentation](https://fluid40.github.io/aas-http-client/)

📝 [Changelog](docs/CHANGELOG.md)

🤖 [GitHub Releases](http://github.com/fluid40/aas-http-client/releases)

📦 [Pypi Packages](https://pypi.org/project/aas-http-client/)

📜 [MIT License](https://github.com/fluid40/aas-http-client/blob/main/LICENSE)

---

## ⚡ Quickstart

For a detailed introduction, please read [Getting Started](docs/getting_started.md).

```bash
pip install aas-http-client
```

### Client

```python
from aas_http_client.classes.client import aas_client

client = aas_client.create_by_url(base_url="http://localhost:8081")

shells_paginated = client.shells.get_all_asset_administration_shells()
print(shells_paginated.get("results", []))
```

### Wrapper

```python
from aas_http_client.classes.wrapper import sdk_wrapper

wrapper = sdk_wrapper.create_by_url(base_url="http://localhost:8081")

shells = wrapper.get_all_asset_administration_shells()
print(shells)

```
