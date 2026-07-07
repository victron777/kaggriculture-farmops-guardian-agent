from typing import Dict, Any
from .models import FarmState

def estimate_irrigation_need(state: FarmState) -> Dict[str, Any]:
    """Estimate liters needed and urgency based on soil moisture and rain forecast."""
    target = 65
    deficit = max(0, target - state.soil_moisture_pct)
    liters_needed = round(deficit * 12, 1)
    urgency = (
        "high" if state.soil_moisture_pct < 35 and state.rain_forecast_mm < 5
        else "medium" if state.soil_moisture_pct < 55
        else "low"
    )
    return {"liters_needed": liters_needed, "urgency": urgency}

def estimate_weather_risk(state: FarmState) -> Dict[str, Any]:
    """Estimate heat and drought risk."""
    heat_risk = state.temperature_c >= 32
    drought_risk = state.rain_forecast_mm < 3 and state.soil_moisture_pct < 45
    risk_score = int(heat_risk) + int(drought_risk)
    label = "high" if risk_score == 2 else "medium" if risk_score == 1 else "low"
    return {"risk": label, "heat_risk": heat_risk, "drought_risk": drought_risk}

def estimate_disease_risk(state: FarmState) -> Dict[str, Any]:
    """Estimate disease risk from field signals and wet weather."""
    score = min(100, state.disease_signals * 25 + (10 if state.rain_forecast_mm > 15 else 0))
    label = "high" if score >= 60 else "medium" if score >= 30 else "low"
    return {"score": score, "risk": label}

def estimate_action_cost(action: str, state: FarmState) -> Dict[str, Any]:
    """Estimate action cost and whether it is within budget."""
    base_costs = {
        "IRRIGATE": 15,
        "INSPECT": 10,
        "FERTILIZE": 40,
        "HARVEST": 75,
        "WAIT": 0,
    }
    cost = base_costs[action]
    return {"action": action, "cost_usd": cost, "within_budget": cost <= state.budget_usd}

def estimate_yield_impact(action: str, state: FarmState) -> Dict[str, Any]:
    """Estimate yield impact score for an action."""
    impact = 0
    if action == "IRRIGATE" and state.soil_moisture_pct < 55:
        impact += 18
    if action == "INSPECT" and state.disease_signals >= 2:
        impact += 12
    if action == "FERTILIZE" and state.growth_stage in ["vegetative", "flowering"]:
        impact += 15
    if action == "HARVEST" and state.crop_maturity_pct >= 90:
        impact += 25
    if action == "WAIT":
        impact += 2 if state.soil_moisture_pct >= 55 and state.disease_signals == 0 else -8
    return {"action": action, "yield_impact_score": impact}
