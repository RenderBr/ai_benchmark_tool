from sqlmodel import SQLModel, Field

class Evaluation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key='user.id')
    prompt: str
    model: str
    response: str
    score: int
