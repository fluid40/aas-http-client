import logging

from basyx.aas import model

from aas_http_client.utilities.sdk_tools import convert_to_object

logger = logging.getLogger(__name__)


class PagingMetadata:
    """Class representing pagination metadata."""

    cursor: str

    def __init__(self, cursor: str) -> None:
        """Initialize a paging metadata object.

        :param cursor: Cursor for the next page
        """
        self.cursor = cursor


class ShellPaginatedData:
    """Class representing paginated data for Asset Administration Shells."""

    paging_metadata: PagingMetadata
    results: list[model.AssetAdministrationShell]

    def __init__(self, cursor: str, results: list[model.AssetAdministrationShell]) -> None:
        """Initialize a paginated data object.

        :param paging_metadata: Paging metadata
        :param results: list of results
        """
        self.paging_metadata = PagingMetadata(cursor)
        self.results = results


def create_shell_paging_data(content: dict) -> ShellPaginatedData:
    """Create a ShellPaginatedData object from a dictionary.

    :param content: Dictionary containing paginated shell data
    :return: ShellPaginatedData object
    """
    aas_list: list[model.AssetAdministrationShell] = []

    results: list = content.get("result", [])
    if not results or len(results) == 0:
        logger.warning("No shells found on server.")
        return ShellPaginatedData(cursor="", results=[])

    for result in results:
        if not isinstance(result, dict):
            logger.error(f"Invalid shell data: {result}")
            return None

        aas = convert_to_object(result)

        if aas:
            aas_list.append(aas)

    cursor = ""
    paging_metadata_dict = content.get("paging_metadata", {})

    if "cursor" in paging_metadata_dict:
        cursor = paging_metadata_dict["cursor"]

    return ShellPaginatedData(
        cursor=cursor,
        results=aas_list,
    )
