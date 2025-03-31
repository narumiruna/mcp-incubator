from __future__ import annotations

import os
import textwrap
from functools import cache
from typing import cast

import anyio
import gradio as gr
import typer
from agents import Agent
from agents import HandoffOutputItem
from agents import ItemHelpers
from agents import MessageOutputItem
from agents import ModelSettings
from agents import OpenAIChatCompletionsModel
from agents import RunItem
from agents import Runner
from agents import ToolCallItem
from agents import ToolCallOutputItem
from agents import set_default_openai_client
from agents import set_default_openai_key
from agents import set_tracing_disabled
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from loguru import logger
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI


@cache
def get_openai_model_settings() -> ModelSettings:
    temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    return ModelSettings(temperature=temperature)


@cache
def get_openai_model() -> OpenAIChatCompletionsModel:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return OpenAIChatCompletionsModel(
        model_name,
        openai_client=get_openai_client(),
    )


@cache
def get_openai_client() -> AsyncOpenAI:
    azure_api_key = os.getenv(key="AZURE_OPENAI_API_KEY")
    if azure_api_key is not None:
        azure_client = AsyncAzureOpenAI(api_key=azure_api_key)
        set_default_openai_key(azure_api_key)
        set_default_openai_client(azure_client)

        # Disable tracing since Azure doesn't support it
        set_tracing_disabled(True)

        return cast(AsyncOpenAI, azure_client)

    return AsyncOpenAI()


def shorten_text(text: str, width: int = 100, placeholder: str = "...") -> str:
    return textwrap.shorten(text, width=width, placeholder=placeholder)


def log_new_items(new_items: list[RunItem]) -> None:
    for new_item in new_items:
        if isinstance(new_item, MessageOutputItem):
            logger.info("Message: {}", shorten_text(ItemHelpers.text_message_output(new_item)))
        elif isinstance(new_item, HandoffOutputItem):
            logger.info(
                "Handed off from {} to {}",
                new_item.source_agent.name,
                new_item.target_agent.name,
            )
        elif isinstance(new_item, ToolCallItem):
            logger.info(
                "Calling tool: {}({})",
                new_item.raw_item.name,
                new_item.raw_item.arguments,
            )
        elif isinstance(new_item, ToolCallOutputItem):
            logger.info("Tool call output: {}", shorten_text(new_item.raw_item["output"]))
        else:
            logger.info("Skipping item: {}", new_item.__class__.__name__)


class Bot:
    def __init__(self, instructions: str, mcp_servers: list[MCPServerStdio] | None = None) -> None:
        self.mcp_servers = mcp_servers or []
        self.agent = Agent(
            name=self.__class__.__name__,
            instructions=instructions,
            model=get_openai_model(),
            model_settings=get_openai_model_settings(),
            mcp_servers=self.mcp_servers,
        )

        self._connected = False
        self.input_items = []  # type: ignore

    async def _connect(self) -> None:
        if self._connected:
            return

        for mcp_server in self.mcp_servers:
            await mcp_server.connect()
        self._connected = True

    async def chat(self, text: str, history: list[dict[str, str]]) -> dict[str, str]:
        await self._connect()

        self.input_items.append(
            {
                "role": "user",
                "content": text,
            }
        )
        result = await Runner.run(self.agent, input=self.input_items)
        self.input_items = result.to_input_list()

        log_new_items(result.new_items)

        return {
            "role": "assistant",
            "content": result.final_output,
        }

    async def cleanup(self) -> None:
        for mcp_server in self.mcp_servers:
            await mcp_server.cleanup()


def main(instructions: str = "使用繁體中文回答問題") -> None:
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


if __name__ == "__main__":
    typer.run(main)
