# 🛠️ Configuration Guide

This guide explains how to configure and create an AAS (Asset Administration Shell) HTTP client to communicate with AAS servers.

**Table of Contents:**

* [🛠️ Configuration Guide](#️-configuration-guide)
  + [Configuration Parameters](#configuration-parameters)
  + [Creation Methods](#creation-methods)
  + [Authentication Methods](#authentication-methods)
  + [Error Handling](#error-handling)
  + [Best Practices](#best-practices)

The AAS HTTP Client allows you to interact with Asset Administration Shell (AAS) servers via HTTP/REST APIs. The client connects to an AAS server using a configurable base URL, with adjustable timeout settings, SSL/TLS certificate verification, and optional HTTP/HTTPS proxy support.
There are three ways to create a client:

* by passing parameters directly ( `create_client_by_url` )
* by providing a configuration dictionary ( `create_client_by_dict` )
* by loading a JSON configuration file ( `create_client_by_config` )

Three authentication methods are supported:

* Basic Auth (username + password)
* Bearer Token
* OAuth2 ( `client_credentials` or `password` grant)

Sensitive values like passwords, client secrets, and bearer tokens are always passed as function parameters — never stored in configuration files.

## Configuration Parameters

* **Root Level**: Contains server connection settings and timeouts
* **AuthenticationSettings**: Groups all authentication-related configurations
  + **BasicAuth**: HTTP Basic Auth settings (username only, password provided separately)
  + **OAuth**: OAuth2 settings for token-based authentication

### Parameters Overview

**Root Level Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `BaseUrl` | `string` | ✅ | - | Base URL of the AAS server including protocol and port |
| `TimeOut` | `integer` | ❌ | `200` | Maximum time in seconds to wait for API responses |
| `ConnectionTimeOut` | `integer` | ❌ | `60` | Maximum time in seconds to wait when establishing connection |
| `SslVerify` | `boolean` | ❌ | `true` | Whether to verify SSL/TLS certificates for HTTPS requests |
| `TrustEnv` | `boolean` | ❌ | `true` | Whether to trust environment variables for proxy configuration |
| `HttpProxy` | `string` | ❌ | `null` | HTTP proxy server URL for non-encrypted connections |
| `HttpsProxy` | `string` | ❌ | `null` | HTTPS proxy server URL for encrypted connections |
| `EncodedIds` | `boolean` | ❌ | `true` | If enabled, all IDs used in API requests have to be base64-encoded |

**Authentication Settings:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `AuthenticationSettings.BasicAuth.Username` | `string` | ❌ | - | Username for HTTP Basic Authentication |
| `AuthenticationSettings.OAuth.ClientId` | `string` | ❌ | - | OAuth2 client identifier |
| `AuthenticationSettings.OAuth.TokenUrl` | `string` | ❌ | - | OAuth2 token endpoint URL |
| `AuthenticationSettings.OAuth.GrantType` | `string` | ❌ | - | OAuth2 grant type ( `client_credentials` or `password` ) |

### Key Points

1. **Authentication compatibility**:
   - ✅ Only one authentication method should be configured at a time
   - If multiple methods are accidentally configured, priority order is: Bearer Token → OAuth2 → Basic Authentication
2. **Passwords and secrets** are provided separately via function parameters for security
3. **Bearer tokens** are provided via function parameters, not configuration files
4. **All settings are optional** except `BaseUrl`
5. **Environment variables** can override proxy settings when `TrustEnv` is `true`

## Creation Methods

There are three ways to create an AAS HTTP client or wrapper. Wrapper creation follows the same pattern as client creation.

### 1. Create by URL

Create a client by providing parameters directly:

```python
from aas_http_client.client import create_client_by_url

client = create_client_by_url(
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
from aas_http_client.client import create_client_by_dict

config = {
    "BaseUrl": "http://localhost:8080",
    "TimeOut": 300,
    "AuthenticationSettings": {
        "BasicAuth": {
            "Username": "admin"
        }
    }
}

client = create_client_by_dict(
    configuration=config,
    basic_auth_password="password123"
)
```

### 3. Create by Configuration File

Create a client using a JSON configuration file:

```python
from pathlib import Path
from aas_http_client.client import create_client_by_config

config_file = Path("config.json")
client = create_client_by_config(
    config_file=config_file,
    basic_auth_password="password123"
)
```

### Example Configuration File

Here's a complete example configuration file ( `config.json` ) that demonstrates all available options:

```json
{
    "BaseUrl": "https://aas-server.example.com",
    "TimeOut": 300,
    "ConnectionTimeOut": 120,
    "SslVerify": true,
    "TrustEnv": true,
    "HttpProxy": "http://proxy.company.com:8080",
    "HttpsProxy": "http://proxy.company.com:8080",
    "EncodedIds": true,
    "AuthenticationSettings": {
        "BasicAuth": {
            "Username": "admin"
        },
        "OAuth": {
            "ClientId": "my-client-id",
            "TokenUrl": "https://auth-server.example.com/oauth/token",
            "GrantType": "client_credentials"
        }
    }
}
```

## Authentication Methods

### 1. Basic Authentication

Use username and password for HTTP Basic Authentication:

```python
client = create_client_by_url(
    base_url="http://localhost:8080",
    basic_auth_username="admin",
    basic_auth_password="password123"
)
```

### 2. Bearer Token Authentication

Use a pre-obtained bearer token (provided as function parameter, not in config file):

```python
client = create_client_by_url(
    base_url="http://localhost:8080",
    bearer_auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)
```

### 3. OAuth2 Client Credentials

Use OAuth2 client credentials flow:

```python
client = create_client_by_url(
    base_url="http://localhost:8080",
    o_auth_client_id="my-client-id",
    o_auth_client_secret="my-client-secret",
    o_auth_token_url="http://auth-server/oauth/token"
)
```

### 4. OAuth2 Password Grant

Use OAuth2 password grant flow:

```python
client = create_client_by_url(
    base_url="http://localhost:8080",
    o_auth_client_id="username",
    o_auth_client_secret="password",
    o_auth_token_url="http://auth-server/oauth/token"
)
```

## Best Practices

### Security

1. **Never hardcode credentials** in your source code
2. **Use environment variables** for sensitive information
3. **Enable SSL verification** in production environments
4. **Use OAuth2** instead of basic authentication when possible
5. **Keep bearer tokens out of configuration files** - pass them as function parameters

```python
import os

client = create_client_by_url(
    base_url=os.getenv("AAS_SERVER_URL"),
    basic_auth_username=os.getenv("AAS_USERNAME"),
    basic_auth_password=os.getenv("AAS_PASSWORD"),
    ssl_verify=True
)
```

### Configuration Management

1. **Use configuration files** for different environments
2. **Validate configuration** before deployment
3. **Set appropriate timeouts** based on network conditions
4. **Monitor connection health** in production

```python
# config/development.json
{
    "BaseUrl": "http://localhost:8080",
    "TimeOut": 30,
    "SslVerify": false
}

# config/production.json
{
    "BaseUrl": "https://aas-prod.company.com",
    "TimeOut": 300,
    "SslVerify": true,
    "HttpsProxy": "http://proxy.company.com:8080"
}
```

1. **Always check** if client creation was successful
2. **Implement retry logic** for transient failures
3. **Log configuration issues** for debugging

### Performance

1. **Reuse client instances** instead of creating new ones for each request
2. **Set appropriate timeouts** to avoid hanging requests
3. **Use connection pooling** for high-throughput scenarios
4. **Monitor response times** and adjust timeouts accordingly
