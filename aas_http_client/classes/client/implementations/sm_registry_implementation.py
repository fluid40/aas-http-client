"""Submodel Registry Implementation Module."""

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


class SubmodelRegistryImplementation(BaseModel):
    """Implementation of Submodel Registry related API calls."""

    def __init__(self, session: requests.Session, base_url: str, time_out: int, auth_method: AuthMethod, o_auth_settings: OAuth, encoded_ids: bool):
        """Initializes the SubmodelRegistryImplementation with the given parameters."""
        self._session = session
        self._base_url = base_url
        self._time_out = time_out
        self._encoded_ids = encoded_ids
        self._auth_method = auth_method
        self._o_auth_settings = o_auth_settings

    # GET /submodel-descriptors/{submodelIdentifier}
    # PUT /submodel-descriptors/{submodelIdentifier}
    # DELETE /submodel-descriptors/{submodelIdentifier}

    # GET /submodel-descriptors
    def get_all_submodel_descriptors(self, limit: int = 100, cursor: str = "") -> dict | None:
        """Returns all Submodel Descriptors.

        :param limit: The maximum number of elements in the response array
        :param cursor: A server-generated identifier retrieved from pagingMetadata that specifies from which position the result listing should continue
        :return: Submodel Descriptors data or None if an error occurred
        """
        url = f"{self._base_url}/submodel-descriptors"

        params = {}
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

    # POST /submodel-descriptors
    def post_submodel_descriptor(self, request_body: dict) -> dict | None:
        """Creates a new Submodel Descriptor, i.e. registers a submodel.

        :param request_body: Submodel Descriptor object
        :return: Created Submodel Descriptor data or None if an error occurred
        """
        url = f"{self._base_url}/submodel-descriptors"

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

    # DELETE /submodel-descriptors
    def delete_all_submodel_descriptors(self) -> bool:
        """Deletes all Submodel Descriptors.

        :return: True if deletion was successful, False otherwise
        """
        url = f"{self._base_url}/submodel-descriptors"

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
