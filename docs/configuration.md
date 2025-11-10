# AAS HTTP Client Configuration Guide

This guide explains how to configure and create an AAS (Asset Administration Shell) HTTP client to communicate with AAS servers.

## Table of Contents

- [Overview](#overview)
- [Example Configuration File](#example-configuration-file)
- [Configuration File Parameters](#configuration-file-parameters)
- [Client Creation Methods](#client-creation-methods)
- [Configuration Parameters](#configuration-parameters)
- [Authentication Methods](#authentication-methods)
- [Configuration Examples](#configuration-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Overview

The AAS HTTP Client provides a convenient way to interact with AAS servers through HTTP/REST APIs. The client supports multiple authentication methods, proxy configurations, and SSL verification options.

## Example Configuration File

Here's a complete example configuration file (`config.json`) that demonstrates all available options:

```json
{
    "BaseUrl": "https://aas-server.example.com",
    "TimeOut": 300,
    "ConnectionTimeOut": 120,
    "SslVerify": true,
    "TrustEnv": true,
    "HttpProxy": "http://proxy.company.com:8080",
    "HttpsProxy": "http://proxy.company.com:8080",
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

### Configuration Structure Overview

- **Root Level**: Contains server connection settings and timeouts
- **AuthenticationSettings**: Groups all authentication-related configurations
  - **BasicAuth**: HTTP Basic Auth settings (username only, password provided separately)
  - **OAuth**: OAuth2 settings for token-based authentication

### Configuration File Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| **Root Level Parameters** |
| `BaseUrl` | `string` | Yes | - | Base URL of the AAS server including protocol and port |
| `TimeOut` | `integer` | No | `200` | Maximum time in seconds to wait for API responses |
| `ConnectionTimeOut` | `integer` | No | `60` | Maximum time in seconds to wait when establishing connection |
| `SslVerify` | `boolean` | No | `true` | Whether to verify SSL/TLS certificates for HTTPS requests |
| `TrustEnv` | `boolean` | No | `true` | Whether to trust environment variables for proxy configuration |
| `HttpProxy` | `string` | No | `null` | HTTP proxy server URL for non-encrypted connections |
| `HttpsProxy` | `string` | No | `null` | HTTPS proxy server URL for encrypted connections |
| **Authentication Settings** |
| `AuthenticationSettings.BasicAuth.Username` | `string` | No | - | Username for HTTP Basic Authentication |
| `AuthenticationSettings.OAuth.ClientId` | `string` | No | - | OAuth2 client identifier |
| `AuthenticationSettings.OAuth.TokenUrl` | `string` | No | - | OAuth2 token endpoint URL |
| `AuthenticationSettings.OAuth.GrantType` | `string` | No | - | OAuth2 grant type (`client_credentials` or `password`) |

### Key Points

1. **Authentication compatibility**:
   - ✅ Only one authentication method should be configured at a time
   - If multiple methods are accidentally configured, priority order is: Bearer Token → OAuth2 → Basic Authentication
2. **Passwords and secrets** are provided separately via function parameters for security
3. **Bearer tokens** are provided via function parameters, not configuration files
4. **All settings are optional** except `BaseUrl`
5. **Environment variables** can override proxy settings when `TrustEnv` is `true`

### Usage with Configuration File

```python
from pathlib import Path
from aas_http_client.client import create_client_by_config

# Load configuration and provide sensitive data separately
config_file = Path("config.json")
client = create_client_by_config(
    config_file=config_file,
    basic_auth_password="your-password",           # For Basic Auth
    o_auth_client_secret="secret",                 # For OAuth2
    bearer_auth_token="your-bearer-token"          # For Bearer Auth (not in config file)
)
```

## Client Creation Methods

There are three ways to create an AAS HTTP client:

### 1. Create Client by URL

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

### 2. Create Client by Dictionary

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

### 3. Create Client by Configuration File

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

## Configuration Parameters

### Basic Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | `str` | Required | Base URL of the AAS server |
| `time_out` | `int` | `200` | Timeout for HTTP requests (seconds) |
| `connection_time_out` | `int` | `60` | Connection timeout (seconds) |
| `ssl_verify` | `bool` | `True` | Enable SSL certificate verification |
| `trust_env` | `bool` | `True` | Trust environment variables for proxy settings |

### Proxy Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `http_proxy` | `str` | `""` | HTTP proxy URL |
| `https_proxy` | `str` | `""` | HTTPS proxy URL |

### Authentication Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `basic_auth_username` | `str` | `""` | Username for basic authentication |
| `basic_auth_password` | `str` | `""` | Password for basic authentication |
| `o_auth_client_id` | `str` | `""` | Client ID for OAuth2 |
| `o_auth_client_secret` | `str` | `""` | Client secret for OAuth2 |
| `o_auth_token_url` | `str` | `""` | Token endpoint URL for OAuth2 |
| `bearer_auth_token` | `str` | `""` | Bearer token for authentication (function parameter only) |

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

## Configuration Examples

### Minimal Configuration

```json
{
    "BaseUrl": "http://localhost:8080"
}
```

### Basic Authentication Configuration

```json
{
    "BaseUrl": "https://aas-server.example.com",
    "TimeOut": 300,
    "SslVerify": true,
    "AuthenticationSettings": {
        "BasicAuth": {
            "Username": "admin"
        }
    }
}
```

### OAuth2 Configuration

```json
{
    "BaseUrl": "https://aas-server.example.com",
    "TimeOut": 300,
    "ConnectionTimeOut": 120,
    "SslVerify": true,
    "AuthenticationSettings": {
        "OAuth": {
            "ClientId": "my-client-id",
            "TokenUrl": "https://auth-server.example.com/oauth/token",
            "GrantType": "client_credentials"
        }
    }
}
```

### Proxy Configuration

```json
{
    "BaseUrl": "https://aas-server.example.com",
    "HttpProxy": "http://proxy.company.com:8080",
    "HttpsProxy": "http://proxy.company.com:8080",
    "TrustEnv": false,
    "AuthenticationSettings": {
        "BasicAuth": {
            "Username": "admin"
        }
    }
}
```

### Production Environment Configuration

```json
{
    "BaseUrl": "https://production-aas.company.com",
    "TimeOut": 600,
    "ConnectionTimeOut": 300,
    "SslVerify": true,
    "TrustEnv": true,
    "HttpsProxy": "http://corporate-proxy:8080",
    "AuthenticationSettings": {
        "OAuth": {
            "ClientId": "production-client",
            "TokenUrl": "https://auth.company.com/oauth2/token",
            "GrantType": "client_credentials"
        }
    }
}
```

### Bearer Token Authentication Example

Bearer tokens are provided as function parameters, not in configuration files:

```python
from pathlib import Path
from aas_http_client.client import create_client_by_config

# Minimal config file for bearer token auth
config = {
    "BaseUrl": "https://aas-server.example.com",
    "TimeOut": 300,
    "SslVerify": true
}

client = create_client_by_dict(
    configuration=config,
    bearer_auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)
```

## Error Handling

The client creation methods return `None` if the configuration is invalid or the connection fails:

```python
client = create_client_by_url(base_url="http://invalid-url")
if client is None:
    print("Failed to create client - check configuration and connectivity")
    exit(1)

# Client is ready to use
shells = client.get_all_asset_administration_shells()
```

Common error scenarios:
- **Invalid URL**: Malformed base URL
- **Connection timeout**: Server unreachable within timeout period
- **Authentication failure**: Invalid credentials or token
- **SSL verification failure**: Invalid certificates when `ssl_verify=True`
- **Proxy issues**: Incorrect proxy configuration

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

### Error Handling

1. **Always check** if client creation was successful
2. **Implement retry logic** for transient failures
3. **Log configuration issues** for debugging

```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def create_production_client():
    config_file = Path("config/production.json")

    client = create_client_by_config(
        config_file=config_file,
        basic_auth_password=os.getenv("AAS_PASSWORD")
    )

    if client is None:
        logger.error(f"Failed to create AAS client from {config_file}")
        raise RuntimeError("AAS client initialization failed")

    logger.info("AAS client created successfully")
    return client
```

### Performance

1. **Reuse client instances** instead of creating new ones for each request
2. **Set appropriate timeouts** to avoid hanging requests
3. **Use connection pooling** for high-throughput scenarios
4. **Monitor response times** and adjust timeouts accordingly

---

For more information about using the client methods, see the [API Reference](API_REFERENCE.md).
