# AI Prompt Benchmark Tool

This repository contains a minimal prototype of the application described in `AGENTS.md`. The app lets users submit a prompt, sends it to multiple (dummy) AI models, scores the responses, and displays them side by side.

## Features

- Simple web UI for entering a prompt
- Two example models (echo and reverse)
- Length-based scoring metric
- REST API built with FastAPI
- Docker support for easy deployment

## Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

Then open `http://localhost:8000` in a browser.

## Docker

Build and run the Docker container:

```bash
docker build -t ai-benchmark-tool .

docker run -p 8000:8000 ai-benchmark-tool
```

Open `http://localhost:8000` to use the app.
