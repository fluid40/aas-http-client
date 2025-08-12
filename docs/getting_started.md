# 🚀 Getting Started

In this guide we'll walk you through using `aas-http-client`.

# Installation

Use command:
```shell
pip install aas-http-client
```
to install the package.

# Client Usage

This chapter handles the usage of the AAS HTTP Client

## Server Configuration
To configure the HTTP server connections there are two possible ways.
- by using a configuration file
- by using parameters 

### Configuration File
As configuration file a YAML file is provided with the following format
```yaml
{
    "base_url": "http://myaasserver:5043/",   # The base url of the aas server. E.g. 'http://www.myaasserver.de/' or 'http://myaasserver:5043/api/v3.0'
    "username": "",                           # username for authentication (optional)
    "https_proxy": null,                      # HTTPS settings for proxy (optional)
    "http_proxy": null,                       # HTTP settings for proxy (optional)
    "time_out": 10,                           # Timeout for single API calls in seconds (optional, default is '200')
    "connection_time_out": 10,                # Timeout when establishing the connection from the client to the server (optional, default is '100')
    "ssl_verify": True                        # Verification of TLS/SSL certificates when establishing an connection (optional, default is 'True')
}
```
## Create client

In the python project import the `aas-http-client` classes and methods:

```python
from aas_http_client import AasHttpClient, create_client_by_config, create_client_by_url
```
Then create a client by using a config file (e.g. `server_config.yaml`, see [Configuration File](#Configuration-File)) via the `create_client_by_config` function.  
If a password for authentication is needed, provide the password as parameter.
```python
config_file = Path("./server_config.yaml")
client = create_client_by_config(config_file, password="")
```

or by configuration with parameters via the `create_client_by_url` function.  
Only `base_url` is required, all other parameters are optional (see [Configuration File](#Configuration-File)).
```python
client = create_client_by_config(base_url="http://myaasserver:5043/",
    username="",
    password="",
    http_proxy="",
    https_proxy="",
    time_out=200,
    connection_time_out=60,
    ssl_verify= True)
```
