from dataclasses import dataclass, field
from enum import Enum


class Status(str, Enum):
    CREATED = "CREATED"
    SENT = "SENT"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


@dataclass
class InvoiceData:
    title: str
    recipient: str
    price: float
    status: Status = field(default=Status.CREATED)