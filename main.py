from uuid import uuid4
from fastmcp import FastMCP
from temporalio.client import Client
from temporal.data import InvoiceData, Status

mcp = FastMCP("temporal-based-mcp")

_client: Client | None = None


async def get_client() -> Client:
    global _client
    if _client is None:
        _client = await Client.connect("temporal://localhost:7233")
    return _client


@mcp.tool
async def process_invoice(data: InvoiceData):
    client = await get_client()
    handle = await client.start_workflow(
        "InvoiceProcessingWorkflow",
        data,
        id=f"invoice-workflow-{uuid4()}",
        task_queue="invoice-task-queue",
    )
    return {"workflow_id": handle.id, "run_id": handle.run_id}


@mcp.tool
async def change_status(workflow_id: str, status: Status):
    client = await get_client()
    handle = client.get_workflow_handle(workflow_id)
    await handle.signal("change_status", status.value)
    return {"workflow_id": workflow_id, "status": status.value}


@mcp.tool
async def check_status(workflow_id: str):
    client = await get_client()
    handle = client.get_workflow_handle(workflow_id)
    status = await handle.query("check_status")
    return {"workflow_id": workflow_id, "status": status}


@mcp.tool
async def check_workflow_status(workflow_id: str):
    client = await get_client()
    handle = client.get_workflow_handle(workflow_id)
    description = await handle.describe()
    return {
        "workflow_id": workflow_id,
        "status": description.status.name,
        "run_id": description.run_id,
        "task_queue": description.task_queue,
    }


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
