"""
Module for testing the new building plan processed tool.

This module contains unit tests for fetching and filtering new building plan data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_development_mcp_server.tools.new_building_plan_processed import (
    _get_new_building_plans_processed,
)
from hkopenai.hk_development_mcp_server.tools.new_building_plan_processed import (
    register,
)


class TestNewBuildingPlanProcessed(unittest.TestCase):
    """
    Test class for verifying new building plan processed functionality.

    This class contains test cases to ensure the data fetching and filtering
    for new building plan processed data work as expected.
    """

    def test_get_new_building_plans_processed(self):
        """
        Test the retrieval and filtering of new building plan processed data.

        This test verifies that the function correctly filters data by year range,
        returns empty results for non-matching years, and handles partial year matches.
        """

        with patch(
            "hkopenai.hk_development_mcp_server.tools.new_building_plan_processed.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            mock_fetch_csv_from_url.return_value = [
                {
                    "Year": "2019",
                    "Month": "1",
                    "First Submission & Major Revision": "100",
                    "Re-submission": "50",
                    "Total": "150",
                },
                {
                    "Year": "2019",
                    "Month": "2",
                    "First Submission & Major Revision": "120",
                    "Re-submission": "60",
                    "Total": "180",
                },
                {
                    "Year": "2020",
                    "Month": "1",
                    "First Submission & Major Revision": "110",
                    "Re-submission": "55",
                    "Total": "165",
                },
            ]

            # Test filtering by year range
            result = _get_new_building_plans_processed(2019, 2019)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["Year"], "2019")
            self.assertEqual(result[1]["Year"], "2019")

            # Test empty result for non-matching years
            result = _get_new_building_plans_processed(2021, 2022)
            self.assertEqual(len(result), 0)

            # Test partial year match
            result = _get_new_building_plans_processed(2019, 2020)
            self.assertEqual(len(result), 3)

    def test_register_tool(self):
        """
        Test the registration of the get_new_building_plans_processed tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_new_building_plans_processed function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Retrieve data on the number of plans processed by the Building Authority in Hong Kong for new buildings within a specified year range."
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(
            decorated_function.__name__, "get_new_building_plans_processed"
        )

        # Call the decorated function and verify it calls _get_new_building_plans_processed
        with patch(
            "hkopenai.hk_development_mcp_server.tools.new_building_plan_processed._get_new_building_plans_processed"
        ) as mock_get_new_building_plans_processed:
            decorated_function(start_year=2018, end_year=2019)
            mock_get_new_building_plans_processed.assert_called_once_with(2018, 2019)
