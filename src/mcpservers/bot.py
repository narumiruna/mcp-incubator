from __future__ import annotations

from typing import Any

from agents import Agent
from agents import Runner
from agents.mcp import MCPServer

from mcpservers.config import get_model_settings
from mcpservers.config import get_run_config
from mcpservers.utils import log_new_items


class Bot:
    def __init__(self, instructions: str | None = None, mcp_servers: list[MCPServer] | None = None) -> None:
        self.mcp_servers = mcp_servers or []
        self.agent = Agent(
            name=self.__class__.__name__,
            instructions=instructions,
            model_settings=get_model_settings(),
            mcp_servers=self.mcp_servers,
        )
        self.run_config = get_run_config()

        self._connected = False
        self.input_items: list[Any] = []

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
        result = await Runner.run(
            self.agent,
            input=self.input_items,
            run_config=self.run_config,
        )
        self.input_items = result.to_input_list()

        log_new_items(result.new_items)

        return {
            "role": "assistant",
            "content": result.final_output,
        }

    async def cleanup(self) -> None:
        for mcp_server in self.mcp_servers:
            await mcp_server.cleanup()
