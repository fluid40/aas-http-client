import json
import logging

import requests
from pydantic import BaseModel

from aas_http_client.classes.client.implementations.authentication import AuthMethod, get_token
from aas_http_client.classes.Configuration.config_classes import OAuth
from aas_http_client.utilities.encoder import decode_base_64
from aas_http_client.utilities.http_helper import (
    STATUS_CODE_200,
    STATUS_CODE_201,
    STATUS_CODE_202,
    STATUS_CODE_204,
    STATUS_CODE_404,
    log_response_errors,
)

logger = logging.getLogger(__name__)


class ShellRegistryImplementation(BaseModel):
    """Implementation of Asset Administration Shell Registry related API calls."""

    def __init__(self, session: requests.Session, base_url: str, time_out: int, auth_method: AuthMethod, o_auth_settings: OAuth, encoded_ids: bool):
        """Initializes the ShellRegistryImplementation with the given parameters."""
        self._session = session
        self._base_url = base_url
        self._time_out = time_out
        self._encoded_ids = encoded_ids
        self._auth_method = auth_method
        self._o_auth_settings = o_auth_settings

    # GET /shell-descriptors/{aasIdentifier}
    def get_all_asset_administration_shell_descriptors(self) -> dict | None:
        """Returns all Asset Administration Shell Descriptors.

        :return: Asset Administration Shells data or None if an error occurred
        """
        url = f"{self._base_url}/shell-descriptors"

        self._set_token()

        try:
            response = self._session.get(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def _set_token(self) -> str | None:
        """Set authentication token in session headers based on configured authentication method.

        :raises requests.exceptions.RequestException: If token retrieval fails
        """
        if self._auth_method != AuthMethod.o_auth:
            return None

        token = get_token(self._o_auth_settings).strip()

        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})
            return token

        return None
