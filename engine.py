import os
import json
import pandas as pd

def min_max(series):
    min_val = series.min()
    max_val = series.max()

    if min_val == max_val:
        return pd.Series([0.0] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val)


class RubiesEngine:
    """
    Rule-based, deterministic customer scoring engine.
    No AI, no ML, no learning.
    """

    def __init__(self, config_path=None):
        # If no path provided, use rubies_config.json in the same folder as this file
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "rubies_config.json")

        # Open the JSON safely
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path) as f:
            cfg = json.load(f)

        self.weights = cfg["weights"]
        self.tiers = dict(
            sorted(cfg["tiers"].items(), key=lambda x: x[1], reverse=True)
        )

    def calculate_scores(self, df):
        df = df.copy()

        df["s_norm"] = min_max(df["savings"])
        df["b_norm"] = min_max(df["balance"])
        df["t_norm"] = min_max(df["transactions"])
        df["c_norm"] = min_max(df["card_usage"])

        df["rubies_score"] = (
            df["s_norm"] * self.weights["savings"]
            + df["b_norm"] * self.weights["balance"]
            + df["t_norm"] * self.weights["transactions"]
            + df["c_norm"] * self.weights["card_usage"]
        ) * 100

        return df

    def assign_tier(self, score):
        for tier, threshold in self.tiers.items():
            if score >= threshold:
                return tier
        return "Unranked"

    def rank_customers(self, df):
        df = df.sort_values("rubies_score", ascending=False).reset_index(drop=True)
        df["rank_current"] = df.index + 1
        df["tier"] = df["rubies_score"].apply(self.assign_tier)
        return df

