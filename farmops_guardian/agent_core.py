from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from .models import FarmState
from .tools import estimate_irrigation_need, estimate_weather_risk, estimate_disease_risk
from .guardrails import validate_action
from .memory import AgentMemory

class FarmOpsGuardianAgent:
    """Autonomous farm resource-management agent."""

    def __init__(self, memory: AgentMemory | None = None):
        self.memory = memory or AgentMemory()

    def observe(self, state: FarmState) -> Dict[str, Any]:
        return {
            "state": state.to_dict(),
            "recent_actions": self.memory.recent_actions()
        }

    def call_tools(self, state: FarmState) -> Dict[str, Any]:
        return {
            "irrigation": estimate_irrigation_need(state),
            "weather": estimate_weather_risk(state),
            "disease": estimate_disease_risk(state),
        }

    def plan(self, state: FarmState, tools: Dict[str, Any]) -> Tuple[str, str]:
        disease = tools["disease"]["risk"]
        weather = tools["weather"]["risk"]
        irrigation = tools["irrigation"]

        if state.crop_maturity_pct >= 90 and state.budget_usd >= 75:
            return "HARVEST", "Crop maturity is high and budget allows harvest."

        if irrigation["urgency"] == "high":
            return "IRRIGATE", "Soil moisture is low and rain forecast is limited."

        if disease == "high":
            return "INSPECT", "Disease signal is high, so inspection is needed before treatment."

        if state.growth_stage in ["vegetative", "flowering"] and state.budget_usd >= 40 and disease != "high":
            return "FERTILIZE", "Growth stage is appropriate and budget allows fertilization."

        if weather == "high":
            return "IRRIGATE", "Weather risk suggests preventing crop stress."

        return "WAIT", "Conditions are stable, so waiting avoids unnecessary cost."

    def run(self, state: FarmState) -> Dict[str, Any]:
        observation = self.observe(state)
        tools = self.call_tools(state)
        proposed_action, rationale = self.plan(state, tools)
        final_action, guardrail_reasons = validate_action(
            proposed_action,
            state,
            tools,
            self.memory.recent_actions()
        )

        trace = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "day": state.day,
            "crop": state.crop,
            "growth_stage": state.growth_stage,
            "soil_moisture_pct": state.soil_moisture_pct,
            "rain_forecast_mm": state.rain_forecast_mm,
            "disease_signals": state.disease_signals,
            "budget_usd": state.budget_usd,
            "proposed_action": proposed_action,
            "final_action": final_action,
            "rationale": rationale,
            "guardrails": " | ".join(guardrail_reasons),
            "tool_results": tools,
            "observation": observation,
        }
        self.memory.remember(trace)
        return trace
