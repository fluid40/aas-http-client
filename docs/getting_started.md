# 🚀 Getting Started

This guide will walk you through installing and using `aas-http-client`.

---

## 📦 Installation

Install via pip:

```bash
pip install aas-http-client
```

---

## 💻 Usage

### 1️⃣ Server Configuration

For detailed configuration options and examples, see the [Configuration Guide](configuration.md).

---

### Client

The client communicates directly with the server and uses generic dictionaries (dict) for input and output. The serialization and deserialization of the request and response body must be performed on the runtime side.

#### 📌 Create Client from Configuration File

Create a client from a given configuration file.

```python
from pathlib import Path
from aas_http_client import create_client_by_config         # import function to create a client by configuration file

config_file = Path("./server_config.json")                  # get the config file
client = create_client_by_config(config_file, basic_auth_password="")  # create the client (in this case without password authentication)
```

#### 📌 Create Client via Parameters

Create a client from given parameters.

```python
from aas_http_client import create_client_by_url            # import function to create a client by parameters

client = create_client_by_url(
    base_url="http://myaasserver:5043/",                    # Base URL of the AAS server (required)
    basic_auth_username="",                                 # Username for authentication (optional, default: "")
    basic_auth_password="",                                 # Password for authentication (optional, default: "")
    http_proxy="",                                          # HTTP proxy (optional, default: "")
    https_proxy="",                                         # HTTPS proxy (optional, default: "")
    time_out=200,                                           # API call timeout in seconds (optional, default: 200)
    connection_time_out=100,                                # Connection establishment timeout in seconds (optional, default: 100)
    ssl_verify=True,                                        # Verify TLS/SSL certificates (optional, default: true)
    trust_env=True                                          # Trust environment variables (optional, default: true)
)
```

#### 📌 Create Client via dictionary

Create a client from given JSON dictionary.

```python
from aas_http_client import create_client_by_dict            # import function to create a client by dictionary

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

client = create_client_by_dict(configuration_dict, basic_auth_password="")
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
