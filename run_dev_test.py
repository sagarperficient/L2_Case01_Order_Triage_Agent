"""Quick test: run the agent on the first 3 dev-labeled tickets to verify the pipeline."""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from src.agent import build_graph
from src.models import TriageState
import pandas as pd
from src.config import DEV_LABELED

def main():
    app = build_graph()
    dev_df = pd.read_csv(DEV_LABELED)

    # Test on all dev-labeled tickets
    test_rows = dev_df

    print("=" * 80)
    print("DEV TEST: Running agent on first 3 labeled tickets")
    print("=" * 80)

    for _, row in test_rows.iterrows():
        input_state: TriageState = {
            "order_id": row["order_id"],
            "customer_tier": row["customer_tier"],
            "text_note": row["text_note"],
            "status": row["status"],
        }

        print(f"\n--- {row['order_id']} ---")
        print(f"  Text: {row['text_note'][:80]}...")
        print(f"  Expected: cat={row['issue_type']}, pri={row['priority']}, route={row['route']}")

        try:
            output = app.invoke(input_state)
            cat_match = "✓" if output["category"] == row["issue_type"] else "✗"
            pri_match = "✓" if output["priority"].upper() == row["priority"].upper() else "✗"
            route_match = "✓" if output["route"] == row["route"] else "✗"

            print(f"  Got:      cat={output['category']} {cat_match}, pri={output['priority']} {pri_match}, route={output['route']} {route_match}")
            print(f"  Rationale: {output['rationale']}")

            if output.get("draft_reply"):
                print(f"  Draft: {output['draft_reply'][:100]}...")
            if output.get("escalation_summary"):
                print(f"  Escalation: {output['escalation_summary'][:100]}...")

        except Exception as e:
            print(f"  ERROR: {e}")

    print("\n" + "=" * 80)
    print("Pipeline test complete.")


if __name__ == "__main__":
    main()
