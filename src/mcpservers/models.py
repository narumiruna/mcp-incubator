from __future__ import annotations

import os
from functools import cache

from agents import ModelSettings
from agents import OpenAIChatCompletionsModel
from agents import set_tracing_disabled
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI


@cache
def get_providers() -> list[str]:
    providers = []
    if os.getenv("OPENAI_API_KEY") is not None:
        providers.append("openai")
    if os.getenv("GEMINI_API_KEY") is not None:
        providers.append("gemini")
    if os.getenv("AZURE_OPENAI_API_KEY") is not None:
        providers.append("azure")

    if len(providers) == 0:
        raise ValueError("No providers found. Please set OPENAI_API_KEY, AZURE_OPENAI_API_KEY, or GEMINI_API_KEY.")

    return providers


@cache
def get_model_settings() -> ModelSettings:
    temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    return ModelSettings(temperature=temperature)


@cache
def get_openai_model() -> OpenAIChatCompletionsModel:
    return OpenAIChatCompletionsModel(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_client=AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")),
    )


@cache
def get_azure_model() -> OpenAIChatCompletionsModel:
    set_tracing_disabled(True)
    return OpenAIChatCompletionsModel(
        model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini"),
        openai_client=AsyncAzureOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY")),
    )


@cache
def get_gemini_model() -> OpenAIChatCompletionsModel:
    set_tracing_disabled(True)
    return OpenAIChatCompletionsModel(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        openai_client=AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv(
                "GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
        ),
    )


def get_model(provider: str | None = None) -> OpenAIChatCompletionsModel:
    available_providers = get_providers()
    if provider is None:
        provider = available_providers[0]

    match provider:
        case "openai":
            return get_openai_model()
        case "azure":
            return get_azure_model()
        case "gemini":
            return get_gemini_model()
        case _:
            raise ValueError(f"Unknown provider: {provider}")
