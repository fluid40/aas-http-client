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

You can configure the HTTP server connection in two ways:

* **Using a configuration file** (recommended)
* **Passing parameters directly** to the client creation function

---

#### 📄 Configuration File

Provide a YAML configuration file with the following format:

```yaml
{
    base_url: "http://myaasserver:5043/"   # Base URL of the AAS server (required)
    username: ""                           # Username for authentication (optional, default: "")
    https_proxy: null                      # HTTPS proxy (optional, default: null)
    http_proxy: null                       # HTTP proxy (optional, default: null)
    time_out: 200                          # API call timeout in seconds (optional, default: 200)
    connection_time_out: 100               # Connection establishment timeout in seconds (optional, default: 100)
    ssl_verify: true                       # Verify TLS/SSL certificates (optional, default: true)
}
```

---

### Client

The client communicates directly with the server and uses generic dictionaries (dict) for input and output. The serialization and deserialization of the request and response body must be performed on the runtime side.

#### 📌 Create Client from Configuration File

See [Configuration File](#-configuration-file)

```python
from pathlib import Path
from aas_http_client import create_client_by_config         # import function to create a client by configuration file

config_file = Path("./server_config.yaml")                  # get the config file 
client = create_client_by_config(config_file, password="")  # create the client (in this case without password authentication)
```

#### 📌 Create Client via Parameters

```python
from aas_http_client import create_client_by_url            # import function to create a client by parameters

client = create_client_by_url(
    base_url="http://myaasserver:5043/",                    # required
    username="",                                            # optional
    password="",                                            # optional
    http_proxy="",                                          # optional
    https_proxy="",                                         # optional
    time_out=200,                                           # optional, default: 200
    connection_time_out=100,                                # optional, default: 100
    ssl_verify=True                                         # optional, default: True
)
```

---

### Wrapper

The client communicates directly with the server and uses generic dictionaries (dict) for input and output. The serialization and deserialization of the request and response body must be performed on the runtime side.

#### 📌 Create Client from Configuration File

See [Configuration File](#-configuration-file)

```python
from pathlib import Path
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_config    # import function to create a wrapper by configuration file (in this case a BaSyx Python SDK wrapper)
import basyx.aas.model                                                      # import BaSyx Python SDK to use the data model


config_file = Path("./server_config.yaml")                                  # get the config file  
client = create_wrapper_by_config(config_file, password="")                 # create the wrapper (in this case without password authentication)
```

#### 📌 Create Client via Parameters

```python
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_url       # import function to create a wrapper by parameters (in this case a BaSyx Python SDK wrapper)
import basyx.aas.model                                                      # import BaSyx Python SDK to use the data model

wrapper = create_wrapper_by_url(
    base_url="http://myaasserver:5043/",                                    # required
    username="",                                                            # optional
    password="",                                                            # optional
    http_proxy="",                                                          # optional
    https_proxy="",                                                         # optional
    time_out=200,                                                           # optional, default: 200
    connection_time_out=100,                                                # optional, default: 100
    ssl_verify=True                                                         # optional, default: True
)
```

---

## ⚠️ Notes

* When `ssl_verify` is set to `False`, SSL/TLS verification is disabled (⚠️ not recommended in production).
* Default timeouts are intentionally high for development; adjust for production usage.
* The client and wrappers supports both **parameter-based** and **YAML-based** configuration.
