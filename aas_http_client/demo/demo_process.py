"""Main process for the demo."""

import logging
from pathlib import Path

from basyx.aas import model

from aas_http_client.classes.client import aas_client
from aas_http_client.classes.wrapper import sdk_wrapper
from aas_http_client.utilities import encoder, model_builder, sdk_tools

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

    wrapper = sdk_wrapper.create_wrapper_by_config(Path("./aas_http_client/demo/java_server_config.yml"))
    client = wrapper.get_client()

    all_shells = wrapper.get_all_asset_administration_shells()
    for existing_shell in all_shells.results:
        logger.warning(f"Delete shell '{existing_shell.id}'")
        wrapper.delete_asset_administration_shell_by_id(existing_shell.id)

    for existing_submodel in wrapper.get_all_submodels():
        logger.warning(f"Delete submodel '{existing_submodel.id}'")
        wrapper.delete_submodel_by_id(existing_submodel.id)

    # create an AAS
    aas1 = model_builder.create_base_ass("poc_aas1", "poc_aas1")
    wrapper.post_asset_administration_shell(aas1)

    aas2 = model_builder.create_base_ass("poc_aas2", "poc_aas2")
    wrapper.post_asset_administration_shell(aas2)

    aas3 = model_builder.create_base_ass("poc_aas3", "poc_aas3")
    wrapper.post_asset_administration_shell(aas3)

    decoded_id = encoder.decode_base_64(aas3.id)
    encoded_id = encoder.encode_base_64(decoded_id)

    identifier = {"identifier": f"{decoded_id}", "encodedIdentifier": f"{encoded_id}"}
    shells = client.get_all_asset_administration_shells(asset_ids=None, id_short=aas3.id_short, limit=2, cursor="")

    shells = client.get_all_asset_administration_shells(asset_ids=None, id_short="", limit=2, cursor="")

    cursor = shells.get("paging_metadata").get("cursor")

    shells = client.get_all_asset_administration_shells(asset_ids=None, id_short="", limit=2, cursor=cursor)

    shells = wrapper.get_all_asset_administration_shells(limit=2)

    python_wrapper = sdk_wrapper.create_wrapper_by_url("http://pythonaasserver:80/")
    python_wrapper.post_asset_administration_shell(aas3)
    tmp = python_wrapper.get_asset_administration_shell_by_id_reference_aas_repository(aas3.id)

    sm1 = model_builder.create_base_submodel("poc_sm1", "poc_sm1")
    wrapper.post_submodel(sm1)
    sm2 = model_builder.create_base_submodel("poc_sm2", "poc_sm2")
    wrapper.post_submodel(sm2)
    sm3 = model_builder.create_base_submodel("poc_sm3", "poc_sm3")
    wrapper.post_submodel(sm3)

    sms = client.get_all_submodels(id_short="poc_sm1", limit=2, cursor="", level="core")

    sms = client.get_all_submodels(limit=2)

    print(sms)

    cursor = sms.get("paging_metadata").get("cursor")

    sms = client.get_all_submodels(limit=2, cursor=cursor)

    for existing_shell in wrapper.get_all_asset_administration_shells():
        logger.warning(f"Delete shell '{existing_shell.id}'")
        wrapper.delete_asset_administration_shell_by_id(existing_shell.id)

    for existing_submodel in wrapper.get_all_submodels():
        logger.warning(f"Delete submodel '{existing_submodel.id}'")
        wrapper.delete_submodel_by_id(existing_submodel.id)
