"""
Module for fetching and processing data on new building plans in Hong Kong.
This module provides tools to retrieve data from public sources regarding building plans processed by the Building Authority.
"""

import csv
import io
from typing import Dict, List, Union
import requests
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the new building plan processed tool with the FastMCP server."""

    @mcp.tool(
        description="Retrieve data on the number of plans processed by the Building Authority in Hong Kong for new buildings within a specified year range."
    )
    def get_new_building_plans_processed(
        start_year: Annotated[int, Field(description="Start year for data range")],
        end_year: Annotated[int, Field(description="End year for data range")],
    ) -> List[Dict[str, Union[str, int]]]:
        return _get_new_building_plans_processed(start_year, end_year)


def fetch_building_plan_data(url: str) -> List[Dict[str, Union[str, int]]]:
    """
    Fetch building plan data from the specified URL.

    Args:
        url (str): The URL of the CSV file containing the building plan data.

    Returns:
        List[Dict[str, Union[str, int]]]: A list of dictionaries with the building plan data.
    """
    response = requests.get(url)
    response.raise_for_status()

    # Handle UTF-8 BOM
    content = response.content.decode("utf-8-sig")
    csv_reader = csv.DictReader(io.StringIO(content))
    data = [row for row in csv_reader]
    return data


def _get_new_building_plans_processed(
    start_year: int, end_year: int
) -> List[Dict[str, Union[str, int]]]:
    """
    Retrieve data on new building plans processed by the Building Authority in Hong Kong.

    Args:
        start_year (int): The starting year of the range.
        end_year (int): The ending year of the range.

    Returns:
        List[Dict[str, Union[str, int]]]: A list of dictionaries containing data on plans processed,
            including year, month, first submission & major revision, re-submission, and total.

    Note:
        - Plans refer to any plans submitted to the Building Authority for approval in respect of building works.
        - Re-submission refers to all types of plan submission which, having been previously submitted, are submitted again for approval.
        - Data source: Buildings Department
    """
    url = "https://static.data.gov.hk/bd/opendata/monthlydigests/Md11.csv"
    data = fetch_building_plan_data(url)

    # Filter data based on the year range
    filtered_data = [row for row in data if start_year <= int(row["Year"]) <= end_year]

    return filtered_data
