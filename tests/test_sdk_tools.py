from basyx.aas import model
from aas_http_client.utilities import encoder
import aas_http_client.utilities.model_builder as model_builder
import aas_http_client.utilities.sdk_tools as sdk_tools
import pytest

SM_ID = "fluid40/sm_sdk_tools_unit_tests"
SHELL_ID = "fluid40/aas_sdk_tools_unit_tests"

@pytest.fixture(scope="module")
def shared_sm() -> model.Submodel:
    # create a Submodel
    return model_builder.create_base_submodel(identifier=SM_ID, id_short="sm_http_client_unit_tests", display_name="Submodel HTTP Client Unit Tests", description="This is a sample Submodel created for unit testing of the AAS HTTP Client.")

@pytest.fixture(scope="module")
def shared_sm_temp() -> model.Submodel:
    # create a Submodel
    return model_builder.create_base_submodel(identifier=f"{SM_ID}_temp", id_short="sm_http_client_unit_tests", display_name="Submodel HTTP Client Unit Tests", description="This is a sample Submodel created for unit testing of the AAS HTTP Client.")

@pytest.fixture(scope="module")
def shared_sme() -> model.SubmodelElement:
    # create a Submodel
    return model_builder.create_base_submodel_element_property(id_short="sme_http_client_unit_tests", type=model.datatypes.String, value="This is a sample SubmodelElement created for unit testing of the AAS HTTP Client.", display_name="SubmodelElement HTTP Client Unit Tests", description="This is a sample SubmodelElement created for unit testing of the AAS HTTP Client.")

@pytest.fixture(scope="module")
def shared_sme_collection() -> model.SubmodelElementCollection:
    # create a Submodel
    return model_builder.create_base_submodel_element_collection(id_short="sme_collection_http_client_unit_tests", value=[], display_name="SubmodelElementCollection HTTP Client Unit Tests", description="This is a sample SubmodelElementCollection created for unit testing of the AAS HTTP Client.")

@pytest.fixture(scope="module")
def shared_aas() -> model.AssetAdministrationShell:
    # create an AAS
    aas = model_builder.create_base_aas(identifier=SHELL_ID, id_short="aas_http_client_unit_tests", global_asset_identifier=SHELL_ID, display_name="AAS HTTP Client Unit Tests", description="This is a sample AAS created for unit testing of the AAS HTTP Client.")
    return aas

def test_001a_add_sm_to_shell(shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    assert len(shared_aas.submodel) == 0

    result = sdk_tools.add_submodel_to_aas(shared_aas, shared_sm)
    assert result is True
    assert len(shared_aas.submodel) == 1

    assert shared_sm.id in sdk_tools.get_submodel_ids(shared_aas)


def test_001b_add_sm_to_shell(shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    assert len(shared_aas.submodel) == 1

    result = sdk_tools.add_submodel_to_aas(shared_aas, shared_sm)
    assert result is False
    assert len(shared_aas.submodel) == 1

def test_002a_remove_sm_from_shell(shared_aas: model.AssetAdministrationShell, shared_sm_temp: model.Submodel):
    assert len(shared_aas.submodel) == 1

    result = sdk_tools.remove_submodel_from_aas(shared_aas, shared_sm_temp)
    assert result is False
    assert len(shared_aas.submodel) == 1

def test_002b_remove_sm_from_shell(shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    assert len(shared_aas.submodel) == 1

    result = sdk_tools.remove_submodel_from_aas(shared_aas, shared_sm)
    assert result is True
    assert len(shared_aas.submodel) == 0

def test_003_get_submodel_ids(shared_aas: model.AssetAdministrationShell, shared_sm: model.Submodel):
    # Add the Submodel to the AAS
    sdk_tools.add_submodel_to_aas(shared_aas, shared_sm)

    # Get the submodel IDs
    submodel_ids = sdk_tools.get_submodel_ids(shared_aas)

    # Check that the ID of the added Submodel is in the list of submodel IDs
    assert shared_sm.id in submodel_ids

    # Clean up by removing the Submodel from the AAS
    sdk_tools.remove_submodel_from_aas(shared_aas, shared_sm)

def test_004a_convert_to_dict(shared_aas: model.AssetAdministrationShell):
    # Convert the AAS to a dictionary
    aas_dict = sdk_tools.convert_to_dict(shared_aas)

    # Check that the result is a dictionary
    assert isinstance(aas_dict, dict)

    # Check that the dictionary contains expected keys
    assert "id" in aas_dict
    assert "idShort" in aas_dict
    assert "modelType" in aas_dict
    assert aas_dict["modelType"] == "AssetAdministrationShell"

def test_004b_convert_to_dict(shared_sm: model.Submodel):
    # Convert the Submodel to a dictionary
    sm_dict = sdk_tools.convert_to_dict(shared_sm)

    # Check that the result is a dictionary
    assert isinstance(sm_dict, dict)

    # Check that the dictionary contains expected keys
    assert "id" in sm_dict
    assert "idShort" in sm_dict
    assert "modelType" in sm_dict
    assert sm_dict["modelType"]== "Submodel"

def test_004c_convert_to_dict():
    # Convert an empty dictionary
    result = sdk_tools.convert_to_dict(None)

    # Check that the result is None
    assert result is None


def test_005a_convert_to_object(shared_aas: model.AssetAdministrationShell):
    # Convert None
    aas_dict = sdk_tools.convert_to_dict(shared_aas)

    assert aas_dict is not None
    assert isinstance(aas_dict, dict)

    result = sdk_tools.convert_to_object(aas_dict)

    # Check that the result is an AssetAdministrationShell object
    assert isinstance(result, model.AssetAdministrationShell)

def test_005b_convert_to_object(shared_sm: model.Submodel):
    # Convert None
    sm_dict = sdk_tools.convert_to_dict(shared_sm)

    assert sm_dict is not None
    assert isinstance(sm_dict, dict)

    result = sdk_tools.convert_to_object(sm_dict)

    # Check that the result is a Submodel object
    assert isinstance(result, model.Submodel)

def test_005c_convert_to_object():
    # Convert None
    result = sdk_tools.convert_to_object({})

    # Check that the result is None
    assert result is None

def test_006a_copy(shared_aas: model.AssetAdministrationShell):
    copied_element = sdk_tools.deep_copy(shared_aas)

    assert copied_element is not None
    assert isinstance(copied_element, model.AssetAdministrationShell)

    copied_aas: model.AssetAdministrationShell = copied_element
    assert copied_aas.id == shared_aas.id
    assert copied_aas.id_short == shared_aas.id_short

def test_006b_copy(shared_sm: model.Submodel):
    copied_element = sdk_tools.deep_copy(shared_sm)

    assert copied_element is not None
    assert isinstance(copied_element, model.Submodel)

    copied_sm: model.Submodel = copied_element
    assert copied_sm.id == shared_sm.id
    assert copied_sm.id_short == shared_sm.id_short

def test_006c_copy(shared_sme: model.SubmodelElement):
    copied_element = sdk_tools.deep_copy(shared_sme)

    assert copied_element is not None
    assert isinstance(copied_element, model.SubmodelElement)

    copied_sme: model.SubmodelElement = copied_element
    assert copied_sme.id_short == shared_sme.id_short

def test_006d_copy(shared_sme_collection: model.SubmodelElementCollection):
    copied_element = sdk_tools.deep_copy(shared_sme_collection)

    assert copied_element is not None
    assert isinstance(copied_element, model.SubmodelElementCollection)

    copied_sme_collection: model.SubmodelElementCollection = copied_element
    assert copied_sme_collection.id_short == shared_sme_collection.id_short
