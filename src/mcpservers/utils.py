from __future__ import annotations

import textwrap

from agents import HandoffOutputItem
from agents import ItemHelpers
from agents import MessageOutputItem
from agents import RunItem
from agents import ToolCallItem
from agents import ToolCallOutputItem
from agents.items import ResponseFunctionToolCall
from loguru import logger


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
            if isinstance(new_item.raw_item, ResponseFunctionToolCall):
                logger.info("Calling tool: {}({})", new_item.raw_item.name, new_item.raw_item.arguments)
        elif isinstance(new_item, ToolCallOutputItem):
            logger.info("Tool call output: {}", shorten_text(str(new_item.raw_item["output"])))
        else:
            logger.info("Skipping item: {}", new_item.__class__.__name__)
