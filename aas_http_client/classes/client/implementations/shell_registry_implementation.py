"""Shell Registry Implementation Module."""

import json
import logging

import requests
from pydantic import BaseModel

from aas_http_client.classes.client.implementations.authentication import AuthMethod, get_token
from aas_http_client.classes.Configuration.config_classes import OAuth
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
    # PUT /shell-descriptors/{aasIdentifier}
    # DELETE /shell-descriptors/{aasIdentifier}
    # GET /shell-descriptors/{aasIdentifier}/submodel-descriptors/{submodelIdentifier}
    # PUT /shell-descriptors/{aasIdentifier}/submodel-descriptors/{submodelIdentifier}
    # DELETE /shell-descriptors/{aasIdentifier}/submodel-descriptors/{submodelIdentifier

    # GET /shell-descriptors
    def get_all_asset_administration_shell_descriptors(
        self, limit: int = 100, cursor: str = "", asset_kind: str = "", asset_type: str = ""
    ) -> dict | None:
        """Returns all Asset Administration Shell Descriptors.

        :param limit: Maximum number of Submodels to return
        :param cursor: Cursor for pagination
        :param asset_kind: The Asset's kind (Instance or Type). Available values : Instance, NotApplicable, Type
        :param asset_type: The Asset's type (UTF8-BASE64-URL-encoded)
        :return: Asset Administration Shell Descriptors data or None if an error occurred
        """
        url = f"{self._base_url}/shell-descriptors"

        params = {}
        if asset_kind:
            params["asset_kind"] = asset_kind
        if asset_type:
            params["asset_type"] = asset_type
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor

        self._set_token()

        try:
            response = self._session.get(url, params=params, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # POST /shell-descriptors
    def post_asset_administration_shell_descriptor(self, request_body: dict) -> dict | None:
        """Creates a new Asset Administration Shell Descriptor, i.e. registers an AAS.

        :param request_body: Asset Administration Shell Descriptor object
        :return: Created Asset Administration Shell Descriptor data or None if an error occurred
        """
        url = f"{self._base_url}/shell-descriptors"

        self._set_token()

        try:
            response = self._session.post(url, json=request_body, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_201:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # DELETE /shell-descriptors
    def delete_all_asset_administration_shell_descriptors(self) -> bool:
        """Deletes all Asset Administration Shell Descriptors.

        :return: True if deletion was successful, False otherwise
        """
        url = f"{self._base_url}/shell-descriptors"

        self._set_token()

        try:
            response = self._session.delete(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # GET /shell-descriptors/{aasIdentifier}/submodel-descriptors
    # POST /shell-descriptors/{aasIdentifier}/submodel-descriptors
    # POST /search
    def search(self, request_body: dict) -> dict | None:
        """Searches for Asset Administration Shell Descriptors based on the provided query.

        :param request_body:query as a dictionary
        :return: Search results as a dictionary or None if an error occurred
        """
        url = f"{self._base_url}/search"

        self._set_token()

        try:
            response = self._session.post(url, json=request_body, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # GET /description
    def get_self_description(self) -> dict | None:
        """Returns the self-describing information of a network resource (ServiceDescription).

        :return: self-describing information of a network resource
        """
        url = f"{self._base_url}/description"

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
