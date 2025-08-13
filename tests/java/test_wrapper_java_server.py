import pytest
from pathlib import Path
from aas_http_client.wrapper.sdk_wrapper import create_wrapper_by_config, SdkWrapper  
from basyx.aas.model import AssetAdministrationShell, Submodel, MultiLanguageTextType
import aas_http_client.utilities.model_builder as model_builder

@pytest.fixture(scope="module")
def wrapper() -> SdkWrapper:
    try:
        file = Path("./tests/server_configs/test_java_server_config.json").resolve()
        
        if not file.exists():
            raise FileNotFoundError(f"Configuration file {file} does not exist.")
        
        client = create_wrapper_by_config(file, password="")
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    shells = client.get_shells()
    if shells is None:
        raise RuntimeError("No shells found on server. Please check the server configuration.")    

    return client

@pytest.fixture(scope="module")
def shared_sm() -> Submodel:
    # create a Submodel
    submodel = model_builder.create_base_submodel("sm_http_client_unit_tests", "")
    submodel.category = "Unit Test"
    return submodel

@pytest.fixture(scope="module")
def shared_aas(shared_sm: Submodel) -> AssetAdministrationShell:
    # create an AAS
    aas = model_builder.create_base_ass(id_short="aas_http_client_unit_tests", namespace="")

    # add Submodel to AAS
    model_builder.add_submodel_to_aas(aas, shared_sm)
    
    return aas
 
def test_001_connect(wrapper: SdkWrapper):
    assert wrapper is not None
    
def test_002_get_shells(wrapper: SdkWrapper):
    shells = wrapper.get_shells()
    assert shells is not None
    assert len(shells) == 0

def test_003_post_shells(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell):
    result = wrapper.post_shells(shared_aas)
    
    assert result is not None
    result_id_short = result.get("idShort", "")
    assert result_id_short == shared_aas.id_short
    
    shells = wrapper.get_shells()
    assert shells is not None
    assert len(shells) == 1
    assert shells[0].id_short == shared_aas.id_short
    assert shells[0].id == shared_aas.id
    
def test_004a_get_shell_by_id(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell):
    shell = wrapper.get_shells_by_id(shared_aas.id)
    
    assert shell is not None
    assert shell.id_short == shared_aas.id_short
    assert shell.id == shared_aas.id

def test_004b_get_shell_by_id_not_found(wrapper: SdkWrapper):
    shell = wrapper.get_shells_by_id("non_existent_id")
    
    assert shell is None
    
def test_005a_put_shells(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell):
    aas = AssetAdministrationShell(id_=shared_aas.asset_information.global_asset_id, asset_information=shared_aas.asset_information)
    aas.id_short = shared_aas.id_short

    description_text = "Put description for unit tests"
    aas.description = MultiLanguageTextType({"en": description_text})
    aas.submodel = shared_aas.submodel  # Keep existing submodels
    
    result = wrapper.put_shells(shared_aas.id, aas)
    
    assert result
    
    shell = wrapper.get_shells_by_id(shared_aas.id)
    
    assert shell is not None
    assert shell.id_short == shared_aas.id_short
    assert shell.id == shared_aas.id
    # description must have changed
    assert shell.description.get("en", "") == description_text
    assert shell.description.get("en", "") != shared_aas.description.get("en", "")
    # submodels must be retained
    assert len(shell.submodel) == len(shared_aas.submodel)
    
    # The display name must be empty 
    assert shell.display_name is None

def test_005b_put_shells_with_id(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell):
    # put with other ID
    id_short = "put_short_id"
    asset_info = model_builder.create_base_asset_information(id_short)
    aas = AssetAdministrationShell(id_=asset_info.global_asset_id, asset_information=asset_info)
    aas.id_short = id_short

    description_text = {"en": "Updated description for unit tests"}
    aas.description = MultiLanguageTextType(description_text)

    result = wrapper.put_shells(shared_aas.id, aas)
    
    assert not result

def test_006_get_shells_reference_by_id(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell):
    reference = wrapper.get_shells_reference_by_id(shared_aas.id)

    # Basyx java server do not provide this endpoint. But works because of workaround in wrapper
    assert reference is not None
    assert len(reference.key) == 1
    assert reference.key[0].value == shared_aas.id

