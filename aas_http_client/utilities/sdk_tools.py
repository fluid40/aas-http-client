"""Utility functions for working with the BaSyx SDK framework objects."""

import json
import logging
from typing import Any

import basyx.aas.adapter.json
from basyx.aas import model

_logger = logging.getLogger(__name__)


def get_submodel_ids(shell: model.AssetAdministrationShell) -> list[str]:
    """Get all IDs from the submodels referenced in the given AAS.

    :param shell: The Asset Administration Shell to extract submodel IDs from.
    :return: A list of submodel IDs referenced in the AAS.
    """
    submodel_ids = []
    for submodel in shell.submodel:
        if len(submodel.key) < 1 or submodel.key[0].type != model.KeyTypes.SUBMODEL:
            _logger.warning(f"Submodel reference {submodel} does not start with SUBMODEL key type.")
            continue

        submodel_ids.append(submodel.key[0].value)

    return submodel_ids


def add_submodel_to_aas(aas: model.AssetAdministrationShell, submodel: model.Submodel) -> None:
    """Add a given Submodel correctly to a provided AssetAdministrationShell.

    :param aas: provided AssetAdministrationShell to which the Submodel should be added
    :param submodel: given Submodel to add
    """
    existing_submodel_ids = get_submodel_ids(aas)
    if submodel.id in existing_submodel_ids:
        _logger.warning(f"Submodel with ID {submodel.id} is already referenced in the AAS. Skipping addition.")
        return

    aas.submodel.add(model.ModelReference.from_referable(submodel))


def remove_submodel_from_aas(aas: model.AssetAdministrationShell, submodel: model.Submodel) -> None:
    """Remove a given Submodel correctly from a provided AssetAdministrationShell.

    :param aas: provided AssetAdministrationShell from which the Submodel should be removed
    :param submodel: given Submodel to remove
    """
    existing_submodel_ids = get_submodel_ids(aas)
    if submodel.id not in existing_submodel_ids:
        _logger.warning(f"Submodel with ID {submodel.id} is not referenced in the AAS. Skipping removal.")
        return

    aas.submodel.remove(model.ModelReference.from_referable(submodel))


def convert_to_object(content: dict) -> Any | None:
    """Convert a dictionary to a BaSyx SDK framework object.

    :param content: dictionary to convert
    :return: BaSyx SDK framework object or None
    """
    if not content or len(content) == 0:
        _logger.debug("Empty content provided for conversion to object.")
        return None

    try:
        dict_string = json.dumps(content)
        return json.loads(dict_string, cls=basyx.aas.adapter.json.json_deserialization.AASFromJsonDecoder)
    except Exception as e:
        _logger.error(f"Decoding error: {e}")
        _logger.error(f"In JSON: {content}")
        return None


def convert_to_dict(object: Any) -> dict | None:
    """Convert a BaSyx SDK framework object. to a dictionary.

    :param object: BaSyx SDK framework object to convert
    :return: dictionary representation of the object or None
    """
    if not object:
        _logger.debug("Empty object provided for conversion to dictionary.")
        return None

    try:
        data_string = json.dumps(object, cls=basyx.aas.adapter.json.AASToJsonEncoder)
        model_dict = json.loads(data_string)
        return model_dict
    except Exception as e:
        _logger.error(f"Encoding error: {e}")
        _logger.error(f"In object: {object}")
        return None
