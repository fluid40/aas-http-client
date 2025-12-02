"""Main process for the demo."""

import json
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
    client = aas_client.create_client_by_url(base_url="http://javaaasserver:8075", encoded_ids=False)
    client_shell_reg = aas_client.create_client_by_url(base_url="http://aas-registry:8080", encoded_ids=False)

    sm = model_builder.create_base_submodel("TestSubmodel", "TestSM")
    shell = model_builder.create_base_ass("TestAAS", "TestAAS")
    sdk_tools.add_submodel_to_aas(shell, sm)

    client.shell.delete_asset_administration_shell_by_id(shell.id)
    client.submodel.delete_submodel_by_id(sm.id)

    shell_data = sdk_tools.convert_to_dict(shell)
    sm_data = sdk_tools.convert_to_dict(sm)

    result = client.submodel.post_submodel(sm_data)
    result = client.shell.post_asset_administration_shell(shell_data)

    desc = client_shell_reg.shell_registry.get_all_asset_administration_shell_descriptors()

    print("Get all AAS Descriptors from Shell Registry:")
