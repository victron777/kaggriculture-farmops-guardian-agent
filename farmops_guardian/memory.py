from typing import Dict, Any, List
import pandas as pd

class AgentMemory:
    """Simple memory store for recent agent decisions and trace records."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def remember(self, record: Dict[str, Any]) -> None:
        self.history.append(record)

    def recent_actions(self, n: int = 3) -> List[str]:
        return [item["final_action"] for item in self.history[-n:]]

    def as_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.history)
