from __future__ import annotations

import os
from functools import cache
from typing import cast

import anyio
import gradio as gr
from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    set_default_openai_client,
    set_default_openai_key,
    set_tracing_disabled,
)
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI


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


class Bot:
    def __init__(self, mcp_servers: list[MCPServerStdio] | None = None) -> None:
        self.mcp_servers = mcp_servers or []
        self.agent = Agent(
            name="Bot",
            instructions="使用台灣中文",
            model=get_openai_model(),
            model_settings=get_openai_model_settings(),
            mcp_servers=self.mcp_servers,
        )

        self._connected = False
        self.input_items = []

    async def _connect(self) -> None:
        if self._connected:
            return

        for mcp_server in self.mcp_servers:
            await mcp_server.connect()
        self._connected = True

    async def chat(self, text: str, _: list[dict[str, str]]) -> dict[str, str]:
        await self._connect()

        self.input_items.append(
            {
                "role": "user",
                "content": text,
            }
        )
        result = await Runner.run(self.agent, input=self.input_items)
        self.input_items = result.to_input_list()
        return {
            "role": "assistant",
            "content": result.final_output,
        }

    async def cleanup(self) -> None:
        for mcp_server in self.mcp_servers:
            await mcp_server.cleanup()


def main() -> None:
    load_dotenv()

    bot = Bot(
        [
            MCPServerStdio(
                params={
                    "command": "uvx",
                    "args": ["yfmcp"],
                }
            )
        ]
    )

    demo = gr.ChatInterface(bot.chat, type="messages")
    demo.launch()

    anyio.run(bot.cleanup)


if __name__ == "__main__":
    main()
