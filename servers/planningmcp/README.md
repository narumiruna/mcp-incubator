# Planning MCP Server

## Tools

- planning_tool

## Usage

[Install uv.](https://docs.astral.sh/uv/getting-started/installation/)

GitHub

```json
{
  "mcpServers": {
    "planningmcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/nationalteam/mcp-servers#subdirectory=servers/planningmcp",
        "planningmcp"
      ]
    }
  }
}
```

Local

```json
{
  "mcpServers": {
    "planningmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/mcp-servers/servers/planningmcp",
        "planningmcp"
      ]
    }
  }
}
```
