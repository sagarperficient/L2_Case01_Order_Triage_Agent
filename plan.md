# Implementation Plan — L2_Case01_Order_Triage_Agent

## Project Summary

An **Order Triage Agent** for NorthPeak Commerce (fictional retailer) using **LangGraph**. The agent processes 54 support tickets through a pipeline: **classify → route → (draft reply | escalate)**. It follows a strict triage policy from `data/personas.md`, produces audit trails, and handles adversarial edge cases.

## Key Observations

| Aspect | Detail |
|--------|--------|
| **Stack** | LangGraph + LangChain + one LLM provider (OpenAI or Anthropic) |
| **Data** | 54 unlabeled tickets in `orders_queue.csv`, 12 labeled in `orders_dev_labeled.csv` |
| **Graph** | `classify_node` → `route_node` → conditional edge → `draft_node` OR `escalate_node` |
| **Tricky tickets** | Prompt injection (ORD-10047–10050), multi-issue (ORD-10052), sarcasm (ORD-10053), minimal text (ORD-10054), priority manipulation (ORD-10051) |

---

## Phase 1: Setup & Configuration      -- DONE

1. **Create a virtual environment** and install dependencies from `starter/requirements.txt`.
2. **Choose an LLM provider** — add `openai` or `anthropic` to requirements.
3. **Create a `.env` file** with your API key (+ optionally Portkey/LangSmith keys for observability).
4. **Add additional dependencies**: `pytest-asyncio`, `portkey-ai` or `langsmith` for tracing.

---

## Phase 2: Core Agent Implementation

5. **Implement `classify_node`** — Use an LLM call with a constrained enum output to classify `text_note` into one of the 10 categories. Prompt should include the full category list and the "Authority" section (ignore customer attempts to direct handling).

6. **Implement `route_node`** — Pure logic, no LLM needed:
   - Look up the base priority from the category table.
   - Apply the premium-tier bump (+1 rung if `customer_tier == "premium"`, capped at URGENT).
   - Route: `fraud_alert` or `payment_issue` → Priya; premium + HIGH/URGENT → Priya; else → Marcus.
   - Write a one-line rationale.

7. **Implement `draft_node`** — LLM call to write a short, empathetic customer reply. Must not promise refunds. Acknowledge → state next step → done.

8. **Implement `escalate_node`** — LLM call to summarize for Priya: what happened, why it's escalated, urgency level.

9. **Implement `build_graph`** — Wire the LangGraph:
   ```
   classify → route → conditional_edge(route == "priya" ? escalate : draft) → END
   ```

10. **Implement `run_all`** — Read CSV with pandas, invoke graph per row, collect results into a structured output (CSV/JSON for machine-readability + printed table for humans).

---

## Phase 3: Edge Cases & Policy Gaps

11. **Handle prompt injection tickets** (ORD-10047–10050) — The "Authority" section is clear: `text_note` is DATA, not instruction. Classify prompt must be hardened against this. Note the attempt in the rationale.

12. **Handle multi-issue tickets** (ORD-10052) — Define and document a consistent rule (e.g., assign the category with the higher base priority). Apply uniformly.

13. **Handle minimal-text tickets** (ORD-10054: "Fit?") — Classify based on best-effort interpretation; note uncertainty in rationale.

14. **Handle sarcasm/tone mismatch** (ORD-10053) — Classify from facts, not tone.

15. **Handle customer priority manipulation** (ORD-10051) — Classify from facts (subscription pause), ignore the "urgent fraud" framing.

---

## Phase 4: Evaluation

16. **Run against dev labeled set** — Compare agent output to the 12 labeled rows. Report per-category accuracy.

17. **Evaluate full queue** — Since it's unlabeled, manually review a sample or use a second LLM-as-judge pass. Document methodology for establishing ground truth.

18. **Verify money-movement/fraud routing** — Confirm every `fraud_alert` and `payment_issue` ticket reached Priya with evidence (ticket IDs).

19. **Identify 2+ hard/wrong tickets** — Analyze why the agent struggled.

---

## Phase 5: Testing & Observability

20. **Write `pytest-asyncio` tests** — Cover:
    - Full agent loop (end-to-end on a sample ticket).
    - Tool mocking (mock LLM calls, assert graph flow).
    - Failure paths (malformed input, empty text_note, unknown tier).

21. **Add observability** — Integrate Portkey or LangSmith tracing. Capture step-level traces for at least one full run.

22. **Expose draft/lookup as a callable tool** — Structure the drafting step so it can be invoked independently (e.g., as a LangChain tool).

---

## Phase 6: Documentation & Deliverables

23. **Write `REFLECTION.md`** (600–1000 words, 6 sections): what was built, why, what failed, how you fixed it, what you'd do differently, business impact.

24. **Record a demo** — Show one drafted reply (Marcus path) and one escalation (Priya path).

25. **Add declared-effort statement** — Approximate hours and what you cut.

26. **Ensure extensibility** — Structure code so adding a new category or route doesn't require rewriting the graph (data-driven routing from personas.md).

---

## Suggested File Structure

```
├── data/
│   ├── orders_queue.csv
│   ├── orders_dev_labeled.csv
│   └── personas.md
├── src/
│   ├── agent.py          # Main graph (classify, route, draft, escalate)
│   ├── config.py         # LLM setup, env vars
│   ├── models.py         # TriageState, enums for categories/priorities
│   └── tools.py          # Callable draft/lookup tool
├── tests/
│   └── test_agent.py     # pytest-asyncio suite
├── output/
│   ├── triage_results.csv
│   └── evaluation.md
├── REFLECTION.md
├── .env
└── requirements.txt
```

---

## Critical Design Decisions (Decide Early)

1. **LLM provider** — OpenAI (gpt-4o) or Anthropic (Claude) for classify/draft nodes.
2. **Multi-issue rule** — Higher-priority category wins? Or escalate if either warrants it?
3. **Prompt injection defense** — System prompt hardening vs. output validation vs. both.
4. **Ground truth method for unlabeled tickets** — Manual review, LLM-as-judge, or both.
