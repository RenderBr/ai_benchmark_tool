from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract model interface."""

    name: str

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        raise NotImplementedError
