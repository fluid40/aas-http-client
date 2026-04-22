# 👨‍⚕️ Troubleshooting
- [👨‍⚕️ Troubleshooting](#️-troubleshooting)
  - [Client creation](#client-creation)

## Client creation

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

* **Invalid URL**: Malformed base URL
* **Connection timeout**: Server unreachable within timeout period
* **Authentication failure**: Invalid credentials or token
* **SSL verification failure**: Invalid certificates when `ssl_verify=True`
* **Proxy issues**: Incorrect proxy configuration
