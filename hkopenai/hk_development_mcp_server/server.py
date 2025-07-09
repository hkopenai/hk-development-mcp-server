import argparse
from fastmcp import FastMCP
from hkopenai.hk_development_mcp_server import tool_new_building_plan_processed
from typing import Dict, List, Annotated, Optional, Union
from pydantic import Field


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI development Server")

    @mcp.tool(
        description="Retrieve data on the number of plans processed by the Building Authority in Hong Kong for new buildings within a specified year range."
    )
    def get_new_building_plans_processed(
        start_year: Annotated[int, Field(description="Start year for data range")],
        end_year: Annotated[int, Field(description="End year for data range")],
    ) -> List[Dict[str, Union[str, int]]]:
        return tool_new_building_plan_processed.get_new_building_plans_processed(
            start_year, end_year
        )

    return mcp


def main(args):
    """
    Main function to start the MCP Server.
    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http", host=args.host, port=args.port)
        print(f"MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
