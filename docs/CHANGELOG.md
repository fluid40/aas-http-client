# 📝 Changelog

## [1.1.2] - 2026-06-11

* 🚀Improvement: Improved logging in client creation.

## [1.1.1] - 2026-06-09

* 🚀Improvement: Expose authentication method in client.

## [1.1.0] - 2026-05-28

* 🚀Improvement: Update external packages to newest versions.

## [1.0.14] - 2026-05-20

* ✨Feat: Add stream upload method for thumbnail to shell.

## [1.0.12] - 2026-05-15

* 🚀Improvement: Add SSL verification option to token retrieval methods

## [1.0.11] - 2026-05-08

* 🚀Improvement: Enhance submodel management with validation in add/remove functions and add return success status

## [1.0.9] - 2026-04-25

* 🚀Improvement: Enable model builder to get empty display names and empty descriptions.

## [1.0.8] - 2026-04-24

* ✨Feat: Harmonize create function names for consistency across client and wrapper modules: `create_by_url`,  `create_by_dict` and `create_by_config`.

## [1.0.4] - 2026-03-26

* 📝Doc: Add [GitHub Pages](https://fluid40.github.io/aas-http-client) for documentation.

## [1.0.0] - 2026-02-17

* ✨Feat: Implement all endpoints from BaSxy Java SDK 'aas-registry', 'submodel-registry' and 'aas-environment'.
* 🚀Improvement: Update all packages to latest versions.

## [0.9.7] - 2026-02-17

* 🚀Improvement: General code improvements.

## [0.9.6] - 2026-02-17

* 🚀Improvement: Use urlsafe base64 encoding/decoding.

## [0.9.5] - 2026-02-03

* 🚀Improvement: Reorder authentication method handling for improved logic flow.

## [0.9.4] - 2026-01-20

* ✨Feat: Update package dependencies.

## [0.9.2] - 2026-01-16

* ✨Feat: Add generic endpoint implementations (GET, PATCH, PUT, POST and DELETE) for handling individual endpoints (e.g. from descriptors) to the client.

## [0.9.1] - 2026-01-08

* 🐛Fix: Rename the client sub-modules ('client.shell' to 'client.shell--s--' and 'client.submodels' to 'client.submodel--s--') so that they conform to the naming convention for endpoints.

## [0.9.0] - 2026-01-08

* ✨Feat: Add endpoints for Submodel reference handling to wrapper and client ('client.shell')

## [0.8.5] - 2026-01-08

* ✨Feat: Add endpoints for AAS thumbnail handling to wrapper and client ('client.shell')

## [0.8.2] - 2026-01-07

* ✨Feat: Improve oAuth authentication handling and add oAuth Token caching.
* 🐛Fix: Fix handling of decoded / encoded IDs in registry implementations.

## [0.8.0] - 2026-01-06

* ✨Feat: Add missing endpoints for Submodel-Registry server communication ('client.submodel_registry'). Not available in wrapper.

## [0.7.5] - 2026-01-06

* ✨Feat: Add missing endpoints for AAS-Registry server communication ('client.shell_registry'). Not available in wrapper.

## [0.7.2] - 2026-01-05

* 📝Doc: Update documentation

## [0.7.1] - 2025-12-18

* 🐛Fix: Replace package 'python-magic' with package 'puremagic'.

## [0.7.0] - 2025-12-18

* ✨Feat: Add first endpoints for SM-Registry server communication ('client.submodel_registry'). Not available in wrapper.

## [0.6.2] - 2025-12-17

* ✨Feat: Add endpoints for './attachment' in submodel repository ('client.experimental', 'wrapper.experimental_...'). Experimental feature - may not be supported by all servers.

## [0.6.1] - 2025-12-10

* ✨Feat: Update 'basyx-python-sdk' package to version 2.0.0

## [0.6.0] - 2025-12-09

* ✨Feat: Add first endpoints for AAS-Registry server communication ('client.shell_registry'). Not available in wrapper.

## [0.5.6] - 2025-12-01

* 🐛Fix: Bugfix in parameter name 'EncodeIds'

## [0.5.5] - 2025-12-01

* ♻️Refactor: Move the specific endpoint implementations to sub-modules ('client.shell' and 'client.submodel')

## [0.5.4] - 2025-12-01

* ✨Feat: Add an 'encode' parameter to enable or disable the requirement for all IDs used in API requests to be Base64-encoded.

## [0.2.6] - 2025-08-18

* 🧹Chore: Automated release notes added to GitHub releases.

## [0.2.5] - 2025-08-18

* ♻️Refactor: The names of the functions have been adapted to correspond to the operation names in the specification.

* ✨Feat        - Feature
* 🐛Fix         - Bugfix
* 📝Doc         - Documentation
* ♻️Refactor    - Refactor
* 🧹Chore       - Chore
* 🚀Improvement - Improvement
