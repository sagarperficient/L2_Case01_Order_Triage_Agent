"""Callable tools: draft reply and ticket lookup exposed as LangChain tools."""

from langchain_core.tools import tool
from src.agent import build_graph
from src.models import TriageState


@tool
def draft_reply(order_id: str, customer_tier: str, text_note: str, status: str = "new") -> str:
    """Draft a customer reply for a given ticket by running it through the full triage pipeline.

    Returns the draft reply text if routed to Marcus, or the escalation summary if routed to Priya.
    """
    app = build_graph()

    input_state: TriageState = {
        "order_id": order_id,
        "customer_tier": customer_tier,
        "text_note": text_note,
        "status": status,
    }

    output = app.invoke(input_state)

    if output.get("draft_reply"):
        return f"[Route: Marcus] Draft Reply:\n{output['draft_reply']}"
    else:
        return f"[Route: Priya] Escalation Summary:\n{output.get('escalation_summary', 'N/A')}"


@tool
def lookup_ticket(order_id: str) -> str:
    """Look up a previously triaged ticket's results from the output file.

    Returns category, priority, route, and rationale for the given order_id.
    """
    import pandas as pd
    from src.config import OUTPUT_DIR

    results_path = OUTPUT_DIR / "triage_results.csv"
    if not results_path.exists():
        return f"No results file found. Run the agent first."

    df = pd.read_csv(results_path)
    match = df[df["order_id"] == order_id]

    if match.empty:
        return f"Order {order_id} not found in results."

    row = match.iloc[0]
    return (
        f"Order: {row['order_id']}\n"
        f"Category: {row['category']}\n"
        f"Priority: {row['priority']}\n"
        f"Route: {row['route']}\n"
        f"Rationale: {row['rationale']}"
    )
