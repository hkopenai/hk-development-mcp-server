"""
This module contains the FastMCP server implementation for the HK OpenAI Development Server.
It is responsible for creating and configuring the server, and registering the available tools.
"""

from fastmcp import FastMCP
from .tools import new_building_plan_processed


def server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI development Server")

    new_building_plan_processed.register(mcp)

    return mcp
