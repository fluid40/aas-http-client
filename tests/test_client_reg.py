import pytest
from pathlib import Path
from aas_http_client.classes.client.aas_client import create_client_by_config, AasHttpClient
from basyx.aas import model
from aas_http_client.utilities import sdk_tools, model_builder
import logging
from aas_http_client.demo.logging_handler import initialize_logging

logger = logging.getLogger(__name__)

JAVA_SERVER_PORTS = [8075]
PYTHON_SERVER_PORTS = [5080, 80]

SM_ID = "fluid40/sm_http_client_unit_tests"
SHELL_ID = "fluid40/aas_http_client_unit_tests"

CONFIG_FILE_ENV = "./tests/server_configs/test_java_server_config.yml"
CONFIG_FILE_AAS_REG_ENV = "./tests/server_configs/test_aas_reg_server_config.yml"
CONFIG_FILE_SM_REG_ENV = "./tests/server_configs/test_sm_reg_server_config.yml"

shared_shell_descriptor = {}
shared_sm_descriptor = {}

@pytest.fixture(scope="module")
def client(request) -> AasHttpClient:
    try:
        initialize_logging()
        client = create_client_by_config(Path(CONFIG_FILE_ENV))
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    shells = client.shell.get_all_asset_administration_shells()
    if shells is None:
        raise RuntimeError("No shells found on server. Please check the server configuration.")

    return client

@pytest.fixture(scope="module")
def client_aas_reg(request) -> AasHttpClient:
    try:
        initialize_logging()
        client = create_client_by_config(Path(CONFIG_FILE_AAS_REG_ENV))
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    descriptors = client.shell_registry.get_all_asset_administration_shell_descriptors()
    if descriptors is None:
        raise RuntimeError("No descriptors found on server. Please check the server configuration.")

    return client

@pytest.fixture(scope="module")
def client_sm_reg(request) -> AasHttpClient:
    try:
        initialize_logging()
        client = create_client_by_config(Path(CONFIG_FILE_SM_REG_ENV))
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    descriptors = client.submodel_registry.get_all_submodel_descriptors()
    if descriptors is None:
        raise RuntimeError("No descriptors found on server. Please check the server configuration.")

    return client

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

@pytest.fixture(scope="module")
def global_shell_descriptor():
    return shared_shell_descriptor

@pytest.fixture(scope="module")
def global_sm_descriptor():
    return shared_sm_descriptor

def test_000a_clean_server(client: AasHttpClient, client_aas_reg: AasHttpClient, client_sm_reg: AasHttpClient):
    shells_result = client.shell.get_all_asset_administration_shells()

    for shell in shells_result.get("result", []):
        client.shell.delete_asset_administration_shell_by_id(shell["id"])

    submodels_result = client.submodel.get_all_submodels()
    for submodel in submodels_result.get("result", []):
        client.submodel.delete_submodel_by_id(submodel["id"])

    client_aas_reg.shell_registry.delete_all_asset_administration_shell_descriptors()
    client_sm_reg.submodel_registry.delete_all_submodel_descriptors()

    shells_result = client.shell.get_all_asset_administration_shells()
    assert len(shells_result.get("result")) == 0
    submodels_result = client.submodel.get_all_submodels()
    assert len(submodels_result.get("result")) == 0
    shell_descriptors_result = client_aas_reg.shell_registry.get_all_asset_administration_shell_descriptors()
    assert len(shell_descriptors_result.get("result")) == 0
    sm_descriptors_result = client_sm_reg.submodel_registry.get_all_submodel_descriptors()
    assert len(sm_descriptors_result.get("result")) == 0

