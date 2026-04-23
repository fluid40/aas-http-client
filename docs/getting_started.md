# 🚀 Getting Started

This guide will walk you through installing and using `aas-http-client` .

- [🚀 Getting Started](#-getting-started)
  - [Installation](#installation)
  - [Client Creation Methods](#client-creation-methods)
    - [1. Create Client by URL](#1-create-client-by-url)
    - [2. Create Client by Dictionary](#2-create-client-by-dictionary)
    - [3. Create Client by Configuration File](#3-create-client-by-configuration-file)
  - [Wrapper Creation Methods](#wrapper-creation-methods)
    - [1. Create Wrapper by URL](#1-create-wrapper-by-url)
    - [2. Create Wrapper by Dictionary](#2-create-wrapper-by-dictionary)
    - [3. Create Wrapper by Configuration File](#3-create-wrapper-by-configuration-file)

---

## Installation

Install via pip:

```bash
pip install aas-http-client
```

For detailed configuration options and examples, see the [Configuration Guide](configuration.md).

---

## Client Creation Methods

There are three ways to create an AAS HTTP client or wrapper.

### 1. Create Client by URL

Create a client by providing parameters directly:

```python
from aas_http_client.classes.client import aas_client

client = aas_client.create_client_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password="password123",
    time_out=300,
    ssl_verify=True
)
```

Create a wrapper by providing parameters directly:

```python
from aas_http_client.classes.wrapper import sdk_wrapper

wrapper = sdk_wrapper.create_wrapper_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password="password123",
    time_out=300,
    ssl_verify=True
)
```

### 2. Create Client by Dictionary

Create a client using a configuration dictionary:

```python
from aas_http_client.classes.client import aas_client

config = {
    "BaseUrl": "http://localhost:8080",
    "TimeOut": 300,
    "AuthenticationSettings": {
        "BasicAuth": {
            "Username": "admin"
        }
    }
}

client = aas_client.create_client_by_dict(
    configuration=config,
    basic_auth_password="password123"
)
```

### 3. Create Client by Configuration File

Create a client using a JSON configuration file:

```python
from pathlib import Path
from aas_http_client.classes.client import aas_client

config_file = Path("config.json")
client = aas_client.create_client_by_config(
    config_file=config_file,
    basic_auth_password="password123"
)
```

## Wrapper Creation Methods

Wrapper creation follows the same pattern as client creation.

### 1. Create Wrapper by URL

Create a wrapper by providing parameters directly:

```python
from aas_http_client.classes.wrapper import sdk_wrapper

wrapper = sdk_wrapper.create_wrapper_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password="password123",
    time_out=300,
    ssl_verify=True
)
```

### 2. Create Wrapper by Dictionary

Create a wrapper using a configuration dictionary:

```python
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

client = sdk_wrapper.create_wrapper_by_dict(
    configuration=config,
    basic_auth_password="password123"
)
```

### 3. Create Wrapper by Configuration File

Create a wrapper using a JSON configuration file:

```python
from pathlib import Path
from aas_http_client.classes.wrapper import sdk_wrapper

config_file = Path("config.json")
client = sdk_wrapper.create_wrapper_by_config(
    config_file=config_file,
    basic_auth_password="password123"
)
```
