# Kaggriculture FarmOps Guardian Agent

Capstone submission package for the **5-Day AI Agents: Intensive Vibe Coding Course With Google**.

## Project summary

FarmOps Guardian is an autonomous resource-management agent for the Kaggriculture farming simulation. It decides the best daily farm action: **IRRIGATE**, **INSPECT**, **FERTILIZE**, **HARVEST**, or **WAIT**.

The agent uses:
- an ADK-style multi-agent architecture,
- a local MCP server exposing farm tools,
- deterministic safety guardrails,
- memory and trace logging,
- scenario evaluation,
- deployment-ready project structure.

## Capstone requirement mapping

| Requirement / concept | Where it is demonstrated |
|---|---|
| Agent / multi-agent system using ADK | `farmops_guardian/adk_agent.py` and notebook section 4 |
| MCP Server | `farmops_guardian/mcp_server.py` |
| Security features | `farmops_guardian/guardrails.py` |
| Agent skills / tools | `farmops_guardian/tools.py` |
| Context and memory | `farmops_guardian/memory.py` |
| Evaluation and observability | `farmops_guardian/evaluation.py` and notebook sections 7 to 9 |
| Deployability | `Dockerfile`, `app.py`, and `DEPLOYMENT_NOTES.md` |
| Writeup | `KAGGLE_WRITEUP.md` |
| Video demo | `VIDEO_SCRIPT.md` |

## How to run locally

```bash
pip install -r requirements.txt
python -m farmops_guardian.evaluation
python app.py
```

The notebook is designed to run without external API keys. The ADK and MCP files are included to show the production-ready architecture and can be activated by installing the optional dependencies.

## Recommended Kaggle submission flow

1. Upload `FarmOps_Guardian_Submission_Notebook.ipynb` to Kaggle as a notebook.
2. Run all cells.
3. Save and publish the notebook publicly.
4. Create a public GitHub repository with this package.
5. Record a video under 5 minutes using `VIDEO_SCRIPT.md`.
6. Submit the Kaggle writeup using `KAGGLE_WRITEUP.md`.
