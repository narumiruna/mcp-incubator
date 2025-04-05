# NoteMCP

## Tools

- add_numbers

## Usage

[Install uv.](https://docs.astral.sh/uv/getting-started/installation/)

GitHub

```json
{
  "mcpServers": {
    "notemcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/nationalteam/mcp-servers#subdirectory=servers/notemcp",
        "notemcp"
      ]
    }
  }
}
```

Local

```json
{
  "mcpServers": {
    "notemcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/mcp-servers/servers/notemcp",
        "notemcp"
      ]
    }
  }
}
```
