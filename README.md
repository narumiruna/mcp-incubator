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
# run the stock bot
uv run mcpservers stock

# run the time bot
uv run mcpservers time
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

3. [Optional] Add a new bot in `mcpservers.cli` to test your MCP server.
