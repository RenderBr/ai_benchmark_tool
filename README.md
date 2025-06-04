# AI Prompt Benchmark Tool

This repository contains a minimal prototype of the application described in `AGENTS.md`. The app lets users submit a prompt, sends it to multiple (dummy) AI models, scores the responses, and displays them side by side.

## Features

- Simple web UI for entering a prompt
- Two example models (echo and reverse) configured in the database
- Length-based scoring metric
- REST API built with FastAPI
- User registration and JWT-based login
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

### Authentication

Register a new user:

```bash
curl -X POST http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"user","password":"pass"}'
```

To register an admin account, include `is_admin: true` in the JSON body.

Use the returned token to authenticate when calling protected endpoints:

```bash
curl -X POST http://localhost:8000/login \
  -d 'username=user&password=pass'

# Example using the token for evaluation
curl -X POST http://localhost:8000/api/evaluate \
  -H "Authorization: Bearer <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"hello"}'
```

### Admin model management

List models (requires admin token):

```bash
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/admin/models
```

Add a model:

```bash
curl -X POST http://localhost:8000/admin/models \
  -H "Authorization: Bearer <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Echo2","type":"echo"}'
```

Delete a model:

```bash
curl -X DELETE -H "Authorization: Bearer <TOKEN>" \
  http://localhost:8000/admin/models/<ID>
```
