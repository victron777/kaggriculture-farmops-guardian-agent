from fastapi import FastAPI
from pydantic import BaseModel
from farmops_guardian.models import FarmState
from farmops_guardian.agent_core import FarmOpsGuardianAgent

app = FastAPI(title="FarmOps Guardian Agent")
agent = FarmOpsGuardianAgent()

class FarmStateRequest(BaseModel):
    day: int
    crop: str
    growth_stage: str
    soil_moisture_pct: float
    temperature_c: float
    rain_forecast_mm: float
    disease_signals: int
    water_available_liters: float
    budget_usd: float
    crop_maturity_pct: float
    last_action: str = "NONE"

@app.post("/decide")
def decide(request: FarmStateRequest):
    state = FarmState(**request.model_dump())
    return agent.run(state)

@app.get("/health")
def health():
    return {"status": "ok", "service": "farmops_guardian"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
