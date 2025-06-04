from sqlmodel import SQLModel, create_engine, Session, select
from .models.model_config import ModelConfig
from .models.user import User
from .models.evaluation import Evaluation

engine = create_engine('sqlite:///./app.db')

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        existing = session.exec(select(ModelConfig)).first()
        if existing is None:
            session.add(ModelConfig(name="Echo", type="echo"))
            session.add(ModelConfig(name="Reverse", type="reverse"))
            session.commit()


def get_session():
    return Session(engine)
