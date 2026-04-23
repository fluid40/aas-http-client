# 🚀 Getting Started

This guide will walk you through installing and using `aas-http-client`.

- [🚀 Getting Started](#-getting-started)
  - [Installation](#installation)
  - [Creation Methods](#creation-methods)
    - [Create by URL](#create-by-url)
    - [Create by Dictionary](#create-by-dictionary)
    - [Create by Configuration File](#create-by-configuration-file)

---

## Installation

Prerequisites:

- Python 3.10 or newer
- Access to an AAS server endpoint

Install via pip:

```bash
pip install aas-http-client
```

For detailed configuration options, authentication methods and examples, see the [Configuration Guide](configuration.md).

---

## Creation Methods

There are three ways to create an AAS HTTP client or wrapper.
Use either a client (dictionary-based API) or a wrapper (SDK object-based API), depending on your use case.

For production usage, avoid hardcoding secrets in source code. Load credentials from environment variables or a secret manager.

### Create by URL

Create a client or wrapper by providing parameters directly using `create_by_url`:

```python
import os

from aas_http_client.classes.client import aas_client
from aas_http_client.classes.wrapper import sdk_wrapper

client = aas_client.create_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password=os.getenv("AAS_BASIC_AUTH_PASSWORD", ""),
    time_out=300,
    ssl_verify=True
)

wrapper = sdk_wrapper.create_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password=os.getenv("AAS_BASIC_AUTH_PASSWORD", ""),
    time_out=300,
    ssl_verify=True
)

if client is None:
    raise RuntimeError("Client creation failed")

if wrapper is None:
    raise RuntimeError("Wrapper creation failed")

print("Client connectivity:", client.get_root() is not None)
print("Wrapper connectivity:", wrapper.get_client().get_root() is not None)
```

### Create by Dictionary

Create a client or wrapper using a configuration dictionary with `create_by_dict`:

```python
import os

from aas_http_client.classes.client import aas_client
from aas_http_client.classes.wrapper import sdk_wrapper

config = {
    "BaseUrl": "http://localhost:8080",
    "TimeOut": 300,
    "AuthenticationSettings": {
        "BasicAuth": {
            "Username": "admin"
        }
    }
}

client = aas_client.create_by_dict(
    configuration=config,
    basic_auth_password=os.getenv("AAS_BASIC_AUTH_PASSWORD", "")
)

wrapper = sdk_wrapper.create_by_dict(
    configuration=config,
    basic_auth_password=os.getenv("AAS_BASIC_AUTH_PASSWORD", "")
)

if client is None:
    raise RuntimeError("Client creation failed")

if wrapper is None:
    raise RuntimeError("Wrapper creation failed")

print("Client connectivity:", client.get_root() is not None)
print("Wrapper connectivity:", wrapper.get_client().get_root() is not None)
```

### Create by Configuration File

Create a client or wrapper using a JSON configuration file with `create_by_config`:

```python
import os

from pathlib import Path
from aas_http_client.classes.client import aas_client
from aas_http_client.classes.wrapper import sdk_wrapper

config_file = Path("config.json")
client = aas_client.create_by_config(
    config_file=config_file,
    basic_auth_password=os.getenv("AAS_BASIC_AUTH_PASSWORD", "")
)

wrapper = sdk_wrapper.create_by_config(
    config_file=config_file,
    basic_auth_password=os.getenv("AAS_BASIC_AUTH_PASSWORD", "")
)

if client is None:
    raise RuntimeError("Client creation failed")

if wrapper is None:
    raise RuntimeError("Wrapper creation failed")

print("Client connectivity:", client.get_root() is not None)
print("Wrapper connectivity:", wrapper.get_client().get_root() is not None)
```
