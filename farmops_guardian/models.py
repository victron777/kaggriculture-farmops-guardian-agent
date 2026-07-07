from dataclasses import dataclass, asdict
from typing import Dict, Any

ALLOWED_ACTIONS = {"IRRIGATE", "INSPECT", "FERTILIZE", "HARVEST", "WAIT"}

@dataclass
class FarmState:
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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
