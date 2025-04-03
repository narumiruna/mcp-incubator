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


def load_config(f: str | Path) -> list[MCPServerStdio]:
    data = load_json(f)
    return [MCPServerStdio(params=params) for params in data["mcpServers"].values()]
