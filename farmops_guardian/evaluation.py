import pandas as pd
from .models import FarmState
from .agent_core import FarmOpsGuardianAgent

def demo_scenarios():
    return [
        FarmState(day=1, crop="tomato", growth_stage="vegetative", soil_moisture_pct=28, temperature_c=35, rain_forecast_mm=0, disease_signals=0, water_available_liters=800, budget_usd=120, crop_maturity_pct=20),
        FarmState(day=2, crop="tomato", growth_stage="flowering", soil_moisture_pct=67, temperature_c=27, rain_forecast_mm=8, disease_signals=3, water_available_liters=600, budget_usd=80, crop_maturity_pct=55),
        FarmState(day=3, crop="tomato", growth_stage="mature", soil_moisture_pct=58, temperature_c=24, rain_forecast_mm=5, disease_signals=0, water_available_liters=500, budget_usd=100, crop_maturity_pct=94),
        FarmState(day=4, crop="tomato", growth_stage="seedling", soil_moisture_pct=30, temperature_c=33, rain_forecast_mm=0, disease_signals=0, water_available_liters=10, budget_usd=90, crop_maturity_pct=5),
        FarmState(day=5, crop="tomato", growth_stage="vegetative", soil_moisture_pct=70, temperature_c=26, rain_forecast_mm=10, disease_signals=0, water_available_liters=700, budget_usd=10, crop_maturity_pct=30),
    ]

def run_evaluation():
    agent = FarmOpsGuardianAgent()
    results = [agent.run(s) for s in demo_scenarios()]
    expected = {
        1: "IRRIGATE",
        2: "INSPECT",
        3: "HARVEST",
        4: "INSPECT",
        5: "WAIT",
    }

    rows = []
    for row in results:
        day = row["day"]
        rows.append({
            "day": day,
            "expected_action": expected[day],
            "final_action": row["final_action"],
            "passed": row["final_action"] == expected[day],
            "guardrails": row["guardrails"],
        })

    eval_df = pd.DataFrame(rows)
    trace_df = agent.memory.as_dataframe()
    return eval_df, trace_df

if __name__ == "__main__":
    eval_df, trace_df = run_evaluation()
    print("Scenario accuracy:", eval_df["passed"].mean())
    print(eval_df.to_string(index=False))
