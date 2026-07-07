# Kaggriculture FarmOps Guardian Agent

## Project overview

FarmOps Guardian is an autonomous resource-management agent for the Kaggriculture farming simulation. The agent helps a farm decide the safest and highest-impact daily action: **IRRIGATE**, **INSPECT**, **FERTILIZE**, **HARVEST**, or **WAIT**.

The problem is that farm decisions are multi-variable. A good action depends on crop maturity, soil moisture, weather risk, disease signals, available water, budget, and previous actions. A normal chatbot can explain options, but an agent can observe state, call tools, reason over constraints, validate its decision, remember what happened, and produce an auditable trace.

## Agent goal

Given a daily farm state, FarmOps Guardian recommends one action that improves yield while respecting operational limits.

## Architecture

The system follows this loop:

1. Observe the farm state.
2. Call tools for irrigation need, weather risk, disease risk, action cost, and yield impact.
3. Plan a recommended action.
4. Validate the recommendation with deterministic guardrails.
5. Store the final action in memory.
6. Log the trace and evaluate the result against test scenarios.

The code separates the agent into clear modules:

- `models.py`: farm state schema and allowed actions.
- `tools.py`: agent skills for risk, cost, and yield calculations.
- `agent_core.py`: autonomous planner loop.
- `guardrails.py`: safety and feasibility checks.
- `memory.py`: recent action memory and trace history.
- `evaluation.py`: scenario-based tests.
- `adk_agent.py`: Google ADK-style multi-agent implementation.
- `mcp_server.py`: local MCP server exposing farm tools.
- `app.py` and `Dockerfile`: deployable API version.

## Course concepts demonstrated

### 1. Agent / multi-agent system using ADK

The project includes an ADK-style implementation with a coordinator agent and two specialist sub-agents: an agronomy agent and a resource agent. The coordinator decides the daily action, while the specialist agents focus on crop health, yield, water, and budget. This demonstrates a modular multi-agent pattern rather than one large monolithic prompt.

### 2. MCP server

The project includes an MCP server that exposes farm tools as callable capabilities. In a production version, ADK or another agent runtime could call these tools through MCP instead of directly importing Python functions. This makes the design more interoperable and easier to extend.

### 3. Security features and guardrails

The guardrail layer blocks unsafe or impossible actions. It prevents irrigation when water is insufficient, harvest when the crop is not mature, fertilization at the wrong growth stage, actions that exceed budget, unknown actions, and repeated irrigation patterns. The important design choice is that guardrails live outside the model, so even a wrong model recommendation is validated before execution.

### 4. Context, memory, and observability

The agent maintains memory of recent actions and stores a trace for each run. Each trace includes the input state, tool outputs, proposed action, final action, rationale, and guardrail result. This makes the agent easier to debug and evaluate.

### 5. Evaluation

The notebook includes five scenarios. The expected outcomes verify that the agent irrigates when soil is dry, inspects when disease risk is high, harvests when the crop is mature, blocks irrigation when water is insufficient, and waits when budget prevents action. The evaluation reports scenario accuracy and prints the trace log.

### 6. Deployability

The project includes a FastAPI wrapper and Dockerfile. The same decision engine can run as a local notebook, command-line script, containerized API, or future managed service.

## Why this is an agent

FarmOps Guardian is not only a rules script. It has an agentic loop: observe, use tools, plan, validate, remember, and evaluate. It can adapt to different scenarios while keeping actions inside safety and resource constraints.

## Example behavior

In a dry-soil scenario, the agent proposes **IRRIGATE** and the guardrail allows it because enough water is available. In a high-disease-risk scenario, the agent chooses **INSPECT** before spending money on treatment. In a mature-crop scenario, the agent chooses **HARVEST**. In a low-water scenario, the planner may propose irrigation, but the guardrail blocks it and changes the action to **INSPECT**.

## Future improvements

The next version would connect to real weather APIs, soil sensors, and Gemini-powered planning through Google ADK. It could also add a farmer dashboard, long-term memory, reinforcement learning for season-level optimization, and cloud observability for production monitoring.

## Submission links

- Code repository: replace with your public GitHub link.
- Kaggle notebook: replace with your published Kaggle notebook link.
- Demo video: replace with your public YouTube or accessible video link.
