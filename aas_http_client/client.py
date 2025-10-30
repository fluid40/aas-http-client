"""Client for HTTP API communication with AAS server."""

import json
import logging
import time
from pathlib import Path

import basyx.aas.adapter.json
import requests
from basyx.aas.model import Reference, Submodel
from pydantic import BaseModel, PrivateAttr, ValidationError
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.models import Response

from aas_http_client.classes.auth_classes import BasicAuthConfig, ServiceProviderAuthConfig
from aas_http_client.core.encoder import decode_base_64

logger = logging.getLogger(__name__)

STATUS_CODE_200 = 200
STATUS_CODE_201 = 201
STATUS_CODE_202 = 202
STATUS_CODE_204 = 204
STATUS_CODE_404 = 404
HEADERS = {"Content-Type": "application/json"}


def log_response_errors(response: Response):  # noqa: C901
    """Create error messages from the response and log them.

    :param response: response
    """
    result_error_messages: list[str] = []

    try:
        response_content_dict: dict = json.loads(response.content)

        if "detail" in response_content_dict:
            detail: dict = response_content_dict.get("detail", {})
            if "error" in detail:
                error: str = detail.get("error", "")
                result_error_messages.append(f"{error}")
            else:
                result_error_messages.append(f"{detail}")

        elif "messages" in response_content_dict or "Messages" in response_content_dict:
            messages: list = response_content_dict.get("messages", [])

            if not messages:
                messages = response_content_dict.get("Messages", [])

            for message in messages:
                if isinstance(message, dict) and "message" in message:
                    result_error_messages.append(message["message"])
                else:
                    result_error_messages.append(str(message))
        elif "error" in response_content_dict:
            result_error_messages.append(response_content_dict.get("error", ""))

        if len(result_error_messages) == 0 and response.text:
            result_error_messages.append(response.text)

    except json.JSONDecodeError:
        result_error_messages.append(response.content)

    logger.error(f"Status code: {response.status_code}")
    for result_error_message in result_error_messages:
        logger.error(result_error_message)


