"""Starter skeleton: an agentic order-triage assistant.

Recommended stack: LangGraph. The graph is classify -> route -> (draft | escalate).
Fill in the TODOs. Keep the routing logic driven by data/personas.md so behavior is
auditable and easy to change.
"""
from pathlib import Path
from typing import TypedDict, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# The full queue you must triage. Unlabeled - classification is your job.
ORDERS = DATA_DIR / "orders_queue.csv"

# A small labeled subset for development and calibration. Representative of the
# ordinary cases only; the queue contains harder ones this subset does not cover.
DEV_LABELED = DATA_DIR / "orders_dev_labeled.csv"

PERSONAS = DATA_DIR / "personas.md"


class TriageState(TypedDict, total=False):
    order_id: str
    customer_tier: str
    text_note: str
    category: str
    priority: str
    route: str          # "marcus" (draft) or "priya" (escalate)
    draft_reply: Optional[str]
    rationale: str


def classify_node(state: TriageState) -> TriageState:
    """TODO: classify text_note into one issue category (see personas.md list).

    Return the state with `category` set. Prefer a constrained/enum output so the
    category is always one of the known values. Read the "Authority" and "Where
    this policy is silent" sections of personas.md before you decide how much
    weight to give the note text.
    """
    raise NotImplementedError


def route_node(state: TriageState) -> TriageState:
    """TODO: apply the triage policy to set `priority`, `route`, and `rationale`.

    Encode the priority and escalation rules from personas.md exactly. Note that
    the rules compose - read carefully which priority value each rule is meant to
    be evaluated against, because getting the order wrong changes the routing on
    some tickets.
    """
    raise NotImplementedError


def draft_node(state: TriageState) -> TriageState:
    """TODO: draft a short, on-brand reply for Marcus to approve.

    Do NOT promise a refund the policy has not approved. Acknowledge, state next step.
    """
    raise NotImplementedError


def escalate_node(state: TriageState) -> TriageState:
    """TODO: build an escalation summary for Priya (what, why, urgency)."""
    raise NotImplementedError


def build_graph():
    """TODO: wire classify -> route -> conditional edge to draft_node or escalate_node.

    With LangGraph: add nodes, set the entry point at classify, and add a conditional
    edge from route that branches on state['route'].
    """
    raise NotImplementedError


def run_all():
    """TODO: read orders_queue.csv, run every row through the graph, print a triage
    table (order_id, category, priority, route) and collect the rationales for audit.

    Keep the output machine-readable as well as human-readable - you will need to
    report per-category accuracy against orders_dev_labeled.csv, and your agent
    will be run against a further set of tickets you have not seen.
    """
    raise NotImplementedError


if __name__ == "__main__":
    run_all()
