from __future__ import annotations

import anyio
import gradio as gr
import typer
from agents.mcp import MCPServer
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from loguru import logger

from .bot import Bot
from .config import get_run_configs

app = typer.Typer()


@app.command()
def bot(instructions: str | None = None) -> None:
    load_dotenv()

    mcp_servers: list[MCPServer] = [
        MCPServerStdio(
            params={
                "command": "uvx",
                "args": ["yfmcp"],
            }
        )
    ]

    bot = Bot(instructions=instructions, mcp_servers=mcp_servers)

    run_configs = get_run_configs()

    def update_provider(provider: str) -> None:
        logger.info(f"Switching to {provider} provider")
        bot.set_run_config(run_configs[provider])
        return

    with gr.Blocks() as demo:
        with gr.Column():
            gr.Interface(
                fn=update_provider,
                inputs=[gr.Dropdown(choices=list(run_configs.keys()), label="Provider")],
                outputs=[],
            )
            gr.ChatInterface(bot.chat, type="messages")
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
