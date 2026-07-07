from typing import Dict, Any, List, Tuple
from .models import FarmState, ALLOWED_ACTIONS
from .tools import estimate_action_cost

def validate_action(action: str, state: FarmState, tool_results: Dict[str, Any], recent_actions: List[str]) -> Tuple[str, List[str]]:
    """Validate and possibly override an agent action using deterministic safety policies."""
    reasons: List[str] = []
    final_action = action

    if action not in ALLOWED_ACTIONS:
        return "WAIT", [f"Blocked unknown action: {action}."]

    cost = estimate_action_cost(action, state)["cost_usd"]
    irrigation = tool_results["irrigation"]

    if cost > state.budget_usd:
        reasons.append(f"Blocked {action}: cost ${cost} exceeds budget ${state.budget_usd}.")
        final_action = "WAIT"

    if action == "IRRIGATE" and irrigation["liters_needed"] > state.water_available_liters:
        reasons.append("Blocked IRRIGATE: not enough water available.")
        final_action = "INSPECT"

    if action == "HARVEST" and state.crop_maturity_pct < 90:
        reasons.append("Blocked HARVEST: crop maturity is below 90%.")
        final_action = "WAIT"

    if action == "FERTILIZE" and state.growth_stage not in ["vegetative", "flowering"]:
        reasons.append("Blocked FERTILIZE: crop is not in the correct growth stage.")
        final_action = "WAIT"

    if recent_actions.count("IRRIGATE") >= 2 and action == "IRRIGATE":
        reasons.append("Blocked IRRIGATE: too many recent irrigation actions.")
        final_action = "INSPECT"

    if not reasons:
        reasons.append("Action passed guardrails.")

    return final_action, reasons
