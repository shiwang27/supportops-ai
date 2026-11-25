# SupportOps AI

SupportOps AI is a learning project for building a small AI-powered support operations tool.

The project will start with simple Python code and gradually add APIs, document search, RAG, and agent workflows.

## Current status

Phase 5: document ingestion

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
