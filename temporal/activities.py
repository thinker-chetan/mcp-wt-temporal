from temporalio import activity

from temporal.data import InvoiceData


@activity.defn(name="create_invoice_activity")
async def create_invoice_activity(input: InvoiceData) -> str:
    activity.logger.info(f"Creating invoice for {input.recipient}...")
    return f"Invoice created for {input.recipient} with amount {input.price}"


@activity.defn(name="send_invoice_activity")
async def send_invoice_activity(input: InvoiceData) -> str:
    activity.logger.info(f"Sending invoice to {input.recipient}...")
    return f"Invoice sent to {input.recipient}"


@activity.defn(name="process_payment_activity")
async def process_payment_activity(input: InvoiceData) -> str:
    activity.logger.info(f"Processing payment for {input.recipient}...")
    return f"Payment processed for {input.recipient}"


@activity.defn(name="complete_invoice_activity")
async def complete_invoice_activity(input: InvoiceData) -> str:
    activity.logger.info(f"Completing invoice for {input.recipient}...")
    return f"Invoice for {input.recipient} completed"