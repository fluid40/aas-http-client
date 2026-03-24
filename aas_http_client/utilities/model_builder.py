"""Model builder module.

Provides some helper methods for easier work with basyx sdk data model
"""

import json
import logging
import uuid
from pathlib import Path
from typing import Any

from basyx.aas import model

from aas_http_client.utilities import sdk_tools

logger = logging.getLogger(__name__)


def create_unique_short_id(id_short: str) -> str:
    """Generate a unique identifier string by appending a UUID to the provided ID short.

    :param id_short: provided ID short
    :return: unique identifier
    """
    return f"{id_short}_{str(uuid.uuid4()).replace('-', '_')}"


def create_submodel_from_file(json_file: str = "") -> model.Submodel:
    """Creates a submodel from a JSON file file.

    :param id: ID of the submodel. If empty, the template's ID is used

    """
    # Define the path to the submodel template file
    sm_template_file = Path(json_file).resolve()

    # Check if the template file exists
    if not sm_template_file.exists():
        raise FileNotFoundError(f"Submodel template file not found: {sm_template_file}")

    submodel_data = {}
    try:
        # Load the template JSON file
        with Path.open(sm_template_file, "r", encoding="utf-8") as f:
            submodel_data = json.load(f)

        # Load the template JSON into a Submodel object
        submodel = sdk_tools.convert_to_object(submodel_data)

        # Ensure the loaded template is indeed a Submodel
        if not isinstance(submodel, model.Submodel):
            raise TypeError("Loaded template JSON structure is not a Submodel.")

    except Exception as e:
        logger.error(f"Error loading submodel template: {e}")
        raise e

    return submodel


def create_base_submodel_element_property(
    id_short: str | None, type: model.datatypes, value: Any, display_name: str = "", description: str = ""
) -> model.Property:
    """Create a basic SubmodelElement of type Property."""
    sme = model.Property(id_short=id_short, value_type=type, value=value)

    if not description:
        description = f"This is the submodel element with ID short '{id_short}'"

    description_text = {"en": f"{description}"}
    sme.description = model.MultiLanguageTextType(description_text)

    if not display_name:
        display_name = "POC Submodel Element"

    display_name_text = {"en": f"{display_name}"}
    sme.display_name = model.MultiLanguageNameType(display_name_text)

    return sme


def create_base_submodel_element_collection(
    id_short: str, value: list[model.SubmodelElement], display_name: str = "", description: str = ""
) -> model.SubmodelElementCollection:
    """Create a basic SubmodelElement of type SubmodelElementCollection."""
    sme = model.SubmodelElementCollection(id_short=id_short, value=value)

    if not description:
        description = f"This is the submodel element with ID short '{id_short}'"

    description_text = {"en": f"{description}"}
    sme.description = model.MultiLanguageTextType(description_text)

    if not display_name:
        display_name = "POC Submodel Element"

    display_name_text = {"en": f"{display_name}"}
    sme.display_name = model.MultiLanguageNameType(display_name_text)

    return sme


def create_base_submodel(identifier: str, id_short: str, display_name: str = "", description: str = "") -> model.Submodel:
    """Create a basic Submodel.

    :param identifier: identifier of the Submodel
    :param id_short: ID short of the Submodel
    :param display_name: display name of the Submodel, defaults to ""
    :param description: description of the Submodel, defaults to ""
    :return: Submodel instance
    """
    sm = model.Submodel(identifier)
    sm.id_short = id_short

    if not description:
        description = f"This is the submodel with ID short '{id_short}'"

    description_text = {"en": f"{description}"}
    sm.description = model.MultiLanguageTextType(description_text)

    if not display_name:
        display_name = "POC AAS"

    display_name_text = {"en": f"{display_name}"}
    sm.display_name = model.MultiLanguageNameType(display_name_text)

    return sm


def create_base_aas(
    identifier: str, id_short: str, global_asset_identifier: str = "", display_name: str = "", description: str = ""
) -> model.AssetAdministrationShell:
    """Create a basic AAS.

    :param identifier: identifier of the AAS
    :param id_short: ID short of the AAS
    :param global_asset_identifier: identifier of the global Asset
    :param display_name: display name of the AAS, defaults to ""
    :param description: description of the AAS, defaults to ""
    :return: AssetAdministrationShell instance
    """
    if not global_asset_identifier:
        global_asset_identifier = identifier

    asset_info = create_base_asset_information(global_asset_identifier)

    aas = model.AssetAdministrationShell(id_=identifier, asset_information=asset_info)
    aas.id_short = id_short

    if not description:
        description = f"This is the asset administration shell with ID short '{id_short}'"

    description_text = {"en": f"{description}"}
    aas.description = model.MultiLanguageTextType(description_text)

    if not display_name:
        display_name = "POC AAS"

    display_name_text = {"en": f"{display_name}"}
    aas.display_name = model.MultiLanguageNameType(display_name_text)

    return aas


def create_base_asset_information(identifier: str) -> model.AssetInformation:
    """Return a basic AssetInformation instance.

    :param id_short: short ID of the AssetInformation
    :param namespace: namespace of the AssetInformation, defaults to "basyx_python_aas_server"
    :return: AssetInformation instance
    """
    return model.AssetInformation(model.AssetKind.INSTANCE, identifier)


def create_reference(id: str) -> model.ModelReference:
    """Create a ModelReference.

    :param id: ID of the Submodel to reference
    :return: ModelReference instance
    """
    return model.ModelReference.from_referable(model.Submodel(id))
