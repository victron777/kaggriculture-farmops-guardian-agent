"""
Minimal MCP server exposing FarmOps tools.

Run:
    pip install mcp
    python -m farmops_guardian.mcp_server

This demonstrates the MCP Server requirement. The notebook does not need to run this server.
"""

try:
    from mcp.server.fastmcp import FastMCP
except Exception:
    FastMCP = None

from .models import FarmState
from .tools import estimate_irrigation_need, estimate_weather_risk, estimate_disease_risk, estimate_action_cost

if FastMCP is not None:
    mcp = FastMCP("farmops-guardian-mcp")

    @mcp.tool()
    def irrigation_need(
        day: int,
        crop: str,
        growth_stage: str,
        soil_moisture_pct: float,
        temperature_c: float,
        rain_forecast_mm: float,
        disease_signals: int,
        water_available_liters: float,
        budget_usd: float,
        crop_maturity_pct: float,
    ) -> dict:
        state = FarmState(day, crop, growth_stage, soil_moisture_pct, temperature_c, rain_forecast_mm, disease_signals, water_available_liters, budget_usd, crop_maturity_pct)
        return estimate_irrigation_need(state)

    @mcp.tool()
    def weather_risk(
        day: int,
        crop: str,
        growth_stage: str,
        soil_moisture_pct: float,
        temperature_c: float,
        rain_forecast_mm: float,
        disease_signals: int,
        water_available_liters: float,
        budget_usd: float,
        crop_maturity_pct: float,
    ) -> dict:
        state = FarmState(day, crop, growth_stage, soil_moisture_pct, temperature_c, rain_forecast_mm, disease_signals, water_available_liters, budget_usd, crop_maturity_pct)
        return estimate_weather_risk(state)

    @mcp.tool()
    def disease_risk(
        day: int,
        crop: str,
        growth_stage: str,
        soil_moisture_pct: float,
        temperature_c: float,
        rain_forecast_mm: float,
        disease_signals: int,
        water_available_liters: float,
        budget_usd: float,
        crop_maturity_pct: float,
    ) -> dict:
        state = FarmState(day, crop, growth_stage, soil_moisture_pct, temperature_c, rain_forecast_mm, disease_signals, water_available_liters, budget_usd, crop_maturity_pct)
        return estimate_disease_risk(state)

if __name__ == "__main__":
    if FastMCP is None:
        print("MCP dependency not installed. Run: pip install mcp")
    else:
        mcp.run()