def test_000b_post_assets(client: AasHttpClient, shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    sm_data = sdk_tools.convert_to_dict(shared_sm)
    sm_result = client.submodel.post_submodel(sm_data)

    assert sm_result is not None

    shell_data = sdk_tools.convert_to_dict(shared_aas)
    shell_result = client.shell.post_asset_administration_shell(shell_data)
    assert shell_result is not None

def test_001a_get_self_description_shell(client_aas_reg: AasHttpClient):
    description = client_aas_reg.shell_registry.get_self_description()

    assert description is not None
    assert "profiles" in description
    assert len(description["profiles"]) == 1

def test_001b_get_self_description_sm(client_sm_reg: AasHttpClient):
    description = client_sm_reg.submodel_registry.get_self_description()

    assert description is not None
    assert "profiles" in description
    assert len(description["profiles"]) == 1

def test_002_search(client_aas_reg: AasHttpClient):
    request_body = {
        "page": {
            "index": 0,
            "size": 1
        },
        "sortBy": {
            "direction": "ASC",
            "path": [
            "idShort"
            ]
        }
    }

    search_result = client_aas_reg.shell_registry.search(request_body)

    assert search_result is not None
    assert "total" in search_result
    total = search_result["total"]
    assert total == 1
    assert "hits" in search_result
    hits = search_result["hits"]
    assert hits is not None
    assert len(hits) == 1
    assert hits[0]["id"] == SHELL_ID

def test_003_get_all_asset_administration_shell_descriptors(client_aas_reg: AasHttpClient):
    descriptors = client_aas_reg.shell_registry.get_all_asset_administration_shell_descriptors()

    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 1
    assert results[0]["id"] == SHELL_ID

    global shared_shell_descriptor
    shared_shell_descriptor.clear()
    shared_shell_descriptor.update(results[0])

def test_004_get_all_submodel_descriptors(client_sm_reg: AasHttpClient):
    descriptors = client_sm_reg.submodel_registry.get_all_submodel_descriptors()

    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 1
    assert results[0]["id"] == SM_ID

    global shared_sm_descriptor
    shared_sm_descriptor.clear()
    shared_sm_descriptor.update(results[0])

def test_005_delete_assets(client: AasHttpClient, client_aas_reg: AasHttpClient, client_sm_reg: AasHttpClient, shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    result = client.submodel.delete_submodel_by_id(shared_sm.id)
    assert result

    submodels = client.shell.delete_asset_administration_shell_by_id(shared_aas.id)
    assert submodels

    shells_result = client.shell.get_all_asset_administration_shells()
    assert len(shells_result.get("result")) == 0
    submodels_result = client.submodel.get_all_submodels()
    assert len(submodels_result.get("result")) == 0
    shell_descriptors_result = client_aas_reg.shell_registry.get_all_asset_administration_shell_descriptors()
    assert len(shell_descriptors_result.get("result")) == 0
    sm_descriptors_result = client_sm_reg.submodel_registry.get_all_submodel_descriptors()
    assert len(sm_descriptors_result.get("result")) == 0

def test_006_post_asset_administration_shell_descriptor(client_aas_reg: AasHttpClient, global_shell_descriptor):
    result = client_aas_reg.shell_registry.post_asset_administration_shell_descriptor(global_shell_descriptor)

    assert result is not None
    assert "id" in result
    assert result["id"] == SHELL_ID

    descriptors = client_aas_reg.shell_registry.get_all_asset_administration_shell_descriptors()
    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 1
    assert results[0]["id"] == SHELL_ID

def test_007_delete_all_asset_administration_shell_descriptors(client_aas_reg: AasHttpClient):
    result = client_aas_reg.shell_registry.delete_all_asset_administration_shell_descriptors()
    assert result

    descriptors = client_aas_reg.shell_registry.get_all_asset_administration_shell_descriptors()
    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 0

def test_008_post_submodel_descriptor(client_sm_reg: AasHttpClient, global_sm_descriptor):
    result = client_sm_reg.submodel_registry.post_submodel_descriptor(global_sm_descriptor)

    assert result is not None
    assert "id" in result
    assert result["id"] == SM_ID

    descriptors = client_sm_reg.submodel_registry.get_all_submodel_descriptors()
    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 1
    assert results[0]["id"] == SM_ID

def test_009_delete_all_submodel_descriptors(client_sm_reg: AasHttpClient):
    result = client_sm_reg.submodel_registry.delete_all_submodel_descriptors()
    assert result

    descriptors = client_sm_reg.submodel_registry.get_all_submodel_descriptors()
    assert descriptors is not None
    assert "result" in descriptors
    results = descriptors["result"]
    assert results is not None
    assert len(results) == 0
