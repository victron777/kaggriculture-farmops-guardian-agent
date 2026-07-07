# Deployment Notes

This project is deployable as a containerized API.

## Local API

```bash
pip install -r requirements.txt
python app.py
```

Test:

```bash
curl -X POST http://localhost:8080/decide \
  -H "Content-Type: application/json" \
  -d '{"day":1,"crop":"tomato","growth_stage":"vegetative","soil_moisture_pct":28,"temperature_c":35,"rain_forecast_mm":0,"disease_signals":0,"water_available_liters":800,"budget_usd":120,"crop_maturity_pct":20}'
```

## Docker

```bash
docker build -t farmops-guardian .
docker run -p 8080:8080 farmops-guardian
```

## Production extension

- Replace synthetic farm state with real sensor and weather APIs.
- Route tool access through MCP.
- Use Google ADK with Gemini for natural-language reasoning.
- Keep deterministic guardrails outside the model.
- Log every observation, tool call, proposed action, final action, and guardrail override.
