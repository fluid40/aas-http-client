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
