from abc import ABC, abstractmethod
from typing import Iterator


class ChatLLM(ABC):
    """Abstract base class for chat LLMs."""

    @abstractmethod
    def completions(
        self, prompt: list[dict], stream: bool = False, **kwargs
    ) -> Iterator[str]:
        pass
