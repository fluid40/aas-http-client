"""Client for HTTP API communication with AAS server."""

import json
import logging
import time
from pathlib import Path

import basyx.aas.adapter.json
import requests
from basyx.aas.model import Reference, Submodel
from pydantic import BaseModel, Field, PrivateAttr, ValidationError
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.models import Response

from aas_http_client.classes.config_classes import AuthenticationConfig
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

    :param response: HTTP response object
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
        if response.content and response.content != "b''":
            result_error_messages.append(response.content)

    logger.error(f"Status code: {response.status_code}")
    for result_error_message in result_error_messages:
        logger.error(result_error_message)


class AasHttpClient(BaseModel):
    """Represents a AasHttpClient to communicate with a REST API."""

    base_url: str = Field(..., alias="BaseUrl", description="Base URL of the AAS server.")
    auth_settings: AuthenticationConfig = Field(
        default_factory=AuthenticationConfig, alias="AuthenticationSettings", description="Authentication settings for the AAS server."
    )
    https_proxy: str | None = Field(default=None, alias="HttpsProxy", description="HTTPS proxy URL.")
    http_proxy: str | None = Field(default=None, alias="HttpProxy", description="HTTP proxy URL.")
    time_out: int = Field(default=200, alias="TimeOut", description="Timeout for HTTP requests.")
    connection_time_out: int = Field(default=100, alias="ConnectionTimeOut", description="Connection timeout for HTTP requests.")
    ssl_verify: bool = Field(default=True, alias="SslVerify", description="Enable SSL verification.")
    trust_env: bool = Field(default=True, alias="TrustEnv", description="Trust environment variables.")
    _session: Session = PrivateAttr(default=None)

    def initialize(self):
        """Initialize the AasHttpClient with the given URL, username and password."""
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]

        self._session = requests.Session()

        self._session.auth = HTTPBasicAuth(self.auth_settings.basic_auth.username, self.auth_settings.basic_auth.get_password())

        self._session.verify = self.ssl_verify
        self._session.trust_env = self.trust_env

        if self.https_proxy:
            self._session.proxies.update({"https": self.https_proxy})
        if self.http_proxy:
            self._session.proxies.update({"http": self.http_proxy})

    def get_root(self) -> dict | None:
        """Get the root of the REST API.

        :return: Root data as a dictionary or None if an error occurred
        """
        url = f"{self.base_url}/shells"

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
        """Set authentication token by client credentials.

        :return: Token dictionary or None if an error occurred
        """
        token = None

        if self.auth_settings.bearer_auth.is_active():
            token = self.auth_settings.bearer_auth.get_token()

        elif self.auth_settings.service_provider_auth.is_active() and self.auth_settings.service_provider_auth.grant_type == "password":
            token = get_token_by_password(
                self.auth_settings.service_provider_auth.token_url,
                self.auth_settings.service_provider_auth.client_id,
                self.auth_settings.service_provider_auth.get_client_secret(),
                self.time_out,
            )

        elif self.auth_settings.service_provider_auth.is_active() and self.auth_settings.service_provider_auth.grant_type == "client_credentials":
            token = get_token_by_basic_auth(
                self.auth_settings.service_provider_auth.token_url,
                self.auth_settings.service_provider_auth.client_id,
                self.auth_settings.service_provider_auth.get_client_secret(),
                self.time_out,
            )

        if token:
            self._session.headers.update({self.auth_settings.service_provider_auth.is_active().header_name: f"Bearer {token}"})

    # region shells

    def post_asset_administration_shell(self, aas_data: dict) -> dict | None:
        """Create a new Asset Administration Shell.

        :param aas_data: JSON data of the Asset Administration Shell to create
        :return: Response data as a dictionary or None if an error occurred
        """
        url = f"{self.base_url}/shells"
        logger.debug(f"Call REST API url '{url}'")

        if self.auth_settings.service_provider_auth.is_active():
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
        """Create or replace an existing Asset Administration Shell.

        :param identifier: Identifier of the AAS to update
        :param aas_data: JSON data of the Asset Administration Shell to update
        :return: True if the update was successful, False otherwise
        """
        decoded_identifier: str = decode_base_64(identifier)
        url = f"{self.base_url}/shells/{decoded_identifier}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Update the Submodel in an AAS repository.

        :param aas_id: ID of the AAS to update the submodel for
        :param submodel_id: ID of the submodel to update
        :param submodel_data: JSON data of the Submodel to update
        :return: True if the update was successful, False otherwise
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}/submodels/{decoded_submodel_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return all Asset Administration Shells.

        :return: List of paginated Asset Administration Shells data or None if an error occurred
        """
        url = f"{self.base_url}/shells"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return a specific Asset Administration Shell.

        :param aas_id: ID of the AAS to retrieve
        :return: Asset Administration Shell data or None if an error occurred
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return a specific Asset Administration Shell as a Reference.

        :param aas_id: ID of the AAS reference to retrieve
        :return: Asset Administration Shell reference data or None if an error occurred
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}/$reference"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return the Submodel from an AAS repository.

        :param aas_id: ID of the AAS to retrieve the submodel from
        :param submodel_id: ID of the submodel to retrieve
        :return: Submodel object or None if an error occurred
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        decoded_submodel_id: str = decode_base_64(submodel_id)

        url = f"{self.base_url}/shells/{decoded_aas_id}/submodels/{decoded_submodel_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Delete an Asset Administration Shell.

        :param aas_id: ID of the AAS to delete
        :return: True if the deletion was successful, False otherwise
        """
        decoded_aas_id: str = decode_base_64(aas_id)
        url = f"{self.base_url}/shells/{decoded_aas_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Create a new Submodel.

        :param submodel_data: JSON data of the Submodel to create
        :return: Submodel data or None if an error occurred
        """
        url = f"{self.base_url}/submodels"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Update an existing Submodel.

        :param identifier: Encoded ID of the Submodel to update
        :param submodel_data: JSON data of the Submodel to update
        :return: True if the update was successful, False otherwise
        """
        decoded_identifier: str = decode_base_64(identifier)
        url = f"{self.base_url}/submodels/{decoded_identifier}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return all Submodels.

        :return: List of Submodel data or None if an error occurred
        """
        url = f"{self.base_url}/submodels"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return a specific Submodel.

        :param submodel_id: Encoded ID of the Submodel to retrieve
        :return: Submodel data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Update an existing Submodel.

        :param submodel_id: Encoded ID of the Submodel to update
        :param submodel_data: JSON data of the Submodel to update
        :return: True if the patch was successful, False otherwise
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Delete a Submodel.

        :param submodel_id: Encoded ID of the Submodel to delete
        :return: True if the deletion was successful, False otherwise
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}"

        if self.auth_settings.service_provider_auth.is_active():
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
        """Return all submodel elements including their hierarchy.

        :param submodel_id: Encoded ID of the Submodel to retrieve elements from
        :return: List of Submodel element data or None if an error occurred
        """
        decoded_submodel_id: str = decode_base_64(submodel_id)
        url = f"{self.base_url}/submodels/{decoded_submodel_id}/submodel-elements"

        if self.auth_settings.service_provider_auth.is_active():
            self._set_token_by_client_credentials()

        try:
            response = self._session.get(url, headers=HEADERS, timeout=self.time_out)
            logger.debug(f"Call REST API url '{response.url
