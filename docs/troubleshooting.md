# 👨‍⚕️ Troubleshooting

This chapter helps you quickly diagnose and resolve the most common issues when working with the AAS HTTP Client. Start with the scenario that matches your problem, verify the listed checks step by step, and then retry your request. Most problems are caused by configuration, connectivity, authentication, or endpoint mismatches.

- [👨‍⚕️ Troubleshooting](#️-troubleshooting)
  - [Quick checklist](#quick-checklist)
  - [Client creation](#client-creation)
  - [HTTP 401 or 403 (authentication or authorization)](#http-401-or-403-authentication-or-authorization)
  - [HTTP 404 (resource not found)](#http-404-resource-not-found)
  - [Empty list responses](#empty-list-responses)
  - [Timeouts or connection errors](#timeouts-or-connection-errors)
  - [SSL and proxy issues](#ssl-and-proxy-issues)
  - [Pagination issues](#pagination-issues)
  - [Wrapper vs client endpoint availability](#wrapper-vs-client-endpoint-availability)
  - [Experimental endpoint issues](#experimental-endpoint-issues)
  - [Generic endpoint helper issues](#generic-endpoint-helper-issues)
  - [Debug logging](#debug-logging)

## Quick checklist

Before deep debugging, verify these basics:

* The base URL is correct and reachable (protocol, host, port, and path).
* Credentials/tokens are valid and belong to a user with required permissions.
* `encoded_ids` matches your server/API expectation.
* You are calling the correct endpoint group:
  + `client.shells`
  + `client.submodels`
  + `client.shell_registry`
  + `client.submodel_registry`
  + `client.experimental`
* Timeouts are high enough for your server/network.
* SSL/proxy settings match your environment.

## Client creation

The client creation methods return `None` if the configuration is invalid or the connection fails:

```python
from aas_http_client.classes.client import aas_client

client = aas_client.create_by_url(base_url="http://invalid-url")
if client is None:
    print("Failed to create client - check configuration and connectivity")
    exit(1)

# Client is ready to use
shells = client.shells.get_all_asset_administration_shells()
```

Common error scenarios:

* **Invalid URL**: Malformed base URL
* **Connection timeout**: Server unreachable within timeout period
* **Authentication failure**: Invalid credentials or token
* **SSL verification failure**: Invalid certificates when `ssl_verify=True`
* **Proxy issues**: Incorrect proxy configuration

Recommended checks:

* Test connectivity immediately after creation:

```python
if client.get_root() is None:
    print("Root endpoint check failed")
```

* If this fails, verify network reachability and URL correctness first.

## HTTP 401 or 403 (authentication or authorization)

Symptoms:

* Read/write operations return `None` or `False`.
* Server logs show unauthorized or forbidden errors.

Typical causes:

* Wrong username/password or bearer token.
* OAuth client configuration invalid (client id, secret, token URL, grant).
* User lacks permission for the targeted endpoint.

What to check:

* Basic auth:
  + Username and password are correct.
* Bearer auth:
  + Token is valid and not expired.
* OAuth:
  + Token endpoint reachable.
  + Client credentials and grant configuration are correct.
* Endpoint access policy on the server side.

## HTTP 404 (resource not found)

Symptoms:

* Methods like `get_*_by_id(...)` return `None`.
* Delete/update operations return `False`.

Typical causes:

* Wrong ID.
* Wrong endpoint group (for example shell vs shell descriptor registry).
* `encoded_ids` mismatch.

What to check:

* Verify the resource exists by listing first.
* Confirm you use the correct API group:
  + Repository resources: `client.shells`,  `client.submodels`
  + Registry descriptors: `client.shell_registry`,  `client.submodel_registry`
* Re-check ID encoding mode and input value format.

## Empty list responses

Symptoms:

* Result is not `None`, but `result` is empty.

Typical causes:

* Repository/registry is actually empty.
* Pagination cursor already points past available items.
* Filters (if used) are too restrictive.

What to check:

* Start with small clean call:

```python
result = client.submodels.get_all_submodels(limit=10)
print(result.get("result", []) if result else None)
```

* Retry without filters and without a cursor.

## Timeouts or connection errors

Symptoms:

* Client creation returns `None`.
* Requests intermittently return `None`.

Typical causes:

* Service not reachable or unstable.
* Timeout values too low.
* Container/network routing issue.

What to check:

* Increase `time_out` and `connection_time_out`.
* Verify host/port reachability from the runtime environment.
* Retry with reduced load and check server resource usage.

## SSL and proxy issues

Symptoms:

* SSL handshake/certificate failures.
* Connection failures only in corporate/proxied environments.

What to check:

* SSL:
  + Use valid certificates.
  + For local debugging only, temporarily set `ssl_verify=False`.
* Proxy:
  + Configure `http_proxy` and `https_proxy` correctly.
  + If environment proxy variables interfere, control `trust_env` explicitly.

## Pagination issues

Symptoms:

* You only see first page of results.
* Iteration misses entries.

What to check:

* Use `limit` and then continue with returned cursor.
* Stop when no further cursor or no new items are returned.

Basic pattern:

```python
cursor = ""
all_items = []

while True:
    page = client.shells.get_all_asset_administration_shells(limit=100, cursor=cursor)
    if page is None:
        break

    items = page.get("result", [])
    all_items.extend(items)

    paging = page.get("paging_metadata", {})
    cursor = paging.get("cursor", "")
    if not cursor:
        break
```

## Wrapper vs client endpoint availability

Symptoms:

* You cannot find a method on `wrapper` that exists on `client`.

Key point:

* Registry endpoints are currently not exposed on `wrapper`.
* Use `client.shell_registry` and `client.submodel_registry` for descriptor APIs.

## Experimental endpoint issues

Symptoms:

* Experimental attachment methods return `None` or `False`.

Typical causes:

* Server does not support the experimental attachment endpoints.
* Target submodel element is not a `File` element.
* Attachment file path is invalid.

What to check:

* Confirm server capability for `/attachment` endpoints.
* Validate `id_short_path` points to an existing `File` element.
* Ensure local file exists before upload calls.

## Generic endpoint helper issues

Symptoms:

* `get_endpoint(...)` returns `None`.
* Write helpers return error payloads instead of `None`.

Key behavior:

* `get_endpoint` returns parsed JSON only for HTTP 200.
* `put_endpoint`,   `post_endpoint`,   `patch_endpoint`,  `delete_endpoint` return `None` on success and parsed JSON on non-success.

What to check:

* Ensure URL points to the expected endpoint.
* Confirm server returns JSON response for the call path.

## Debug logging

If an issue is unclear, enable debug logs and inspect request URLs and status handling:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

Then retry the failing operation and inspect:

* Called endpoint URL
* HTTP status behavior
* Authentication flow messages
* ID and path values used in requests
