# Temporal Based MCP
This is a demo to test durable & reliable MCP tools with Temporal.

## Setup
### Clone repo
```bash
git clone https://github.com/thinker-chetan/mcp-wt-temporal
```
### Install dependencies

```bash
uv sync
```

## Use

### Run Temporal Server, UI (via docker)
```docker
docker run --rm -p 7233:7233 -p 8233:8233 temporalio/temporal:latest server start-dev --ip 0.0.0.0
```
### Run Temporal Worker
```bash
uv run python -m temporal.worker
```
### Run MCP Server
```bash
uv run python main.py
```
### Connect MCP to gemini
Already done - Refer [settings.json](./.gemini/settings.json)

### Test 
```bash
gemini
```
Ask gemini to process an invoice, approve or reject the invoice - completes the workflow. You can check status of both invoice and workflow.