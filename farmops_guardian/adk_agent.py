"""
ADK implementation sketch for the capstone.

This file demonstrates the Agent / Multi-agent system requirement using Google ADK.
It is intentionally separated from the notebook so the notebook can run without API keys.
To activate it, install google-adk and set GOOGLE_API_KEY or use Vertex AI credentials.
"""

from .tools import estimate_irrigation_need, estimate_weather_risk, estimate_disease_risk, estimate_action_cost, estimate_yield_impact

try:
    from google.adk.agents import Agent
except Exception:  # Keeps the repository import-safe when ADK is not installed.
    Agent = None

ROOT_INSTRUCTION = """
You are FarmOps Guardian, an autonomous Kaggriculture farm operations coordinator.
Choose exactly one allowed action: IRRIGATE, INSPECT, FERTILIZE, HARVEST, or WAIT.
Use tools before deciding. Explain the reason briefly.
Do not recommend unsafe actions. Guardrails outside the LLM will validate the decision.
"""

def build_adk_agent(model: str = "gemini-2.5-flash-lite"):
    if Agent is None:
        raise ImportError("google-adk is not installed. Install it with: pip install google-adk")

    agronomy_agent = Agent(
        name="agronomy_agent",
        model=model,
        description="Assesses crop growth, disease risk, and yield impact.",
        instruction="Use disease and yield tools to recommend crop-health actions.",
        tools=[estimate_disease_risk, estimate_yield_impact],
    )

    resource_agent = Agent(
        name="resource_agent",
        model=model,
        description="Assesses water and budget constraints.",
        instruction="Use irrigation and cost tools to recommend resource-safe actions.",
        tools=[estimate_irrigation_need, estimate_action_cost],
    )

    root_agent = Agent(
        name="farmops_guardian",
        model=model,
        description="Coordinator agent for daily farm resource decisions.",
        instruction=ROOT_INSTRUCTION,
        tools=[
            estimate_irrigation_need,
            estimate_weather_risk,
            estimate_disease_risk,
            estimate_action_cost,
            estimate_yield_impact,
        ],
        sub_agents=[agronomy_agent, resource_agent],
    )

    return root_agent
