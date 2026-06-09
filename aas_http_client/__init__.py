"""AAS HTTP Client Package."""

import importlib.metadata
from datetime import datetime, timezone

from aas_http_client.classes.client import aas_client
from aas_http_client.classes.client.aas_client import AasHttpClient
from aas_http_client.classes.client.implementations.authentication import AuthMethod
from aas_http_client.classes.Configuration.config_classes import BasicAuth, BearerAuth, OAuth
from aas_http_client.classes.wrapper import sdk_wrapper
from aas_http_client.classes.wrapper.sdk_wrapper import SdkWrapper
from aas_http_client.utilities import encoder, model_builder, sdk_tools
from aas_http_client.utilities.version_check import check_for_update

__copyright__ = f"Copyright (C) {datetime.now(tz=timezone.utc).year} :em engineering methods AG. All rights reserved."
__author__ = "Daniel Klein"

try:
    __license__ = "MIT"
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

__project__ = "aas-http-client"
__package__ = "aas-http-client"

check_for_update()

__all__ = [
    "AasHttpClient",
    "AuthMethod",
    "BasicAuth",
    "BearerAuth",
    "OAuth",
    "SdkWrapper",
    "aas_client",
    "encoder",
    "model_builder",
    "sdk_tools",
    "sdk_wrapper",
]
