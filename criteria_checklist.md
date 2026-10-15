# Submission Checklist — L2_Case01_Order_Triage_Agent

## Deliverables

- [ ] Working LangGraph triage agent that processes all 54 tickets in `data/orders_queue.csv` end-to-end.
- [ ] Per-ticket audit record: category, priority, route, and a one-line rationale.
- [ ] Evaluation output: per-category accuracy against `data/orders_dev_labeled.csv`, plus your own assessment of the queue tickets the dev subset does not cover.
- [ ] Confirmation that every money-movement and fraud ticket reached Priya, with the evidence.
- [ ] At least two tickets your agent got wrong or found genuinely hard, with your analysis of why.
- [ ] A documented rule for any case the policy does not decide, applied consistently, and the list of tickets it applied to.
- [ ] `REFLECTION.md`, 600-1000 words, six sections: what was built · why · what failed · how you fixed it · what you'd do differently · business impact.
- [ ] `pytest-asyncio` suite covering the agent loop, tool mocking, and failure paths, with passing output included.
- [ ] The drafting or lookup step exposed as a callable tool, and the code structured so a new category or route can be added without rewriting the graph.
- [ ] Observability evidence: Portkey traces and/or LangSmith step traces for your runs.
- [ ] A demo (recording or transcript) showing one drafted reply and one escalation.
- [ ] Declared-effort statement: approximate hours and what you cut.

## Evidence standard

Every claim cites a ticket id, a category, or a measured number. "The agent
handles edge cases well" scores nothing. A claim of the form "ticket &lt;id&gt;
describes two issues; my rule assigns &lt;category&gt; because it carries the higher
base priority, and I applied that same rule to &lt;other id&gt;" scores — with the
real ids from your own run.

Note that `orders_queue.csv` has **no labels**. Any accuracy figure you report
for the full queue must explain how you established ground truth. Reporting high
accuracy on unlabeled data without explaining your method reads as an
unsupported claim.

## Before you submit — challenge your own work

- [ ] Have I solved the actual business problem, or only made the graph run?
- [ ] Can I explain every significant decision and the alternatives I rejected?
- [ ] **Have I checked how my agent behaves on tickets that are not straightforward?** The dev subset covers ordinary cases. The queue contains harder ones — tickets with almost no text, tickets whose tone does not match their severity, tickets describing more than one problem, and tickets where the customer expresses an opinion about how their ticket should be handled. Find them.
- [ ] Do the priority and escalation rules compose correctly in my implementation? Trace one premium ticket at each base priority level by hand and confirm the routing matches the policy exactly.
- [ ] Is there any ticket where my agent's decision was driven by something other than the facts of the complaint and the documented policy?
- [ ] Does my rationale trail let Dev see not just what was decided, but anything unusual about how the ticket was written?

## How this will be assessed

Your agent is run against a **held-out batch of tickets you have not seen** —
unlabeled, drawn from the same queue population, and including case types the dev
subset does not cover. Accuracy on the dev subset alone is not sufficient
evidence.

Your self-reported evaluation numbers are compared against the grader's own run
of your agent. Divergence counts against the evaluation dimension.

You will also answer several questions about your own submission at submission
time. They reference specific tickets and decisions in this case, so they cannot
be prepared in advance.
