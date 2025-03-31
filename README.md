# MCP Servers

## Installation

Install uv: [instructions](https://docs.astral.sh/uv/getting-started/installation/)

```sh
pipx install uv
```

Install package

```sh
uv sync
```

## Usage

Run the bot:

```sh
uv run mcpservers
```

## Add New MCP Server

1. Copy `servers/templatemcp` directory to `servers/` directory and rename it to your server name.
2. Add you server to `uv.workspace.members` in `pyproject.toml` file.

```toml
[tool.uv.workspace]
members = ["servers/templatemcp", "servers/planningmcp", "servers/yourmcp"]

[tool.uv.sources]
templatemcp = { workspace = true }
planningmcp = { workspace = true }
yourmcp = { workspace = true }
```

3. Add your MCP server to bot in `mcpservers.cli` file.
