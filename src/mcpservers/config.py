import json
from pathlib import Path
from typing import TypedDict

from agents.mcp import MCPServerStdio
from agents.mcp import MCPServerStdioParams


class MCPServerConfig(TypedDict):
    mcpServers: dict[str, MCPServerStdioParams]


def load_json(f: str | Path) -> MCPServerConfig:
    with Path(f).open() as fp:
        return json.load(fp)


def load_mcp_servers_from_json(f: str | Path) -> list[MCPServerStdio]:
    config = load_json(f)
    return [MCPServerStdio(params=params) for params in config["mcpServers"].values()]
