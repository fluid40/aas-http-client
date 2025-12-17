import json
import logging
import mimetypes
from pathlib import Path

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


class ExperimentalImplementation(BaseModel):
    """Implementation of Asset Administration Shell Registry related API calls."""

    def __init__(self, session: requests.Session, base_url: str, time_out: int, auth_method: AuthMethod, o_auth_settings: OAuth, encoded_ids: bool):
        """Initializes the ShellRegistryImplementation with the given parameters."""
        self._session = session
        self._base_url = base_url
        self._time_out = time_out
        self._encoded_ids = encoded_ids
        self._auth_method = auth_method
        self._o_auth_settings = o_auth_settings

    # GET /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment
    def get_file_by_path_submodel_repo(self, submodel_identifier: str, id_short_path: str) -> bytes | None:
        """Downloads file content from a specific submodel element from the Submodel at a specified path. Experimental feature - may not be supported by all servers.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :return: Attachment data as bytes (octet-stream) or None if an error occurred
        """
        if not self._encoded_ids:
            submodel_identifier = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}/attachment"

        self._set_token()  # ensures Authorization header is set

        try:
            response = self._session.get(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == 404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return None

            if response.status_code != 200:
                log_response_errors(response)
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling REST API: {e}")
            return None

        return response.content

    # POST /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment
    def post_file_by_path_submodel_repo(self, submodel_identifier: str, id_short_path: str, file: Path) -> bool:
        """Uploads file content to an existing submodel element at a specified path within submodel elements hierarchy. Experimental feature - may not be supported by all servers.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :param file: Path to the file to upload as attachment
        :return: Attachment data as bytes or None if an error occurred
        """
        if file.exists() is False or not file.is_file():
            logger.error(f"Attachment file '{file}' does not exist.")
            return False

        if not self._encoded_ids:
            submodel_identifier = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}/attachment"

        self._set_token()

        try:
            mime_type, _ = mimetypes.guess_type(file)

            with file.open("rb") as f:
                files = {"file": (file.name, f, mime_type or "application/octet-stream")}
                response = self._session.post(url, files=files, timeout=self._time_out)

            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == 404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return False

            if response.status_code not in (200, 201, 204):
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # PUT /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment
    def put_file_by_path_submodel_repo(self, submodel_identifier: str, id_short_path: str, file: Path) -> bool:
        """Uploads file content to an existing submodel element at a specified path within submodel elements hierarchy. Experimental feature - may not be supported by all servers.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :param file: Path to the file to upload as attachment
        :return: Attachment data as bytes or None if an error occurred
        """
        if file.exists() is False or not file.is_file():
            logger.error(f"Attachment file '{file}' does not exist.")
            return False

        if not self._encoded_ids:
            submodel_identifier = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}/attachment"

        self._set_token()

        try:
            mime_type, _ = mimetypes.guess_type(file)

            with file.open("rb") as f:
                files = {"file": (file.name, f, mime_type or "application/octet-stream")}
                response = self._session.put(url, files=files, timeout=self._time_out)

            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == 404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return False

            if response.status_code not in (200, 201, 204):
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error call REST API: {e}")
            return False

        return True

    # DELETE /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment
    def delete_file_by_path_submodel_repo(self, submodel_identifier: str, id_short_path: str) -> bool:
        """Deletes file content of an existing submodel element at a specified path within submodel elements hierarchy. Experimental feature - may not be supported by all servers.

        :param submodel_identifier: The Submodel’s unique id
        :param id_short_path: IdShort path to the submodel element (dot-separated)
        :return: True if deletion was successful, False otherwise
        """
        if not self._encoded_ids:
            submodel_identifier = decode_base_64(submodel_identifier)

        url = f"{self._base_url}/submodels/{submodel_identifier}/submodel-elements/{id_short_path}/attachment"

        self._set_token()

        try:
            response = self._session.delete(url, timeout=self._time_out)
            logger.debug(f"Call REST API url '{response.url}'")

            if response.status_code == 404:
                logger.warning(f"Submodel element with IDShort path '{id_short_path}' not found.")
                return False

            if response.status_code not in (200, 202, 204):
                log_response_errors(response)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling REST API: {e}")
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

    def _post_multipart(self, url, files):
        headers = dict(self._session.headers)
        headers.pop("Content-Type", None)
        return self._session.post(url, headers=headers, files=files)
