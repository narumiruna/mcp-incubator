import os
from typing import Final

from agents import Model
from agents import ModelProvider
from agents import OpenAIChatCompletionsModel
from agents import set_tracing_disabled
from openai import AsyncAzureOpenAI

DEFAULT_OPENAI_MODEL: Final[str] = "gpt-4o"


class AzureModelProvider(ModelProvider):
    def __init__(self) -> None:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("AZURE_OPENAI_API_KEY is not set.")

        set_tracing_disabled(True)
        self.client = AsyncAzureOpenAI(api_key=api_key)

    def get_model(self, model_name: str | None) -> Model:
        if model_name is None:
            model_name = os.getenv("AZURE_OPENAI_MODEL")

        return OpenAIChatCompletionsModel(
            model=model_name or DEFAULT_OPENAI_MODEL,
            openai_client=self.client,
        )
