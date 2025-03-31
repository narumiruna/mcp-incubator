from __future__ import annotations

import os
from functools import cache

from agents import ModelSettings
from agents import RunConfig

from .providers import AzureModelProvider
from .providers import GeminiModelProvider


@cache
def get_available_providers() -> list[str]:
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
def get_run_config(provider: str | None = None, model: str | None = None) -> RunConfig:
    available_providers = get_available_providers()

    if provider is None:
        provider = available_providers[0]

    if provider not in available_providers:
        raise ValueError(f"Provider {provider} is not available. Available providers: {available_providers}")

    match provider:
        case "openai":
            return RunConfig(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
        case "azure":
            return RunConfig(model_provider=AzureModelProvider())
        case "gemini":
            return RunConfig(model_provider=GeminiModelProvider())
        case _:
            raise ValueError(f"Unknown provider: {provider}")


@cache
def get_model_settings() -> ModelSettings:
    temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    return ModelSettings(temperature=temperature)


# @cache
# def get_run_config() -> RunConfig:
#     gemini_api_key = os.getenv("GEMINI_API_KEY")
#     if gemini_api_key is not None:
#         logger.info("Using Gemini API key")
#         return RunConfig(model_provider=GeminiModelProvider())

#     azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
#     if azure_api_key is not None:
#         logger.info("Using Azure OpenAI API key")

#         return
#     model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#     return RunConfig(model=model_name)


# @cache
# def get_run_configs() -> dict[str, RunConfig]:
#     configs = {}

#     gemini_api_key = os.getenv("GEMINI_API_KEY")
#     if gemini_api_key is not None:
#         configs["gemini"] = RunConfig(model_provider=GeminiModelProvider())

#     azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
#     if azure_api_key is not None:
#         configs["azure"] = RunConfig(model_provider=AzureModelProvider())

#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     if openai_api_key is not None:
#         configs["openai"] = RunConfig(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

#     return configs
