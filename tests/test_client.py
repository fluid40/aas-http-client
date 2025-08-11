import pytest
from pathlib import Path
from aas_http_client.client import create_client_by_config, AasHttpClient
from basyx.aas.model import AssetAdministrationShell, Submodel, MultiLanguageTextType
import aas_http_client.utilities.model_builder as model_builder
import json
import basyx.aas.adapter.json

@pytest.fixture(scope="module")
def client() -> AasHttpClient:
    try:
        file = Path("./tests/test_server_config.json").resolve()
        
        if not file.exists():
            raise FileNotFoundError(f"Configuration file {file} does not exist.")
        
        client = create_client_by_config(file, password="")
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    shells = client.get_shells()
    if shells is None:
        raise RuntimeError("No shells found on server. Please check the server configuration.")

    for shell in shells.get("result", []):
        id = shell.get("id", "")
        client.delete_shells_by_id(id)
        

    return client

@pytest.fixture(scope="module")
def shared_sm() -> Submodel:
    # create a Submodel
    return model_builder.create_base_submodel("sm_http_client_unit_tests")

@pytest.fixture(scope="module")
def shared_aas(client: AasHttpClient, shared_sm: Submodel) -> AssetAdministrationShell:
    # create an AAS
    aas = model_builder.create_base_ass("aas_http_client_unit_tests")

    # add Submodel to AAS
    model_builder.add_submodel_to_aas(aas, shared_sm)
    
    return aas
 
def test_001_connect(client: AasHttpClient):
    assert client is not None
    
def test_002_get_shells(client: AasHttpClient, shared_aas: AssetAdministrationShell):
    result = client.get_shells()
    assert result is not None
    shells = result.get("result", [])
    assert len(shells) == 0

def test_003_post_shells(client: AasHttpClient, shared_aas: AssetAdministrationShell):
    aas_data_string = json.dumps(shared_aas, cls=basyx.aas.adapter.json.AASToJsonEncoder)
    aas_data = json.loads(aas_data_string)
    result = client.post_shells(aas_data)
    
    assert result is not None
    result_id_short = result.get("idShort", "")
    assert result_id_short == shared_aas.id_short
    
    get_result = client.get_shells()
    assert get_result is not None
    shells = get_result.get("result", [])
    assert len(shells) == 1
    assert shells[0].get("idShort", "") == shared_aas.id_short

def test_004a_get_shell_by_id(client: AasHttpClient, shared_aas: AssetAdministrationShell):
    result = client.get_shells_by_id(shared_aas.id)
    
    assert result is not None
    assert result.get("idShort", "") == shared_aas.id_short

def test_004b_get_shell_by_id_not_found(client: AasHttpClient):
    result = client.get_shells_by_id("non_existent_id")
    
    assert result is None
    
def test_005a_update_shells(client: AasHttpClient, shared_aas: AssetAdministrationShell):
    # Update the idShort of the shared AAS

    description_text = {"en": "Updated description for unit tests"}
    shared_aas.description = MultiLanguageTextType(description_text)
    
    aas_data_string = json.dumps(shared_aas, cls=basyx.aas.adapter.json.AASToJsonEncoder)
    aas_data = json.loads(aas_data_string)
    
    result = client.put_shells(shared_aas.id, aas_data)
    
    assert result
    
    get_result = client.get_shells_by_id(shared_aas.id)
    
    assert get_result is not None
    assert get_result.get("description", {})[0].get("text", "") == "Updated description for unit tests"
    assert get_result.get("idShort", "") == shared_aas.id_short
    assert get_result.get("id", "") == shared_aas.id
    assert get_result.get("description", {})[0].get("text", "") == shared_aas.description.get("en", "")

def test_005b_update_shells_with_id(client: AasHttpClient, shared_aas: AssetAdministrationShell):
    # Update the idShort of the shared AAS

    description_text = {"en": "Updated description for unit tests"}
    shared_aas.description = MultiLanguageTextType(description_text)
    
    aas_data_string = json.dumps(shared_aas, cls=basyx.aas.adapter.json.AASToJsonEncoder)
    aas_data = json.loads(aas_data_string)
    
    aas_data["id"] = "updated_id"  # Ensure the id is included in the update
    
    result = client.put_shells(shared_aas.id, aas_data)
    
    assert result is False

def test_098_delete_shells(client: AasHttpClient, shared_aas: AssetAdministrationShell):
    result = client.delete_shells_by_id(shared_aas.id)
    
    assert result is not None
    
    get_result = client.get_shells()
    assert get_result is not None
    shells = get_result.get("result", [])
    assert len(shells) == 0