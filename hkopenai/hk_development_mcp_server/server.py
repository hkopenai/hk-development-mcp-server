import argparse
from fastmcp import FastMCP
from hkopenai.hk_development_mcp_server import tool_new_building_plan_processed


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI development Server")

    tool_new_building_plan_processed.register(mcp)

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
