from __future__ import annotations

import os
from functools import cache
from typing import cast

from agents import ModelSettings
from agents import OpenAIChatCompletionsModel
from agents import set_default_openai_client
from agents import set_default_openai_key
from agents import set_tracing_disabled
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
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_api_key is not None:
        azure_client = AsyncAzureOpenAI(api_key=azure_api_key)
        set_default_openai_key(azure_api_key)
        set_default_openai_client(azure_client)

        # Disable tracing since Azure doesn't support it
        set_tracing_disabled(True)

        return cast(AsyncOpenAI, azure_client)

    return AsyncOpenAI()
