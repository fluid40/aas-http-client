# 🚀 Getting Started

This guide will walk you through installing and using `aas-http-client` .

- [🚀 Getting Started](#-getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Creation Methods](#creation-methods)
    - [/Shell/ Endpoints](#shell-endpoints)
    - [/Submodel/ Endpoints](#submodel-endpoints)
    - [/shell-descriptors/ Endpoints](#shell-descriptors-endpoints)
    - [/submodel-descriptors/ Endpoints](#submodel-descriptors-endpoints)
    - [Experimental Endpoint Implementations](#experimental-endpoint-implementations)

---

## Installation

Prerequisites:

* Python 3.10 or newer
* Access to an AAS server endpoint

Install via pip:

```bash
pip install aas-http-client
```

For detailed configuration options, authentication methods and examples, see the [Configuration Guide](configuration.md).

---

## Usage

### Creation Methods

There are three ways to create an AAS HTTP client or wrapper.
Use either a client (dictionary-based API) or a wrapper (SDK object-based API), depending on your use case.
Creation methods can return `None` if the configuration is invalid or the connection fails.

For production usage, avoid hardcoding secrets in source code. Load credentials from environment variables or a secret manager.

#### Create by URL

Create a client or wrapper by providing parameters directly using `create_by_url` :

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

#### Create by Dictionary

Create a client or wrapper using a configuration dictionary with `create_by_dict` :

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

#### Create by Configuration File

Create a client or wrapper using a JSON configuration file with `create_by_config` :

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

### /Shell/ Endpoints

This section shows how to work with the most common Shell repository operations after client or wrapper creation.

Most important points:

* Shell endpoints are available via `client.shells` (dictionary responses) or directly on `wrapper` (SDK object responses).
* List endpoints are paginated. Use `limit` and `cursor` when iterating through larger result sets.
* Always handle `None` results to detect connectivity, authorization, or server-side issues.

#### Example: List Asset Administration Shells (client)

```python
# Assumes `client` was created successfully in one of the sections above.
result = client.shells.get_all_asset_administration_shells(limit=10)

if result is None:
    raise RuntimeError("Failed to fetch shells")

shells = result.get("result", [])
print(f"Received {len(shells)} shell(s)")
```

#### Example: Fetch one shell by ID (wrapper)

```python
# Assumes `wrapper` was created successfully in one of the sections above.
aas_id = "urn:example:aas:001"
aas = wrapper.get_asset_administration_shell_by_id(aas_id)

if aas is None:
    print("Shell not found or request failed")
else:
    print("Found shell with id:", aas.id)
```

For the full list of available methods and signatures, see the API reference:

* [AAS HTTP Client API Reference](https://fluid40.github.io/aas-http-client/)

### /Submodel/ Endpoints

This section shows how to work with common Submodel repository operations after client or wrapper creation.

Most important points:

* Submodel endpoints are available via `client.submodels` (dictionary responses) or directly on `wrapper` (SDK object responses).
* List endpoints are paginated. Use `limit` and `cursor` when retrieving larger result sets.
* `level` and `extent` can be used to control response depth and blob behavior.
* Always handle `None` results to detect connectivity, authorization, or server-side issues.

#### Example: List Submodels (client)

```python
# Assumes `client` was created successfully in one of the sections above.
result = client.submodels.get_all_submodels(limit=10)

if result is None:
    raise RuntimeError("Failed to fetch submodels")

submodels = result.get("result", [])
print(f"Received {len(submodels)} submodel(s)")
```

#### Example: Fetch one submodel by ID (wrapper)

```python
# Assumes `wrapper` was created successfully in one of the sections above.
submodel_id = "urn:example:submodel:001"
submodel = wrapper.get_submodel_by_id(submodel_id)

if submodel is None:
    print("Submodel not found or request failed")
else:
    print("Found submodel with id:", submodel.id)
```

For the full list of available methods and signatures, see the API reference:

* [AAS HTTP Client API Reference](https://fluid40.github.io/aas-http-client/)

### /shell-descriptors/ Endpoints

This section shows how to work with Asset Administration Shell registry endpoints.

Most important points:

* Shell descriptor endpoints are available via `client.shell_registry`.
* Registry endpoints currently are not exposed on `wrapper`.
* List endpoints are paginated. Use `limit` and `cursor` when iterating through larger result sets.
* Depending on server settings, IDs may need Base64 URL-safe encoding. Keep `encoded_ids` consistent with your server setup.

#### Example: List shell descriptors

```python
# Assumes `client` was created successfully in one of the sections above.
result = client.shell_registry.get_all_asset_administration_shell_descriptors(limit=10)

if result is None:
    raise RuntimeError("Failed to fetch shell descriptors")

descriptors = result.get("result", [])
print(f"Received {len(descriptors)} shell descriptor(s)")
```

#### Example: Fetch one shell descriptor by ID

```python
# Assumes `client` was created successfully in one of the sections above.
aas_id = "urn:example:aas:001"
descriptor = client.shell_registry.get_asset_administration_shell_descriptor_by_id(aas_id)

if descriptor is None:
    print("Shell descriptor not found or request failed")
else:
    print("Found descriptor with id:", descriptor.get("id"))
```

#### Example: Register a shell descriptor

```python
# Assumes `client` was created successfully in one of the sections above.
payload = {
    "id": "urn:example:aas:001",
    "idShort": "aas_example_001",
    "assetKind": "Instance",
    "endpoints": [
        {
            "interface": "AAS-3.0",
            "protocolInformation": {
                "href": "http://localhost:8080/shells/urn:example:aas:001",
                "endpointProtocol": "http",
                "endpointProtocolVersion": ["1.1"],
                "subprotocol": "",
                "subprotocolBody": "",
                "subprotocolBodyEncoding": "plain",
                "securityAttributes": []
            }
        }
    ],
    "submodelDescriptors": []
}

created = client.shell_registry.post_asset_administration_shell_descriptor(payload)

if created is None:
    raise RuntimeError("Failed to create shell descriptor")

print("Registered descriptor:", created.get("id"))
```

For the full list of available methods and signatures, see the API reference:

* [AAS HTTP Client API Reference](https://fluid40.github.io/aas-http-client/)

### /submodel-descriptors/ Endpoints

This section shows how to work with Submodel registry endpoints.

Most important points:

* Submodel descriptor endpoints are available via `client.submodel_registry`.
* Registry endpoints currently are not exposed on `wrapper`.
* List endpoints are paginated. Use `limit` and `cursor` when iterating through larger result sets.
* Depending on server settings, IDs may need Base64 URL-safe encoding. Keep `encoded_ids` consistent with your server setup.

#### Example: List submodel descriptors

```python
# Assumes `client` was created successfully in one of the sections above.
result = client.submodel_registry.get_all_submodel_descriptors(limit=10)

if result is None:
    raise RuntimeError("Failed to fetch submodel descriptors")

descriptors = result.get("result", [])
print(f"Received {len(descriptors)} submodel descriptor(s)")
```

#### Example: Fetch one submodel descriptor by ID

```python
# Assumes `client` was created successfully in one of the sections above.
submodel_id = "urn:example:submodel:001"
descriptor = client.submodel_registry.get_submodel_descriptor_by_id(submodel_id)

if descriptor is None:
    print("Submodel descriptor not found or request failed")
else:
    print("Found descriptor with id:", descriptor.get("id"))
```

#### Example: Register a submodel descriptor

```python
# Assumes `client` was created successfully in one of the sections above.
payload = {
    "id": "urn:example:submodel:001",
    "idShort": "sm_example_001",
    "endpoints": [
        {
            "interface": "SUBMODEL-3.0",
            "protocolInformation": {
                "href": "http://localhost:8080/submodels/urn:example:submodel:001",
                "endpointProtocol": "http",
                "endpointProtocolVersion": ["1.1"],
                "subprotocol": "",
                "subprotocolBody": "",
                "subprotocolBodyEncoding": "plain",
                "securityAttributes": []
            }
        }
    ],
    "semanticId": {
        "type": "ExternalReference",
        "keys": [
            {
                "type": "GlobalReference",
                "value": "urn:example:semantic:submodel:001"
            }
        ]
    }
}

created = client.submodel_registry.post_submodel_descriptor(payload)

if created is None:
    raise RuntimeError("Failed to create submodel descriptor")

print("Registered descriptor:", created.get("id"))
```

For the full list of available methods and signatures, see the API reference:

* [AAS HTTP Client API Reference](https://fluid40.github.io/aas-http-client/)

### Experimental Endpoint Implementations

This section shows the experimental attachment endpoints for file content on Submodel File elements.

Most important points:

* Experimental endpoints are available via `client.experimental` and via wrapper methods prefixed with `experimental_`.
* Experimental endpoints may not be supported by every server implementation.

#### Example: Download file content (wrapper)

```python
from pathlib import Path

# Assumes `wrapper` was created successfully in one of the sections above.
attachment = wrapper.experimental_get_file_by_path_submodel_repo(
    submodel_identifier="urn:example:submodel:001",
    id_short_path="Documents.UserManual"
)

if attachment is None:
    print("No attachment found or request failed")
else:
    output = Path("downloaded_" + attachment.filename)
    output.write_bytes(attachment.content)
    print("Downloaded attachment to:", output)
    print("Detected content type:", attachment.content_type)
```

#### Example: Upload or replace file content (client)

```python
from pathlib import Path

# Assumes `client` was created successfully in one of the sections above.
submodel_id = "urn:example:submodel:001"
id_short_path = "Documents.UserManual"
file_path = Path("manual.pdf")

created = client.experimental.post_file_by_path_submodel_repo(
    submodel_identifier=submodel_id,
    id_short_path=id_short_path,
    file=file_path
)

if not created:
    raise RuntimeError("Failed to upload attachment with POST")

updated = client.experimental.put_file_by_path_submodel_repo(
    submodel_identifier=submodel_id,
    id_short_path=id_short_path,
    file=file_path
)

if not updated:
    raise RuntimeError("Failed to replace attachment with PUT")

print("Attachment upload/update successful")
```
