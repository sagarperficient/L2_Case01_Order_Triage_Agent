"""Run the agent on the full 54-ticket queue and save results."""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from src.agent import run_all, evaluate


def main():
    print("=" * 80)
    print("FULL QUEUE RUN: Processing all 54 tickets")
    print("=" * 80)

    results = run_all()

    print(f"\nTotal tickets processed: {len(results)}")

    # Summary stats
    routes = {"marcus": 0, "priya": 0}
    priorities = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "URGENT": 0}
    for r in results:
        routes[r["route"]] = routes.get(r["route"], 0) + 1
        priorities[r["priority"]] = priorities.get(r["priority"], 0) + 1

    print(f"\nRouting: Marcus={routes['marcus']}, Priya={routes['priya']}")
    print(f"Priorities: {priorities}")

    # Show Priya's tickets (fraud/money-movement verification)
    print("\n" + "=" * 80)
    print("PRIYA'S ESCALATIONS (must include ALL fraud & payment_issue):")
    print("=" * 80)
    for r in results:
        if r["route"] == "priya":
            print(f"  {r['order_id']:12s} | {r['category']:20s} | {r['priority']:8s} | {r['rationale']}")

    # Run evaluation against dev set
    evaluate(results)

    # Flag edge-case tickets
    edge_cases = ["ORD-10047", "ORD-10048", "ORD-10049", "ORD-10050",
                  "ORD-10051", "ORD-10052", "ORD-10053", "ORD-10054"]
    print("\n" + "=" * 80)
    print("EDGE CASE TICKETS:")
    print("=" * 80)
    for r in results:
        if r["order_id"] in edge_cases:
            print(f"\n  {r['order_id']} (tier={r['customer_tier']})")
            print(f"    Category: {r['category']}")
            print(f"    Priority: {r['priority']}")
            print(f"    Route:    {r['route']}")
            print(f"    Rationale: {r['rationale']}")


if __name__ == "__main__":
    main()
