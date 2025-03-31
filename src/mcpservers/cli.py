from __future__ import annotations

import anyio
import gradio as gr
import typer
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

from .bot import Bot

app = typer.Typer()


@app.command()
def bot(instructions: str = "使用繁體中文回答問題") -> None:
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
