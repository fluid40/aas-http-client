"""Main process for the demo."""

import logging
from pathlib import Path

from basyx.aas import model

from aas_http_client import client as aas_client
from aas_http_client.utilities import model_builder, sdk_tools
from aas_http_client.wrapper import sdk_wrapper

logger = logging.getLogger(__name__)


def start() -> None:
    """Start the demo process."""
    # create a submodel element
    sme_short_id: str = model_builder.create_unique_short_id("poc_sme")
    sme = model_builder.create_base_submodel_element_property(sme_short_id, model.datatypes.String, "Sample Value")
    clone = model_builder.clone_submodel_element_property(sme)

    # create a submodel
    sm_short_id: str = model_builder.create_unique_short_id("poc_sm")
    submodel = model_builder.create_base_submodel(sm_short_id, sm_short_id)
    # add submodel element to submodel
    # submodel.submodel_element.add(sme)

    # create an AAS
    aas_short_id: str = model_builder.create_unique_short_id("poc_aas")
    aas = model_builder.create_base_ass(aas_short_id, aas_short_id)

    # add submodel to AAS
    sdk_tools.add_submodel_to_aas(aas, submodel)

    client = aas_client.create_client_by_url(
        "http://javaaasserver:8075/",
        service_provider_auth_client_id="fluid40",
        service_provider_auth_client_secret="LdFB4jRrMMkgcVWgFkOVdDVDXtQ5os8w",
        service_provider_auth_token_url="https://aurora-fluid40.iqstruct-engineering.de/auth/realms/BaSyx/protocol/openid-connect/token",
    )

    client = aas_client.create_client_by_config(Path("./aas_http_client/demo/java_server_config.yml"))

    # tmp = get_token_by_basic_auth(
    #     "https://aurora-fluid40.iqstruct-engineering.de/auth/realms/BaSyx/protocol/openid-connect/token",
    #     "fluid40",
    #     "LdFB4jRrMMkgcVWgFkOVdDVDXtQ5os8w",
    # )

    wrapper = _create_sdk_wrapper(Path("./aas_http_client/demo/python_server_config.yml"))
    for existing_shell in wrapper.get_all_asset_administration_shells():
        logger.warning(f"Delete shell '{existing_shell.id}'")
        wrapper.delete_asset_administration_shell_by_id(existing_shell.id)

    for existing_submodel in wrapper.get_all_submodels():
        logger.warning(f"Delete submodel '{existing_submodel.id}'")
        wrapper.delete_submodel_by_id(existing_submodel.id)

    wrapper.post_asset_administration_shell(aas)
    wrapper.post_submodel(submodel)

    tmp = wrapper.get_asset_administration_shell_by_id_reference_aas_repository(aas.id)

    shell = wrapper.get_asset_administration_shell_by_id(aas.id)
    submodel = wrapper.get_submodel_by_id(submodel.id)

    wrapper.post_submodel_element_submodel_repo(submodel.id, sme)

    submodel = wrapper.get_submodel_by_id(submodel.id)

    for existing_shell in wrapper.get_all_asset_administration_shells():
        logger.warning(f"Delete shell '{existing_shell.id}'")
        wrapper.delete_asset_administration_shell_by_id(existing_shell.id)

    for existing_submodel in wrapper.get_all_submodels():
        logger.warning(f"Delete submodel '{existing_submodel.id}'")
        wrapper.delete_submodel_by_id(existing_submodel.id)


def _create_client(config: Path) -> aas_client.AasHttpClient:
    """Create a HTTP client from a given configuration file.

    :param config: Given configuration file
    :return: HTTP client
    """
    try:
        file = config
        client = aas_client.create_client_by_config(file, password="")

    except Exception as e:
        logger.error(f"Failed to create client for {file}: {e}")

    return client


def _create_sdk_wrapper(config: Path) -> sdk_wrapper.SdkWrapper:
    """Create a SDK wrapper from a given configuration file.

    :param config: Given configuration file
    :return: SDK wrapper
    """
    try:
        file = config
        client = sdk_wrapper.create_wrapper_by_config(file, basic_auth_password="")

    except Exception as e:
        logger.error(f"Failed to create client for {file}: {e}")

    return client