def test_007_get_shells_submodels_by_id_not_posted(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell, shared_sm: Submodel):
    submodel = wrapper.get_shells_submodels_by_id(shared_aas.id, shared_sm.id)

    assert submodel is None
    
def test_008_get_submodels(wrapper: SdkWrapper):
    submodels = wrapper.get_submodels()
    assert submodels is not None
    assert len(submodels) == 0
    
def test_009_post_submodels(wrapper: SdkWrapper, shared_sm: Submodel):   
    result = wrapper.post_submodels(shared_sm)

    assert result
    
    submodels = wrapper.get_submodels()
    assert submodels is not None
    assert len(submodels) == 1
    assert submodels[0].id_short == shared_sm.id_short
    assert submodels[0].id == shared_sm.id

def test_010_get_shells_submodels_by_id(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell, shared_sm: Submodel):
    submodel = wrapper.get_shells_submodels_by_id(shared_aas.id, shared_sm.id)
    
    # Basyx java server do not provide this endpoint
    assert submodel is None
    
def test_011a_get_submodels_by_id(wrapper: SdkWrapper, shared_sm: Submodel):
    submodel = wrapper.get_submodels_by_id(shared_sm.id)

    assert submodel is not None
    assert submodel.id_short == shared_sm.id_short
    assert submodel.id == shared_sm.id
    
def test_011b_get_submodels_by_id_not_found(wrapper: SdkWrapper):
    result = wrapper.get_submodels_by_id("non_existent_id")

    assert result is None
 
def test_012_patch_submodel_by_id(wrapper: SdkWrapper, shared_sm: Submodel):
    sm = Submodel(shared_sm.id_short)
    sm.id_short = shared_sm.id_short

    description_text = "Patched description for unit tests"
    sm.description = MultiLanguageTextType({"en": description_text})

    result = wrapper.patch_submodel_by_id(shared_sm.id, sm)

    # Basyx java server do not provide this endpoint
    assert not result
        
def test_013_put_shells_submodels_by_id(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell, shared_sm: Submodel):
    sm = Submodel(shared_sm.id_short)
    sm.id_short = shared_sm.id_short

    description_text = "Put via shell description for unit tests"
    sm.description = MultiLanguageTextType({"en": description_text})

    result = wrapper.put_shells_submodels_by_id(shared_aas.id, shared_sm.id, sm)
    
    # Basyx java server do not provide this endpoint
    assert not result # Restore original submodel
            
def test_014_put_submodels_by_id(wrapper: SdkWrapper, shared_sm: Submodel):
    sm = Submodel(shared_sm.id_short)
    sm.id_short = shared_sm.id_short

    description_text = "Put description for unit tests"
    sm.description = MultiLanguageTextType({"en": description_text})

    result = wrapper.put_submodels_by_id(shared_sm.id, sm)

    assert result
    
    submodel = wrapper.get_submodels_by_id(shared_sm.id)
    assert submodel is not None
    assert submodel.id_short == shared_sm.id_short
    assert submodel.id == shared_sm.id
    # description must have changed
    assert submodel.description.get("en", "") == description_text
    assert submodel.description.get("en", "") != shared_sm.description.get("en", "")
    # display name stays
    assert submodel.display_name is None
    # category was not set an must be empty
    assert submodel.category is None
    assert len(submodel.submodel_element) == 0
    
    # restore to its original state
    wrapper.put_submodels_by_id(shared_sm.id, shared_sm)  # Restore original submodel         
            
def test_098_delete_shells_by_id(wrapper: SdkWrapper, shared_aas: AssetAdministrationShell):
    result = wrapper.delete_shells_by_id(shared_aas.id)
    
    assert result
    
    shells = wrapper.get_shells()
    assert shells is not None
    assert len(shells) == 0
        
def test_099_delete_submodel_by_id(wrapper: SdkWrapper, shared_sm: Submodel):
    result = wrapper.delete_submodels_by_id(shared_sm.id)
    
    assert result
    
    submodels = wrapper.get_submodels()
    assert submodels is not None
    assert len(submodels) == 0