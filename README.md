# SupportOps AI

SupportOps AI is a learning project for building a small AI-powered support operations tool.

The project will start with simple Python code and gradually add APIs, document search, RAG, and agent workflows.

## Current status

Working MVP: ticket API, document search, and grounded assistant

## Run the project

```bash
python main.py
```

The Python environment will be set up before we add external packages.

Tickets are now saved in a local `tickets.json` file so they are available the next time the program starts.

## Start the API

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn api:app --reload
```

The API includes a health check at `/health`, along with endpoints for listing and creating tickets.

Support documents can be placed in the `documents` folder as `.txt` files. The `/documents/chunks` endpoint reads those files, splits them into smaller pieces, and keeps the source filename with each piece.

## Assistant endpoints

- `POST /assistant/ask` routes a question to ticket lookup or document search.
- `GET /evaluation` runs a small retrieval evaluation set.

The current search implementation uses local TF-IDF vectors, so the project works without an external API key. The assistant returns retrieved support text with source filenames. A later upgrade can replace this local retrieval layer with neural embeddings and a hosted vector database.

This is a working learning MVP. It does not claim to be a production system yet: ticket data is stored in a local JSON file, and the assistant uses retrieved text instead of an external language model.

## Run with Docker

```bash
docker build -t supportops-ai .
docker run -p 8080:8080 supportops-ai
```
