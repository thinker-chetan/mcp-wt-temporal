import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from temporal.activities import (
    create_invoice_activity,
    send_invoice_activity,
    process_payment_activity,
    complete_invoice_activity,
)
from temporal.workflow import InvoiceProcessingWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="invoice-task-queue",
        workflows=[InvoiceProcessingWorkflow],
        activities=[
            create_invoice_activity,
            send_invoice_activity,
            process_payment_activity,
            complete_invoice_activity,
        ],
    )
    print("Worker started for invoice processing...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())