import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(PROJECT_DIR, "agents")
sys.path.insert(0, AGENTS_DIR)

from agents.analyst_agent import run_analyst  # noqa: E402

BRIEF_PATH = os.path.join(PROJECT_DIR, "brief.txt")
ARTIFACTS_DIR = os.path.join(PROJECT_DIR, "artifacts")
OUTPUT_PATH = os.path.join(ARTIFACTS_DIR, "requirements.json")

REQUIRED_KEYS = {"goal", "allowed_actions", "safe_stop", "avoid_obstacles"}
VALID_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}


def test_analyst():
    with open(BRIEF_PATH, "r", encoding="utf-8") as f:
        brief_text = f.read()

    requirements = run_analyst(brief_text)

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(requirements, f, indent=4, ensure_ascii=False)

    assert os.path.exists(OUTPUT_PATH), "requirements.json was not created"

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert set(saved.keys()) == REQUIRED_KEYS, (
        f"keys must be exactly {sorted(REQUIRED_KEYS)}, got {sorted(saved.keys())}"
    )
    assert isinstance(saved["goal"], str) and saved["goal"].strip(), (
        "'goal' must be a non-empty string"
    )
    assert isinstance(saved["safe_stop"], bool), "'safe_stop' must be a boolean"
    assert isinstance(saved["avoid_obstacles"], bool), (
        "'avoid_obstacles' must be a boolean"
    )
    assert isinstance(saved["allowed_actions"], list), (
        "'allowed_actions' must be a list"
    )
    assert all(a in VALID_ACTIONS for a in saved["allowed_actions"]), (
        f"actions must be within {sorted(VALID_ACTIONS)}"
    )

    print(json.dumps(saved, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test_analyst()
    print("test_analyst PASSED")
