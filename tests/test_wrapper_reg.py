import pytest
from pathlib import Path
from aas_http_client.classes.wrapper.sdk_wrapper import create_wrapper_by_config, SdkWrapper, create_wrapper_by_dict, create_wrapper_by_url
from basyx.aas import model
import aas_http_client.utilities.model_builder as model_builder
import aas_http_client.utilities.sdk_tools as sdk_tools
import json
import basyx.aas.adapter.json
from urllib.parse import urlparse
import logging
from aas_http_client.demo.logging_handler import initialize_logging
from aas_http_client.utilities import encoder

logger = logging.getLogger(__name__)

JAVA_SERVER_PORTS = [8075]
PYTHON_SERVER_PORTS = [5080, 80]

SM_ID = "fluid40/sm_http_client_unit_tests"
SHELL_ID = "fluid40/aas_http_client_unit_tests"

CONFIG_FILE_ENV = "./tests/server_configs/test_java_server_config.yml"
CONFIG_FILE_AAS_REG_ENV = "./tests/server_configs/test_aas_reg_server_config.yml"

@pytest.fixture(scope="module")
def wrapper(request) -> SdkWrapper:
    try:
        initialize_logging()
        wrapper = create_wrapper_by_config(Path(CONFIG_FILE_ENV))
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    shells = wrapper.get_all_asset_administration_shells()
    if shells is None:
        raise RuntimeError("No shells found on server. Please check the server configuration.")

    return wrapper
@pytest.fixture(scope="module")
def wrapper_aas_reg(request) -> SdkWrapper:
    try:
        initialize_logging()
        wrapper = create_wrapper_by_config(Path(CONFIG_FILE_AAS_REG_ENV))
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    descriptors = wrapper.get_all_asset_administration_shell_descriptors()
    if descriptors is None:
        raise RuntimeError("No descriptors found on server. Please check the server configuration.")

    return wrapper

@pytest.fixture(scope="module")
def shared_sm() -> model.Submodel:
    # create a Submodel
    return model_builder.create_base_submodel(identifier=SM_ID, id_short="sm_http_client_unit_tests")

@pytest.fixture(scope="module")
def shared_aas(shared_sm: model.Submodel) -> model.AssetAdministrationShell:
    # create an AAS
    aas = model_builder.create_base_ass(identifier=SHELL_ID, id_short="aas_http_client_unit_tests")

    # add Submodel to AAS
    sdk_tools.add_submodel_to_aas(aas, shared_sm)

    return aas

def test_000_post_assets(wrapper: SdkWrapper, shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    sm_data = sdk_tools.convert_to_dict(shared_sm)
    sm_result = wrapper.post_submodel(sm_data)

    assert sm_result is not None

    shell_data = sdk_tools.convert_to_dict(shared_aas)
    shell_result = wrapper.post_asset_administration_shell(shell_data)
    assert shell_result is not None

def test_001_(wrapper_aas_reg: SdkWrapper):
    descriptors = wrapper_aas_reg.get_all_asset_administration_shell_descriptors()

    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 1
    assert results[0]["id"] == SHELL_ID

def test_099a_delete_assets(wrapper: SdkWrapper, shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    result = wrapper.delete_submodel_by_id(shared_sm.id)
    assert result

    submodels = wrapper.delete_asset_administration_shell_by_id(shared_aas.id)
    assert submodels