class AasHttpClient(BaseModel):
    """Represents a AasHttpClient to communicate with a REST API."""

    base_url: str = "http://javaaasserver:5060/"
    basic_auth: BasicAuthConfig | None = None
    service_provider_auth: ServiceProviderAuthConfig | None = None
    https_proxy: str | None = None
    http_proxy: str | None = None
    time_out: int = 200
    connection_time_out: int = 100
    ssl_verify: bool = True
    trust_env: bool = True
    auth_service_provider: str | None = None
    _session: Session = PrivateAttr(default=None)

    def initialize(
        self,
        basic_auth_password: str,
        service_provider_auth_client_secret: str,
    ):
        """Initialize the AasHttpClient with the given URL, username and password.

        :param password: password
        """
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]

        self._session = requests.Session()

        self._session.auth = HTTPBasicAuth("", "")
        if self.basic_auth:
            self._session.auth = HTTPBasicAuth(self.basic_auth.username, basic_auth_password)

        self._session.verify = self.ssl_verify
        self._session.trust_env = self.trust_env

        if self.service_provider_auth:
            self.service_provider_auth.set_client_secret(service_provider_auth_client_secret)

        if self.https_proxy:
            self._session.proxies.update({"https": self.https_proxy})
        if self.http_proxy:
            self._session.proxies.update({"http": self.http_proxy})

    def get_root(self) -> dict | None:
        """Get the root of the REST API.

        :return: root data as a dictionary or None if an error occurred
        """
        url = f"{self.base_url}/shells"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=10)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def _set_token_by_client_credentials(self) -> dict | None:
        if self.service_provider_auth is None:
            logger.error("Service provider authentication is not configured.")
            return None

        if self.service_provider_auth.grant_type == "password":
            token = get_token_by_password(
                self.service_provider_auth.token_url,
                self.service_provider_auth.client_id,
                self.service_provider_auth.get_client_secret(),
                self.time_out,
            )
        else:
            token = get_token_by_basic_auth(
                self.service_provider_auth.token_url,
                self.service_provider_auth.client_id,
                self.service_provider_auth.get_client_secret(),
                self.time_out,
            )

        if token:
            self._session.headers.update({self.service_provider_auth.header_name: f"Bearer {token}"})

    # region shells

    def post_asset_administration_shell(self, aas_data: dict) -> dict | None:
        """Creates a new Asset Administration Shell.

        :param aas_data: Json data of the Asset Administration Shell to post
        :return: Response data as a dictionary or None if an error occurred
        """
        url = f"{self.base_url}/shells"
        logger.debug(f"Call REST API url '{url}'")

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.post(url, headers=HEADERS, json=aas_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code not in (STATUS_CODE_201, STATUS_CODE_202):
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def put_asset_administration_shell_by_id(self, identifier: str, aas_data: dict) -> bool:
        """Creates or replaces an existing Asset Administration Shell.

        :param identifier: Identifier of the AAS to update
        :param aas_data: Json data of the Asset Administration Shell data to update
        :return: True if the update was successful, False otherwise
        """
        decoded_identifier: str = decode_base_64(identifier)
        url = f"{self.base_url}/shells/{decoded_identifier}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.put(url, headers=HEADERS, json=aas_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code is not STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    def put_submodel_by_id_aas_repository(self, aas_id: str, submodel_id: str, submodel_data: dict) -> bool:
        """Updates the Submodel.

        :param aas_id: ID of the AAS to update the submodel for
        :param submodel_data: Json data to the Submodel to update
        :return: True if the update was successful, False otherwise
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}/submodels/{decoded_submodel_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.put(url, headers=HEADERS, json=submodel_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    def get_all_asset_administration_shells(self) -> list[dict] | None:
        """Returns all Asset Administration Shells.

        :return: List of paginated Asset Administration Shells data or None if an error occurred
        """
        url = f"{self.base_url}/shells"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def get_asset_administration_shell_by_id(self, aas_id: str) -> dict | None:
        """Returns a specific Asset Administration Shell.

        :param aas_id: ID of the AAS to retrieve
        :return: Asset Administration Shells data or None if an error occurred
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def get_asset_administration_shell_by_id_reference_aas_repository(self, aas_id: str) -> Reference | None:
        """Returns a specific Asset Administration Shell as a Reference.

        :param aas_id: ID of the AAS reference to retrieve
        :return: Asset Administration Shells reference data or None if an error occurred
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}/$reference"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        ref_dict_string = response.content.decode("utf-8")
        return json.loads(ref_dict_string, cls=basyx.aas.adapter.json.AASFromJsonDecoder)

    def get_submodel_by_id_aas_repository(self, aas_id: str, submodel_id: str) -> Submodel | None:
        """Returns the Submodel.

        :param aas_id: ID of the AAS to retrieve the submodel from
        :param submodel_id: ID of the submodel to retrieve
        :return: Submodel object or None if an error occurred
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        decoded_submodel_id: str = decode_base_64(submodel_id)

        url = f"{self.base_url}/shells/{decoded_aas_id}/submodels/{decoded_submodel_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def delete_asset_administration_shell_by_id(self, aas_id: str) -> bool:
        """Deletes an Asset Administration Shell.

        :param aas_id: ID of the AAS to retrieve
        :return: True if the deletion was successful, False otherwise
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.delete(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # endregion

    # region submodels

    def post_submodel(self, submodel_data: dict) -> dict | None:
        """Creates a new Submodel.

        :param Submodel_data: Json data of the Submodel to post
        :return: Submodel data or None if an error occurred
        """
        url = f"{self.base_url}/submodels"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.post(url, headers=HEADERS, json=submodel_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code not in (STATUS_CODE_201, STATUS_CODE_202):
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def put_submodels_by_id(self, identifier: str, submodel_data: dict) -> bool:
        """Updates a existing Submodel.

        :param identifier: Encoded ID of the Submodel to update
        :param submodel_data: Json data of the Submodel to update
        :return: True if the update was successful, False otherwise
        """
        decoded_identifier: str = decode_base_64(identifier)
        url = f"{self.base_url}/submodels/{decoded_identifier}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.put(url, headers=HEADERS, json=submodel_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    def get_all_submodels(self) -> list[dict] | None:
        """Returns all Submodels.

        :return: List of Submodel data or None if an error occurred
        """
        url = f"{self.base_url}/submodels"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def get_submodel_by_id(self, submodel_id: str) -> dict | None:
        """Returns a specific Submodel.

        :param submodel_id: Encoded ID of the Submodel to retrieve
        :return: Submodel data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def patch_submodel_by_id(self, submodel_id: str, submodel_data: dict) -> bool:
        """Updates an existing Submodel.

        :param submodel_id: Encoded ID of the Submodel to delete
        :return: True if the patch was successful, False otherwise
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.patch(url, headers=HEADERS, json=submodel_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    def delete_submodel_by_id(self, submodel_id: str) -> bool:
        """Deletes a Submodel.

        :param submodel_id: Encoded ID of the Submodel to delete
        :return: True if the deletion was successful, False otherwise
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.delete(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    def get_all_submodel_elements_submodel_repository(self, submodel_id: str) -> list[dict] | None:
        """Returns all submodel elements including their hierarchy.

        :param submodel_id: Encoded ID of the Submodel to retrieve elements from
        :return: List of Submodel element data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def post_submodel_element_submodel_repo(self, submodel_id: str, submodel_element_data: dict) -> dict | None:
        """Creates a new submodel element.

        :param submodel_id: Encoded ID of the Submodel to create elements for
        :return: Submodel element data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.post(url, headers=HEADERS, json=submodel_element_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_201:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def post_submodel_element_by_path_submodel_repo(self, submodel_id: str, submodel_element_path: str, submodel_element_data: dict) -> dict | None:
        """Creates a new submodel element at a specified path within submodel elements hierarchy.

        :param submodel_id: Encoded ID of the Submodel to create elements for
        :param submodel_element_path: Path within the Submodel elements hierarchy
        :param submodel_element_data: Data for the new Submodel element
        :return: Submodel element data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements/{submodel_element_path}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.post(url, headers=HEADERS, json=submodel_element_data, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_201:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def get_submodel_element_by_path_submodel_repo(self, submodel_id: str, submodel_element_path: str) -> dict | None:
        """Returns a specific submodel element from the Submodel at a specified path.

        :param submodel_id: Encoded ID of the Submodel to retrieve element from
        :param submodel_element_path: Path of the Submodel element to retrieve
        :return: Submodel element data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)

        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements/{submodel_element_path}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return None

        content = response.content.decode("utf-8")
        return json.loads(content)

    def delete_submodel_element_by_path_submodel_repo(self, submodel_id: str, submodel_element_path: str):
        """Deletes a submodel element at a specified path within the submodel elements hierarchy.

        :param submodel_id: Encoded ID of the Submodel to delete submodel element from
        :param submodel_element_path: Path of the Submodel element to delete
        :return: True if the deletion was successful, False otherwise
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)

        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements/{submodel_element_path}"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.delete(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    def patch_submodel_element_by_path_value_only_submodel_repo(self, submodel_id: str, submodel_element_path: str, value: str) -> bool:
        """Updates the value of an existing SubmodelElement.

        :param submodel_id: Encoded ID of the Submodel to update submodel element for
        :param submodel_element_path: Path of the Submodel element to update
        :param value: Submodel element value to update as string
        :return: True if the patch was successful, False otherwise
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)

        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements/{submodel_element_path}/$value"

        if self.service_provider_auth:
            self._set_token_by_client_credentials()

        try:
            response = self._session.patch(url, headers=HEADERS, json=value, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code != STATUS_CODE_204:
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True


# endregion

# region client


def get_token_by_basic_auth(endpoint: str, username: str, password: str, timeout=200) -> dict | None:
    """Get token from a specific authentication service provider by basic authentication.

    :param endpoint: Get token endpoint for the authentication service provider
    :param username: Username for the authentication service provider
    :param password: Password for the authentication service provider
    :param timeout: Timeout for the API calls, defaults to 200
    :return: Access token or None if an error occurred
    """
    data = {"grant_type": "client_credentials"}

    auth = HTTPBasicAuth(username, password)

    try:
        response = requests.post(endpoint, auth=auth, data=data, timeout=timeout)
        logger.info(f"Request URL: {response.url}")
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        logger.error(f"Error getting token: {e}")
        return None


def get_token_by_password(endpoint: str, username: str, password: str, timeout=200) -> dict | None:
    """Get token from a specific authentication service provider by username and password.

    :param endpoint: Get token endpoint for the authentication service provider
    :param username: Username for the authentication service provider
    :param password: Password for the authentication service provider
    :param timeout: Timeout for the API calls, defaults to 200
    :return: Access token or None if an error occurred
    """
    data = {"grant_type": "password", "username": username, "password": password}

    return _get_token(endpoint, data, timeout)


def _get_token(endpoint: str, data: dict[str, str], timeout: int = 200) -> dict | None:
    """Get token from a specific authentication service provider.

    :param endpoint: Get token endpoint for the authentication service provider
    :param data: Data for the authentication service provider
    :param timeout: Timeout for the API calls, defaults to 200
    :return: Access token or None if an error occurred
    """
    try:
        response = requests.post(endpoint, json=data, timeout=timeout)
        logger.info(f"Request URL: {response.url}")
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        logger.error(f"Error getting token: {e}")
        return None


def create_client_by_url(
    base_url: str,
    basic_auth_username: str = "",
    basic_auth_password: str = "",
    service_provider_auth_client_id: str = "",
    service_provider_auth_client_secret: str = "",
    service_provider_auth_token_url: str = "",
    http_proxy: str = "",
    https_proxy: str = "",
    time_out: int = 200,
    connection_time_out: int = 60,
    ssl_verify: str = True,  # noqa: FBT002
    trust_env: bool = True,  # noqa: FBT001, FBT002
) -> AasHttpClient | None:
    """Create a HTTP client for a AAS server connection from the given parameters.

    :param base_url: Base URL of the AAS server, e.g. "http://basyx_python_server:80/"_
    :param username: Username for the AAS server, defaults to ""
    :param basic_auth_password: password for the BaSyx server basic auth, defaults to ""
    :param http_proxy: http proxy URL, defaults to ""
    :param https_proxy: https proxy URL, defaults to ""
    :param time_out: Timeout for the API calls, defaults to 200
    :param connection_time_out: Timeout for the connection to the API, defaults to 60
    :param ssl_verify: Whether to verify SSL certificates, defaults to True
    :param trust_env: Whether to trust environment variables for proxy settings, defaults to True
    :return: An instance of Http client initialized with the provided parameters.
    """
    logger.info(f"Create AAS server http client from URL '{base_url}'.")
    config_dict: dict[str, str] = {}
    config_dict["base_url"] = base_url
    config_dict["http_proxy"] = http_proxy
    config_dict["https_proxy"] = https_proxy
    config_dict["time_out"] = time_out
    config_dict["connection_time_out"] = connection_time_out
    config_dict["ssl_verify"] = ssl_verify
    config_dict["trust_env"] = trust_env
    config_dict["basic_auth"] = None
    config_dict["service_provider_auth"] = None

    if basic_auth_password and basic_auth_username:
        config_dict["basic_auth"] = {"username": basic_auth_username}

    if service_provider_auth_client_id and service_provider_auth_client_secret and service_provider_auth_token_url:
        config_dict["service_provider_auth"] = {
            "client_id": service_provider_auth_client_id,
            "token_url": service_provider_auth_token_url,
        }

    return create_client_by_dict(config_dict, basic_auth_password, service_provider_auth_client_secret)


def create_client_by_dict(configuration: dict, basic_auth_password: str = "", service_provider_auth_client_secret: str = "") -> AasHttpClient | None:
    """Create a HTTP client for a AAS server connection from the given configuration.

    :param configuration: Dictionary containing the BaSyx server connection settings.
    :param basic_auth_password: Password for the AAS server basic auth, defaults to ""
    :return: An instance of Http client initialized with the provided parameters.
    """
    logger.info("Create AAS server http client from dictionary.")
    config_string = json.dumps(configuration, indent=4)

    return _create_client(config_string, basic_auth_password, service_provider_auth_client_secret)


def create_client_by_config(config_file: Path, basic_auth_password: str = "", service_provider_auth_client_secret: str = "") -> AasHttpClient | None:
    """Create a HTTP client for a AAS server connection from a given configuration file.

    :param config_file: Path to the configuration file containing the AAS server connection settings.
    :param basic_auth_password: password for the BaSyx server basic auth, defaults to ""
    :return: An instance of Http client initialized with the provided parameters.
    """
    config_file = config_file.resolve()
    logger.info(f"Create AAS server http client from configuration file '{config_file}'.")
    if not config_file.exists():
        config_string = "{}"
        logger.warning(f"Configuration file '{config_file}' not found. Using default configuration.")
    else:
        config_string = config_file.read_text(encoding="utf-8")
        logger.debug(f"Configuration  file '{config_file}' found.")

    return _create_client(config_string, basic_auth_password, service_provider_auth_client_secret)


def _create_client(config_string: str, basic_auth_password: str, service_provider_auth_client_secret: str) -> AasHttpClient | None:
    try:
        client = AasHttpClient.model_validate_json(config_string)
    except ValidationError as ve:
        raise ValidationError(f"Invalid BaSyx server configuration file: {ve}") from ve

    logger.info("Using server configuration:")
    logger.info(f"base_url: '{client.base_url}'")
    logger.info(f"timeout: '{client.time_out}'")

    if client.basic_auth:
        logger.info(f"basic_auth: '{client.basic_auth.username}'")
    if client.service_provider_auth:
        logger.info(f"service_provider_auth: '{client.service_provider_auth.token_url}': {client.service_provider_auth.client_id}'")

    logger.info(f"https_proxy: '{client.https_proxy}'")
    logger.info(f"http_proxy: '{client.http_proxy}'")
    logger.info(f"connection_timeout: '{client.connection_time_out}'.")
    client.initialize(basic_auth_password, service_provider_auth_client_secret)

    # test the connection to the REST API
    connected = _connect_to_api(client)

    if not connected:
        return None

    return client


def _connect_to_api(client: AasHttpClient) -> bool:
    start_time = time.time()
    logger.debug(f"Try to connect to REST API '{client.base_url}' for {client.connection_time_out} seconds.")
    counter: int = 0
    while True:
        try:
            root = client.get_root()
            if root:
                logger.info(f"Connected to server API at '{client.base_url}' successfully.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        if time.time() - start_time > client.connection_time_out:
            raise TimeoutError(f"Connection to server API timed out after {client.connection_time_out} seconds.")

        counter += 1
        logger.warning(f"Retrying connection (attempt: {counter}).")
        time.sleep(1)


# endregion
