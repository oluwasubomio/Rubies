import os
import pandas as pd
from engine import RubiesEngine

engine = RubiesEngine()

def load_week(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    fallback = "rubies_mock_data.csv"
    if os.path.exists(fallback):
        return pd.read_csv(fallback)
    raise FileNotFoundError(f"Neither {path} nor {fallback} were found.")

week1 = load_week("data/week_1.csv")
week2 = load_week("data/week_2.csv")

w1 = engine.finalize(engine.score(week1))
w2 = engine.finalize(engine.score(week2))

w1_renamed = w1[["customer_id", "rank_current"]].rename(columns={"rank_current": "rank_prev"})

movement = w2.merge(
    w1_renamed,
    on="customer_id"
)

movement["movement"] = movement["rank_prev"] - movement["rank_current"]

def arrow(x):
    if x > 0:
        return "↑"
    if x < 0:
        return "↓"
    return "→"

movement["trend"] = movement["movement"].apply(arrow)

movement.to_json("rubies_output.json", orient="records", indent=2)
print("Rubies output with week-over-week movement generated.")
