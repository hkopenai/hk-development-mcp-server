"""
This module contains the FastMCP server implementation for the HK OpenAI Development Server.
It is responsible for creating and configuring the server, and registering the available tools.
"""
from fastmcp import FastMCP
from hkopenai.hk_development_mcp_server import tool_new_building_plan_processed


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI development Server")

    tool_new_building_plan_processed.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to start the MCP Server.
    Args:
        host: The host address to bind the server to.
        port: The port number to listen on.
        sse: A boolean indicating whether to run in SSE mode.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(f"MCP Server running in SSE mode on port {port}, bound to {host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")
