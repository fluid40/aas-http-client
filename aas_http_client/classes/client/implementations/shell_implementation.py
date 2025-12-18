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


class ShellImplementation(BaseModel):
    """Implementation of Asset Administration Shell related API calls."""

    def __init__(self, session: requests.Session, base_url: str, time_out: int, auth_method: AuthMethod, o_auth_settings: OAuth, encoded_ids: bool):
        """Initializes the ShellImplementation with the given parameters."""
        self._session = session
        self._base_url = base_url
        self._time_out = time_out
        self._encoded_ids = encoded_ids
        self._auth_method = auth_method
        self._o_auth_settings = o_auth_settings

    # GET /shells/{aasIdentifier}
    def get_asset_administration_shell_by_id(self, aas_identifier: str) -> dict | None:
        """Returns a specific Asset Administration Shell.

        :param aas_identifier: The Asset Administration Shell’s unique id
        :return: Asset Administration Shells data or None if an error occurred
        """
        if not self._encoded_ids:
            aas_identifier: str = decode_base_64(aas_identifier)

        url = f"{self._base_url}/shells/{aas_identifier}"

        self._set_token()

        try:
            response = self._session.get(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Asset Administration Shell with id '{aas_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # PUT /shells/{aasIdentifier}
    def put_asset_administration_shell_by_id(self, aas_identifier: str, request_body: dict) -> bool:
        """Creates or replaces an existing Asset Administration Shell.

        :param aas_identifier: The Asset Administration Shell’s unique id
        :param request_body: Json data of the Asset Administration Shell data to put
        :return: True if the update was successful, False otherwise
        """
        if not self._encoded_ids:
            aas_identifier: str = decode_base_64(aas_identifier)

        url = f"{self._base_url}/shells/{aas_identifier}"

        self._set_token()

        try:
            response = self._session.put(url, json=request_body, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Asset Administration Shell with id '{aas_identifier}' not found.")
                return None

            if response.status_code is not STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # DELETE /shells/{aasIdentifier}
    def delete_asset_administration_shell_by_id(self, aas_identifier: str) -> bool:
        """Deletes an Asset Administration Shell.

        :param aas_identifier: The Asset Administration Shell’s unique id
        :return: True if the deletion was successful, False otherwise
        """
        if not self._encoded_ids:
            aas_identifier: str = decode_base_64(aas_identifier)

        url = f"{self._base_url}/shells/{aas_identifier}"

        self._set_token()

        try:
            response = self._session.delete(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Asset Administration Shell with id '{aas_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # GET /shells/{aasIdentifier}
    # PUT /shells/{aasIdentifier}
    # GET /shells/{aasIdentifier}/asset-information/thumbnail
    # PUT /shells/{aasIdentifier}/asset-information/thumbnail
    # DELETE /shells/{aasIdentifier}/asset-information/thumbnail

    # GET /shells
    def get_all_asset_administration_shells(
        self, asset_ids: list[dict] | None = None, id_short: str = "", limit: int = 100, cursor: str = ""
    ) -> dict | None:
        """Returns all Asset Administration Shells.

        :param assetIds: A list of specific Asset identifiers (format: {"identifier": "string",  "encodedIdentifier": "string"})
        :param idShort: The Asset Administration Shell's IdShort
        :param limit: The maximum number of elements in the response array
        :param cursor: A server-generated identifier retrieved from pagingMetadata that specifies from which position the result listing should continue
        :return: List of paginated Asset Administration Shells data or None if an error occurred
        """
        url = f"{self._base_url}/shells"

        # Build query parameters
        if asset_ids is None:
            asset_ids = []

        params = {}
        if asset_ids is not None and len(asset_ids) > 0:
            params["assetIds"] = asset_ids
        if id_short:
            params["idShort"] = id_short
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor

        self._set_token()

        try:
            response = self._session.get(url, timeout=self._time_out, params=params)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # POST /shells
    def post_asset_administration_shell(self, request_body: dict) -> dict | None:
        """Creates a new Asset Administration Shell.

        :param request_body: Json data of the Asset Administration Shell to post
        :return: Response data as a dictionary or None if an error occurred
        """
        url = f"{self._base_url}/shells"
        logger.debug(f"Call REST API url '{url}'")

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

    # GET /shells/{aasIdentifier}/submodel-refs
    # POST /shells/{aasIdentifier}/submodel-refs
    # DELETE /shells/{aasIdentifier}/submodel-refs/{submodelIdentifier}

    # not supported by Java Server

    # PUT /shells/{aasIdentifier}/submodels/{submodelIdentifier}
    def put_submodel_by_id_aas_repository(self, aas_identifier: str, submodel_identifier: str, request_body: dict) -> bool:
        """Updates the Submodel.

        :param aas_identifier: ID of the AAS to update the submodel for
        :param submodel_identifier: ID of the submodel to update
        :param request_body: Json data to the Submodel to put
        :return: True if the update was successful, False otherwise
        """
        if not self._encoded_ids:
            aas_identifier: str = decode_base_64(aas_identifier)
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/shells/{aas_identifier}/submodels/{submodel_identifier}"

        self._set_token()

        try:
            response = self._session.put(url, json=request_body, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Asset Administration Shell with id '{aas_identifier}' or submodel with id '{submodel_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # GET /shells/{aasIdentifier}/$reference
    def get_asset_administration_shell_by_id_reference_aas_repository(self, aas_identifier: str) -> dict | None:
        """Returns a specific Asset Administration Shell as a Reference.

        :param aas_identifier: ID of the AAS reference to retrieve
        :return: Asset Administration Shells reference data or None if an error occurred
        """
        if not self._encoded_ids:
            aas_identifier: str = decode_base_64(aas_identifier)

        url = f"{self._base_url}/shells/{aas_identifier}/$reference"

        self._set_token()

        try:
            response = self._session.get(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Asset Administration Shell with id '{aas_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        ref_dict_string = response.content.decode("utf-8")
        return json.loads(ref_dict_string)

    # GET /shells/{aasIdentifier}/submodels/{submodelIdentifier}
    def get_submodel_by_id_aas_repository(self, aas_identifier: str, submodel_identifier: str) -> dict | None:
        """Returns the Submodel.

        :param aas_identifier: ID of the AAS to retrieve the submodel from
        :param submodel_identifier: ID of the submodel to retrieve
        :return: Submodel object or None if an error occurred
        """
        if not self._encoded_ids:
            aas_identifier: str = decode_base_64(aas_identifier)
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/shells/{aas_identifier}/submodels/{submodel_identifier}"

        self._set_token()

        try:
            response = self._session.get(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Asset Administration Shell with id '{aas_identifier}' or submodel with id '{submodel_identifier}' not found.")
                return None

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
