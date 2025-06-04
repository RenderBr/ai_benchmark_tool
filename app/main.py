from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Dict, Optional

from sqlmodel import select

from .models.dummy import EchoModel, ReverseModel
from .scoring import length_score
from .models.user import User
from .models.evaluation import Evaluation
from .database import init_db, get_session
from .auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
)

app = FastAPI(title="AI Prompt Benchmark")
app.add_event_handler("startup", init_db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)

# Initialize models
MODELS = [EchoModel(), ReverseModel()]

class PromptRequest(BaseModel):
    prompt: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ModelResult(BaseModel):
    model: str
    response: str
    score: int

class PromptResponse(BaseModel):
    results: List[ModelResult]


def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[User]:
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload["sub"]
    with get_session() as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

def evaluate_prompt(prompt: str) -> List[Dict[str, str]]:
    results = []
    for model in MODELS:
        try:
            resp = model.generate(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model {model.name} error: {e}")
        score = length_score(resp)
        results.append({"model": model.name, "response": resp, "score": score})
    return results


@app.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest):
    with get_session() as session:
        existing = session.exec(select(User).where(User.username == data.username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username taken")
        user = User(username=data.username, hashed_password=get_password_hash(data.password))
        session.add(user)
        session.commit()
        token = create_access_token({"sub": user.username})
        return {"access_token": token}


@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_session() as session:
        user = session.exec(select(User).where(User.username == form_data.username)).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        token = create_access_token({"sub": user.username})
        return {"access_token": token}

@app.post("/api/evaluate", response_model=PromptResponse)
async def evaluate(req: PromptRequest, token: Optional[str] = Depends(oauth2_scheme)):
    user: Optional[User] = None
    if token:
        payload = decode_token(token)
        if payload and "sub" in payload:
            with get_session() as session:
                user = session.exec(select(User).where(User.username == payload["sub"])).first()
    results = evaluate_prompt(req.prompt)
    if user:
        with get_session() as session:
            for r in results:
                ev = Evaluation(
                    user_id=user.id,
                    prompt=req.prompt,
                    model=r["model"],
                    response=r["response"],
                    score=r["score"],
                )
                session.add(ev)
            session.commit()
    return {"results": results}

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")
