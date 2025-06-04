from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict

from .models.dummy import EchoModel, ReverseModel
from .scoring import length_score

app = FastAPI(title="AI Prompt Benchmark")

# Initialize models
MODELS = [EchoModel(), ReverseModel()]

class PromptRequest(BaseModel):
    prompt: str

class ModelResult(BaseModel):
    model: str
    response: str
    score: int

class PromptResponse(BaseModel):
    results: List[ModelResult]

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

@app.post("/api/evaluate", response_model=PromptResponse)
async def evaluate(req: PromptRequest):
    results = evaluate_prompt(req.prompt)
    return {"results": results}

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")
