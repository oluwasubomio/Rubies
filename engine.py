import os
import json

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
