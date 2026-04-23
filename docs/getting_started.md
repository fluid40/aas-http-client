# 🚀 Getting Started

This guide will walk you through installing and using `aas-http-client` .

- [🚀 Getting Started](#-getting-started)
  - [Installation](#installation)
  - [Client / Wrapper Creation Methods](#client--wrapper-creation-methods)
    - [1. Create by URL](#1-create-by-url)
    - [2. Create by Dictionary](#2-create-by-dictionary)
    - [3. Create by Configuration File](#3-create-by-configuration-file)

---

## Installation

Install via pip:

```bash
pip install aas-http-client
```

For detailed configuration options, authentication methods and examples, see the [Configuration Guide](configuration.md).

---

## Client / Wrapper Creation Methods

There are three ways to create an AAS HTTP client or wrapper.

### 1. Create by URL

Create a client or wrapper by providing parameters directly using `create_by_url`:

```python
from aas_http_client.classes.client import aas_client
from aas_http_client.classes.wrapper import sdk_wrapper

client = aas_client.create_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password="password123",
    time_out=300,
    ssl_verify=True
)

wrapper = sdk_wrapper.create_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password="password123",
    time_out=300,
    ssl_verify=True
)
```

### 2. Create by Dictionary

Create a client or wrapper using a configuration dictionary with `create_by_dict`:

```python
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
    basic_auth_password="password123"
)

wrapper = sdk_wrapper.create_by_dict(
    configuration=config,
    basic_auth_password="password123"
)
```

### 3. Create by Configuration File

Create a client or wrapper using a JSON configuration file with `create_by_config`:

```python
from pathlib import Path
from aas_http_client.classes.client import aas_client
from aas_http_client.classes.wrapper import sdk_wrapper

config_file = Path("config.json")
client = aas_client.create_by_config(
    config_file=config_file,
    basic_auth_password="password123"
)

wrapper = sdk_wrapper.create_by_config(
    config_file=config_file,
    basic_auth_password="password123"
)
```
