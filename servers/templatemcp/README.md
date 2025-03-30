# MCP Server Template

## Tools

- add_numbers

## Usage

[Install uv.](https://docs.astral.sh/uv/getting-started/installation/)

GitHub

```json
{
  "mcpServers": {
    "templatemcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/templatemcp",
        "templatemcp"
      ]
    }
  }
}
```

PyPI

```json
{
  "mcpServers": {
    "templatemcp": {
      "command": "uvx",
      "args": ["templatemcp"]
    }
  }
}
```

Local

```json
{
  "mcpServers": {
    "templatemcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/mcp-incubator/servers/templatemcp",
        "templatemcp"
      ]
    }
  }
}
```
