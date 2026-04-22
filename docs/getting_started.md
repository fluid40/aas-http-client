# 🚀 Getting Started

This guide will walk you through installing and using `aas-http-client` .

---

## 📦 Installation

Install via pip:

```bash
pip install aas-http-client
```

---

## Usage

### Server Configuration

For detailed configuration options and examples, see the [Configuration Guide](configuration.md).

---

## Creation Methods

There are three ways to create an AAS HTTP client or wrapper. Wrapper creation follows the same pattern as client creation.

### 1. Create by URL

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

### 2. Create by Dictionary

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

### 3. Create by Configuration File

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

---

### Wrapper

The wrapper provides high-level methods using BaSyx Python SDK data models for easier integration.

#### 📌 Create Wrapper from Configuration File

Create a wrapper from a given configuration file.

```python
from pathlib import Path
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_config    # import function to create a wrapper by configuration file
import basyx.aas.model                                                      # import BaSyx Python SDK to use the data model

config_file = Path("./server_config.json")                                  # get the config file
wrapper = create_wrapper_by_config(config_file, basic_auth_password="")     # create the wrapper (in this case without password authentication)
```

#### 📌 Create Wrapper via Parameters

Create a wrapper from given parameters.

```python
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_url       # import function to create a wrapper by parameters
import basyx.aas.model                                                      # import BaSyx Python SDK to use the data model

wrapper = create_wrapper_by_url(
    base_url="http://myaasserver:5043/",                                    # Base URL of the AAS server (required)
    basic_auth_username="",                                                 # Username for authentication (optional, default: "")
    basic_auth_password="",                                                 # Password for authentication (optional, default: "")
    http_proxy="",                                                          # HTTP proxy (optional, default: "")
    https_proxy="",                                                         # HTTPS proxy (optional, default: "")
    time_out=200,                                                           # API call timeout in seconds (optional, default: 200)
    connection_time_out=100,                                                # Connection establishment timeout in seconds (optional, default: 100)
    ssl_verify=True,                                                        # Verify TLS/SSL certificates (optional, default: true)
    trust_env=True                                                          # Trust environment variables (optional, default: true)
)
```

#### 📌 Create Wrapper via dictionary

Create a wrapper from given JSON dictionary.

```python
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_dict      # import function to create a wrapper by dictionary

configuration_dict = {
    "BaseUrl": "http://myaasserver:5043/",                  # Base URL of the AAS server (required)
    "HttpsProxy": None,                                     # HTTPS proxy (optional, default: null)
    "HttpProxy": None,                                      # HTTP proxy (optional, default: null)
    "TimeOut": 200,                                         # API call timeout in seconds (optional, default: 200)
    "ConnectionTimeOut": 100,                               # Connection establishment timeout in seconds (optional, default: 100)
    "SslVerify": True,                                      # Verify TLS/SSL certificates (optional, default: true)
    "TrustEnv": True,                                       # Trust environment variables (optional, default: true)
    "AuthenticationSettings": {
        "BasicAuthentication": {
            "Username": ""                                  # Username for basic authentication
        }
    }
}

wrapper = create_wrapper_by_dict(configuration_dict, basic_auth_password="")
```

---

## ⚠️ Notes

* When `ssl_verify` is set to `False`, SSL/TLS verification is disabled (⚠️ not recommended in production).
* Default timeouts are intentionally high for development; adjust for production usage.
* The client and wrappers support both **parameter-based** and **configuration file-based** setup.
* For detailed configuration options, authentication methods, and examples, see the [Configuration Guide](configuration.md).
