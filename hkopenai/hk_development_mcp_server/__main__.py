"""
Console-script entry point for hkopenai.hk_development_mcp_server.
"""

from hkopenai_common.cli_utils import cli_main
from .server import server


def main():
    """Console-script entry point for the hk development mcp server."""
    cli_main(server, "hk development mcp server")


if __name__ == "__main__":
    main()
