from __future__ import annotations

from typing import Final

import anyio
import gradio as gr
import typer
from agents.mcp import MCPServer
from agents.mcp import MCPServerStdio
from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import Bot
from .config import get_available_providers

DEFAULT_INSTRUCTIONS: Final[str] = """使用台灣正體中文。擅長邏輯推理且謹慎，能夠將問題拆解並逐步進行思考。"""


app = typer.Typer()


@app.command()
def bot() -> None:
    load_dotenv(find_dotenv())

    mcp_servers: list[MCPServer] = [
        MCPServerStdio(
            params={
                "command": "uvx",
                "args": ["yfmcp"],
            }
        ),
        # https://github.com/modelcontextprotocol/servers/tree/main/src/time
        MCPServerStdio(
            params={
                "command": "uvx",
                "args": ["mcp-server-time", "--local-timezone=Asia/Taipei"],
            }
        ),
    ]

    bot = Bot(instructions=DEFAULT_INSTRUCTIONS, mcp_servers=mcp_servers)
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        with gr.Row():
            with gr.Column():
                # switch provider
                gr.Interface(
                    fn=bot.set_provider,
                    inputs=[gr.Dropdown(choices=get_available_providers(), label="Provider")],
                    outputs=[],
                    live=True,
                    flagging_mode="never",
                    clear_btn=None,
                )
            # set instructions
            gr.Interface(
                fn=bot.set_instructions,
                inputs=[gr.Textbox(label="Instructions", value=bot.agent.instructions)],
                outputs=[],
                flagging_mode="never",
                clear_btn=None,
            )

        gr.ChatInterface(bot.chat, type="messages")
        demo.launch()

    anyio.run(bot.cleanup)
