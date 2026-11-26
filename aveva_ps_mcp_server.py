"""Entry point for the AVEVA Process Simulation MCP Server."""

from aveva_ps_mcp.server import mcp

if __name__ == "__main__":
    mcp.run()
