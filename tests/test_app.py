import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_development_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_development_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_development_mcp_server.tool_new_building_plan_processed.get_new_building_plans_processed')
    def test_create_mcp_server(self, mock_tool_building_plans, mock_fastmcp):
        # Setup mocks
        mock_server = Mock()
        
        # Track decorator calls and capture decorated function
        decorator_calls = []
        decorated_func = None
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                nonlocal decorated_func
                decorated_func = f
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_fastmcp.return_value = mock_server
        mock_tool_building_plans.return_value = [
            {"Year": "2011", "Month": "6", "First submission & major revision": "445", "Re-submission": "853", "Total": "1298"}
        ]

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tool was decorated
        self.assertIsNotNone(decorated_func)
        
        # Test the actual decorated function if it relates to building plans
        if decorated_func and hasattr(decorated_func, '__name__') and decorated_func.__name__ == 'get_new_building_plans_processed':
            result = decorated_func(2011, 2011)
            mock_tool_building_plans.assert_called_once_with(2011, 2011)
            self.assertEqual(result, [
                {"Year": "2011", "Month": "6", "First submission & major revision": "445", "Re-submission": "853", "Total": "1298"}
            ])

if __name__ == "__main__":
    unittest.main()

