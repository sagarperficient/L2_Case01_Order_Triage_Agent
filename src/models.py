"""State definitions and data models for the triage agent."""

from typing import TypedDict, Optional
from enum import Enum


class IssueCategory(str, Enum):
    DELIVERY_DELAY = "delivery_delay"
    WRONG_ITEM = "wrong_item"
    DAMAGED = "damaged"
    REFUND_REQUEST = "refund_request"
    PAYMENT_ISSUE = "payment_issue"
    ADDRESS_CHANGE = "address_change"
    CANCEL_REQUEST = "cancel_request"
    PRODUCT_QUESTION = "product_question"
    SUBSCRIPTION = "subscription"
    FRAUD_ALERT = "fraud_alert"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class Route(str, Enum):
    MARCUS = "marcus"
    PRIYA = "priya"


class TriageState(TypedDict, total=False):
    order_id: str
    customer_tier: str
    text_note: str
    status: str
    category: str
    priority: str
    route: str
    draft_reply: Optional[str]
    escalation_summary: Optional[str]
    rationale: str
