from sqlmodel import SQLModel, Field

class ModelConfig(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str
