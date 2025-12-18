import json
import logging

import requests
from pydantic import BaseModel

from aas_http_client.classes.client.implementations import AuthMethod, get_token
from aas_http_client.classes.Configuration.config_classes import OAuth
from aas_http_client.utilities.encoder import decode_base_64
from aas_http_client.utilities.http_helper import (
    STATUS_CODE_200,
    STATUS_CODE_201,
    STATUS_CODE_204,
    STATUS_CODE_404,
    log_response_errors,
)

logger = logging.getLogger(__name__)


class SmImplementation(BaseModel):
    """Implementation of Submodel related API calls."""

    def __init__(self, session: requests.Session, base_url: str, time_out: int, auth_method: AuthMethod, o_auth_settings: OAuth, encoded_ids: bool):
        """Initializes the SmImplementation with the given parameters."""
        self._session = session
        self._base_url = base_url
        self._time_out = time_out
        self._encoded_ids = encoded_ids
        self._auth_method = auth_method
        self._o_auth_settings = o_auth_settings

    # GET /submodels/{submodelIdentifier}
    def get_submodel_by_id(self, submodel_identifier: str, level: str = "", extent: str = "") -> dict | None:
        """Returns a specific Submodel.

        :param submodel_identifier: The Submodel’s unique id
        :param level: Determines the structural depth of the respective resource content. Available values : deep, core
        :param extent: Determines to which extent the resource is being serialized. Available values : withBlobValue, withoutBlobValue
        :return: Submodel data or None if an error occurred
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}"

        params = {}
        if level:
            params["level"] = level
        if extent:
            params["extent"] = extent

        self._set_token()

        try:
            response = self._session.get(url, params=params, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel with id '{submodel_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # PUT /submodels/{submodelIdentifier}
    def put_submodels_by_id(self, submodel_identifier: str, request_body: dict) -> bool:
        """Updates a existing Submodel.

        :param submodel_identifier: The Submodel’s unique id
        :param request_body: Json data of the Submodel to update
        :return: True if the update was successful, False otherwise
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}"

        self._set_token()

        try:
            response = self._session.put(url, json=request_body, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel with id '{submodel_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # DELETE /submodels/{submodelIdentifier}
    def delete_submodel_by_id(self, submodel_identifier: str) -> bool:
        """Deletes a Submodel.

        :param submodel_identifier: The Submodel’s unique id
        :return: True if the deletion was successful, False otherwise
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}"

        self._set_token()

        try:
            response = self._session.delete(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel with id '{submodel_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # GET /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}
    def get_submodel_element_by_path_submodel_repo(
        self, submodel_identifier: str, id_short_path: str, level: str = "", extent: str = ""
    ) -> dict | None:
        """Returns a specific submodel element from the Submodel at a specified path.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :param level: Determines the structural depth of the respective resource content. Available values : deep, core
        :param extent: Determines to which extent the resource is being serialized. Available values : withBlobValue, withoutBlobValue
        :return: Submodel element data or None if an error occurred
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}"

        params = {}
        if level:
            params["level"] = level
        if extent:
            params["extent"] = extent

        self._set_token()

        try:
            response = self._session.get(url, params=params, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return None

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel with id '{submodel_identifier}' not found.")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # PUT /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}

    # POST /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}
    def post_submodel_element_by_path_submodel_repo(
        self, submodel_identifier: str, id_short_path: str, request_body: dict, level: str = "", extent: str = ""
    ) -> dict | None:
        """Creates a new submodel element at a specified path within submodel elements hierarchy.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :param request_body: Data for the new Submodel element
        :param level: Determines the structural depth of the respective resource content. Available values : deep, core
        :param extent: Determines to which extent the resource is being serialized. Available values : withBlobValue, withoutBlobValue
        :return: Submodel element data or None if an error occurred
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}"

        params = {}
        if level:
            params["level"] = level
        if extent:
            params["extent"] = extent

        self._set_token()

        try:
            response = self._session.post(url, json=request_body, params=params, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return None

            if response.status_code != STATUS_CODE_201:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    # DELETE /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}
    def delete_submodel_element_by_path_submodel_repo(self, submodel_identifier: str, id_short_path: str):
        """Deletes a submodel element at a specified path within the submodel elements hierarchy.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :return: True if the deletion was successful, False otherwise
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}"

        self._set_token()
        try:
            response = self._session.delete(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # GET /submodels
    def get_all_submodels(
        self, semantic_id: str = "", id_short: str = "", limit: int = 0, cursor: str = "", level: str = "", extent: str = ""
    ) -> dict | None:
        """Returns all Submodels.

        :param semantic_id: The value of the semantic id reference (UTF8-BASE64-URL-encoded)
        :param id_short: The Submodels’s IdShort
        :param limit: The maximum number of elements in the response array
        :param cursor: A server-generated identifier retrieved from pagingMetadata that specifies from which position the result listing should continue
        :param level: Determines the structural depth of the respective resource content. Available values : deep, core
        :param extent: Determines to which extent the resource is being serialized. Available values : withBlobValue, withoutBlobValue
        :return: List of Submodel data or None if an error occurred
        """
        url = f"{self._base_url}/submodels"

        params = {}
        if semantic_id:
            params["semanticId"] = semantic_id
        if id_short:
            params["idShort"] = id_short
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor
        if level:
            params["level"] = level
        if extent:
            params["extent"] = extent

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

    # POST /submodels
    def post_submodel(self, request_body: dict) -> dict | None:
        """Creates a new Submodel.

        :param request_body: Json data of the Submodel to post
        :return: Submodel data or None if an error occurred
        """
        url = f"{self._base_url}/submodels"

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

    # GET /submodels/{submodelIdentifier}/submodel-elements
    def get_all_submodel_elements_submodel_repository(
        self, submodel_identifier: str, limit: int = 100, cursor: str = "", level: str = "", extent: str = ""
    ) -> list[dict] | None:
        """Returns all submodel elements including their hierarchy.

        :param submodel_identifier: The Submodel’s unique id
        :param limit: The maximum number of elements in the response array
        :param cursor: A server-generated identifier retrieved from pagingMetadata that specifies from which position the result listing should continue
        :param level: Determines the structural depth of the respective resource content. Available values : deep, core
        :param extent: Determines to which extent the resource is being serialized. Available values : withBlobValue, withoutBlobValue
        :return: List of Submodel element data or None if an error occurred
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements"

        params = {}
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor
        if level:
            params["level"] = level
        if extent:
            params["extent"] = extent

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

    # POST /submodels/{submodelIdentifier}/submodel-elements
    def post_submodel_element_submodel_repo(self, submodel_identifier: str, request_body: dict) -> dict | None:
        """Creates a new submodel element.

        :param submodel_identifier: The Submodel’s unique id
        :param request_body: Data for the new Submodel element
        :return: Submodel element data or None if an error occurred
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements"

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

    # POST /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke
    # GET /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value

    # PATCH /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value
    def patch_submodel_element_by_path_value_only_submodel_repo(
        self, submodel_identifier: str, id_short_path: str, value: str, level: str = ""
    ) -> bool:
        """Updates the value of an existing SubmodelElement.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :param value: Submodel element value to update as string
        :param level: Determines the structural depth of the respective resource content. Available values : deep, core
        :return: True if the patch was successful, False otherwise
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}/$value"

        params = {}
        if level:
            params["level"] = level

        self._set_token()

        try:
            response = self._session.patch(url, json=value, params=params, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # GET /submodels/{submodelIdentifier}/$value
    # PATCH /submodels/{submodelIdentifier}/$value
    # GET /submodels/{submodelIdentifier}/$metadata

    # not supported by Java Server

    # PATCH /submodels/{submodelIdentifier}
    def patch_submodel_by_id(self, submodel_identifier: str, submodel_data: dict) -> bool:
        """Updates an existing Submodel.

        :param submodel_identifier: The Submodel’s unique id
        :return: True if the patch was successful, False otherwise
        """
        if not self._encoded_ids:
            submodel_identifier: str = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}"

        self._set_token()

        try:
            response = self._session.patch(url, json=submodel_data, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == STATUS_CODE_404:
                logger.warning(f"Submodel with id '{submodel_identifier}' not found.")
                return None

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

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
