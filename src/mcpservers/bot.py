from __future__ import annotations

from typing import Any

from agents import Agent
from agents import Runner
from agents.mcp import MCPServer
from loguru import logger

from mcpservers.config import get_model
from mcpservers.config import get_model_settings
from mcpservers.utils import log_new_items


class Bot:
    def __init__(self, instructions: str | None = None, mcp_servers: list[MCPServer] | None = None) -> None:
        self.mcp_servers = mcp_servers or []
        self.agent = Agent(
            name=self.__class__.__name__,
            instructions=instructions,
            model=get_model(),
            model_settings=get_model_settings(),
            mcp_servers=self.mcp_servers,
        )

        self._connected = False
        self.input_items: list[Any] = []

    def clear_messages(self) -> None:
        logger.info("Clearning messages")
        self.input_items = []

    def set_model(self, provider: str) -> None:
        logger.info(f"Switching to {provider}'s model")
        self.agent.model = get_model(provider)

        self.clear_messages()

    def set_instructions(self, instructions: str | None) -> None:
        logger.info(f"Setting instructions: {instructions}")
        self.agent.instructions = instructions

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
