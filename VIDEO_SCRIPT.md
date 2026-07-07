# Demo video script, under 5 minutes

Hi, my capstone project is Kaggriculture FarmOps Guardian Agent.

The problem is daily farm resource management. In a farming simulation, the agent needs to decide whether to irrigate, inspect, fertilize, harvest, or wait. That decision depends on crop maturity, soil moisture, weather risk, disease signals, water availability, budget, and previous actions.

The agent follows an observe, tool, plan, validate, remember, and evaluate loop.

First, it observes the farm state. Then it calls tools for irrigation need, weather risk, disease risk, action cost, and expected yield impact. After that, the planner recommends one action. Before the action is returned, a guardrail layer validates it. Finally, the system stores a trace in memory and evaluates the decision.

This project demonstrates the course concepts in several ways.

First, it includes an ADK-style multi-agent design. There is a coordinator agent, an agronomy specialist, and a resource specialist. The coordinator chooses the final action.

Second, it includes an MCP server. The farm tools can be exposed as MCP tools, which makes the design more interoperable.

Third, it includes security guardrails. For example, the system blocks irrigation when there is not enough water, blocks harvest if the crop is not mature, blocks actions that exceed budget, and only allows actions from a fixed action list.

Fourth, it includes memory and observability. Every run logs the farm state, tool results, proposed action, final action, rationale, and guardrail decision.

Now I will show the notebook.

In scenario one, the soil is very dry and the weather is hot, so the agent selects irrigation.

In scenario two, disease signals are high, so the agent selects inspection.

In scenario three, the crop is mature and the budget allows it, so the agent selects harvest.

In scenario four, the planner wants irrigation because the soil is dry, but the guardrail blocks irrigation because water availability is too low. The final action becomes inspection.

In scenario five, budget is very limited, so the agent waits instead of taking an expensive action.

At the end, the notebook shows evaluation accuracy and the trace log. This proves the system is not just producing text. It is making decisions, using tools, applying safety rules, keeping memory, and recording observable behavior.

For production, I would connect it to real weather APIs and farm sensors, use Gemini through Google ADK for natural-language reasoning, keep guardrails outside the model, and deploy the FastAPI version as a containerized service.

That is FarmOps Guardian, an autonomous, guardrailed farm resource-management agent for Kaggriculture.
