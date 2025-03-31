from __future__ import annotations

import anyio
import gradio as gr
import typer
from agents.mcp import MCPServer
from agents.mcp import MCPServerStdio
from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import Bot
from .config import get_run_configs

app = typer.Typer()


@app.command()
def bot(instructions: str | None = None) -> None:
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

    bot = Bot(instructions=instructions, mcp_servers=mcp_servers)

    run_configs = get_run_configs()
    provider_names = list(run_configs.keys())
    if len(provider_names) == 0:
        raise ValueError("No providers found.")

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        with gr.Row():
            with gr.Column():
                # switch provider
                gr.Interface(
                    fn=bot.set_provider,
                    inputs=[gr.Dropdown(choices=provider_names, label="Provider")],
                    outputs=[],
                    live=True,
                    allow_flagging="never",
                    clear_btn=None,
                )
                # switch model
                # gr.Interface(
                #     fn=bot.set_model,
                #     inputs=[gr.Dropdown(choices=["gpt-4o", "gpt-4o-mini", "gemini-2.0-flash"], label="Model")],
                #     outputs=[],
                #     live=True,
                #     allow_flagging="never",
                #     clear_btn=None,
                # )
            # set instructions
            gr.Interface(
                fn=bot.set_instructions,
                inputs=[
                    gr.Textbox(
                        label="Instructions",
                        value="使用台灣正體中文。擅長邏輯思考且嚴謹，會分解問題並且一步一步地思考。",
                    )
                ],
                outputs=[],
                allow_flagging="never",
                clear_btn=None,
            )

        gr.ChatInterface(bot.chat, type="messages")
        demo.launch()

    anyio.run(bot.cleanup)
