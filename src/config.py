"""Configuration: LLM setup, paths, and environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ORDERS_QUEUE = DATA_DIR / "orders_queue.csv"
DEV_LABELED = DATA_DIR / "orders_dev_labeled.csv"
PERSONAS = DATA_DIR / "personas.md"

ISSUE_CATEGORIES = [
    "delivery_delay",
    "wrong_item",
    "damaged",
    "refund_request",
    "payment_issue",
    "address_change",
    "cancel_request",
    "product_question",
    "subscription",
    "fraud_alert",
]

BASE_PRIORITY = {
    "fraud_alert": "URGENT",
    "payment_issue": "URGENT",
    "damaged": "HIGH",
    "wrong_item": "HIGH",
    "delivery_delay": "MEDIUM",
    "refund_request": "MEDIUM",
    "address_change": "MEDIUM",
    "cancel_request": "MEDIUM",
    "product_question": "LOW",
    "subscription": "LOW",
}

PRIORITY_LADDER = ["LOW", "MEDIUM", "HIGH", "URGENT"]

# LLM Configuration — using Anthropic via Portkey gateway
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "")
ANTHROPIC_CUSTOM_HEADERS = os.getenv("ANTHROPIC_CUSTOM_HEADERS", "")
MODEL_NAME = os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL", "claude-sonnet-4-20250514")
