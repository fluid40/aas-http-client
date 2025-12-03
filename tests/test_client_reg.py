import pytest
from pathlib import Path
from aas_http_client.classes.client.aas_client import create_client_by_config, AasHttpClient, create_client_by_dict, create_client_by_url
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

AIMC_SM_ID = "https://fluid40.de/ids/sm/7644_4034_2556_2369"
SM_ID = "fluid40/sm_http_client_unit_tests"
SHELL_ID = "fluid40/aas_http_client_unit_tests"

CONFIG_FILE_ENV = "./tests/server_configs/test_java_server_config.yml"
CONFIG_FILE_AAS_REG_ENV = "./tests/server_configs/test_aas_reg_server_config.yml"

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

def test_(client: AasHttpClient, client_aas_reg):
    result = client.submodel.get_all_submodels()
    result_reg = client_aas_reg.shell_registry.get_all_asset_administration_shell_descriptors()
    assert result is not None
    assert result_reg is not None
