from .base import BaseModel

class EchoModel(BaseModel):
    name = "echo-model"

    def generate(self, prompt: str) -> str:
        return f"Echo: {prompt}"

class ReverseModel(BaseModel):
    name = "reverse-model"

    def generate(self, prompt: str) -> str:
        return f"Reverse: {prompt[::-1]}"
