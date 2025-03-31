from __future__ import annotations

import anyio
import gradio as gr
import typer
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

from .bot import Bot

app = typer.Typer()


@app.command()
def stock(instructions: str | None = None) -> None:
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
def time(instructions: str | None = None) -> None:
    load_dotenv()

    bot = Bot(
        instructions=instructions,
        mcp_servers=[
            # https://github.com/modelcontextprotocol/servers/tree/main/src/time
            MCPServerStdio(
                params={
                    "command": "uvx",
                    "args": ["mcp-server-time", "--local-timezone=Asia/Taipei"],
                }
            )
        ],
    )

    demo = gr.ChatInterface(bot.chat, type="messages")
    demo.launch()

    anyio.run(bot.cleanup)
