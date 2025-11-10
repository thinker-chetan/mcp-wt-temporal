from datetime import timedelta
from temporalio import workflow
from temporal.activities import (
    create_invoice_activity,
    send_invoice_activity,
    process_payment_activity,
    complete_invoice_activity,
)
from temporal.data import InvoiceData, Status


@workflow.defn(name="InvoiceProcessingWorkflow")
class InvoiceProcessingWorkflow:
    def __init__(self) -> None:
        self.invoice: InvoiceData | None = None
        self.status: Status = Status.CREATED

    @workflow.run
    async def run(self, data: InvoiceData) -> str:
        self.invoice = data
        self.status = Status.CREATED
        await workflow.execute_activity(
            create_invoice_activity,
            self.invoice,
            start_to_close_timeout=timedelta(seconds=10),
        )
        self.status = Status.SENT
        await workflow.execute_activity(
            send_invoice_activity,
            self.invoice,
            start_to_close_timeout=timedelta(seconds=10),
        )

        await workflow.wait_condition(lambda: self.status != Status.SENT and self.status != Status.PENDING and self.status != Status.CREATED)

        if self.status == Status.REJECTED:
            return "Invoice processing rejected"
        elif self.status == Status.APPROVED: 
            self.status = Status.COMPLETED
            await workflow.execute_activity(
                process_payment_activity,
                self.invoice,
                start_to_close_timeout=timedelta(seconds=10),
            )
            await workflow.execute_activity(
                complete_invoice_activity,
                self.invoice,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return "Invoice processing complete"

    @workflow.signal(name="change_status")
    async def change_status(self, status: str) -> None:
        self.status = Status(status)

    @workflow.query(name="check_status")
    def check_status(self) -> str:
        return self.status.value