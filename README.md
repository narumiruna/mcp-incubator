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
uv run mcpservers bot
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

3. Or you can add a new bot to `mcpservers.cli`, for example:

```python
import anyio
import gradio as gr
import typer
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

from .bot import Bot

app = typer.Typer()


@app.command()
def stock_bot(instructions: str = "...") -> None:
    load_dotenv()

    bot = Bot(
        instructions=instructions,
        mcp_servers=[
            MCPServerStdio(
                params={
                    "command": "uvx",
                    "args": ["yfmcp"],
                }
            )
        ],
    )

    demo = gr.ChatInterface(bot.chat, type="messages")
    demo.launch()

    anyio.run(bot.cleanup)

@app.command()
def bot(instructions: str = "...") -> None:
...
```
