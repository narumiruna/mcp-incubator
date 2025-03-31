import os
from typing import Final

from agents import Model
from agents import ModelProvider
from agents import OpenAIChatCompletionsModel
from agents import set_tracing_disabled
from openai import AsyncOpenAI

DEFAULT_GEMINI_MODEL: Final[str] = "gemini-2.0-flash"
DEFAULT_GEMINI_BASE_URL: Final[str] = "https://generativelanguage.googleapis.com/v1beta/openai/"


class GeminiModelProvider(ModelProvider):
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY is not set.")

        base_url = os.getenv("GEMINI_BASE_URL", DEFAULT_GEMINI_BASE_URL)

        set_tracing_disabled(True)
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=model_name or DEFAULT_GEMINI_MODEL, openai_client=self.client)
