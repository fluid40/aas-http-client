"""Main process for the demo."""

import logging
from pathlib import Path

from basyx.aas import model

from aas_http_client.classes.client import aas_client as aas_client
from aas_http_client.utilities import model_builder, sdk_tools
from aas_http_client.wrapper import sdk_wrapper

logger = logging.getLogger(__name__)


def start() -> None:
    """Start the demo process."""
    # create a submodel element
    sme_short_id: str = model_builder.create_unique_short_id("poc_sme")
    sme = model_builder.create_base_submodel_element_property(sme_short_id, model.datatypes.String, "Sample Value")

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

    # client = aas_client.create_client_by_url(
    #     "http://javaaasserver:8075/",
    #     service_provider_auth_client_id="fluid40",
    #     service_provider_auth_client_secret="LdFB4jRrMMkgcVWgFkOVdDVDXtQ5os8w",
    #     service_provider_auth_token_url="https://aurora-fluid40.iqstruct-engineering.de/auth/realms/BaSyx/protocol/openid-connect/token",
    # )

    # client = aas_client.create_client_by_config(Path("./aas_http_client/demo/java_server_config.yml"))

    # tmp = get_token_by_basic_auth(
    #     "https://aurora-fluid40.iqstruct-engineering.de/auth/realms/BaSyx/protocol/openid-connect/token",
    #     "fluid40",
    #     "LdFB4jRrMMkgcVWgFkOVdDVDXtQ5os8w",
    # )

    wrapper = sdk_wrapper.create_wrapper_by_config(Path("./aas_http_client/demo/java_server_config.yml"))

    oauth = sdk_wrapper.create_wrapper_by_url(
        base_url="https://aurora-fluid40.iqstruct-engineering.de/aas-env",
        o_auth_token_url="https://aurora-fluid40.iqstruct-engineering.de/auth/realms/BaSyx/protocol/openid-connect/token",
        o_auth_client_id="workstation-1",
        o_auth_client_secret="nY0mjyECF60DGzNmQUjL81XurSl8etom",
        ssl_verify=False,
    )

    bearer_client = sdk_wrapper.create_wrapper_by_url(
        base_url="https://fluid40.imd.mw.tu-dresden.de/hack5/",
        bearer_auth_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmbHVpZDQwc3RhdHVzIjoicGFydG5lciIsInN1YiI6ImRhbmllbCIsInVzZXJOYW1lIjoiZGFuaWVsQGZsdWlkNDAuZGUiLCJzZXJ2ZXJOYW1lIjoiRkw0MC1UZXN0LUlEUCIsImRvbWFpbiI6ImZsdWlkNDAuZGUiLCJpc3MiOiJmbHVpZDQwLWlkcC50dS1kcmVzZGVuLmRlIiwiYXVkIjoiaHR0cHM6Ly9mbHVpZDQwLmltZC5tdy50dS1kcmVzZGVuLmRlL2hhY2s1IiwiZXhwIjoxNzkzNjkzODAxLCJpYXQiOjE3NjIyNDQyMDEsImp0aSI6ImRkNTU0NGM1LWUyNzktNGI2ZC04NjE2LWY4YjU3ZDA5MTc2ZSIsImNsaWVudF9pZCI6ImRhbmllbF9fZGQ1NTQ0YzUtZTI3OS00YjZkLTg2MTYtZjhiNTdkMDkxNzZlIn0.fo1e9LLlfpQ6Q_2Soymvlo4iBXvOwFI_4pu4AjFb8wX7iwsGOq6h7axYvB_Co21GZIcAbkaxD-IwvOQv22P49XffzeIAPiisNjxs5rRYZIBK1bL27pC8fC3F3EcyNayrnay-95-a3QkuPSSVL4pjXppjJlrjPSkLabvZHbWuEKWsr2pJ-lemc0dKHCI6DrYx6xgL4_Rj4QV2MK0u6uFHKOPm_GyY9RjHPU53Aca38xoIOl7egRn104YXTmaFLutXMD6PwwfbwPjX2xnzsqa_IotZ_9Z5J2hazTA3DuUtdD3nwr6vxNcJxNoHGzFWSDE44lhw9izv_FdXwYOMC-RSPw",
    )

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
