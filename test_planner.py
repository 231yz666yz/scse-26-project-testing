import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(PROJECT_DIR, "agents")
sys.path.insert(0, AGENTS_DIR)

from agents.planner_agent import run_planner  # noqa: E402

ARTIFACTS_DIR = os.path.join(PROJECT_DIR, "artifacts")
REQ_PATH = os.path.join(ARTIFACTS_DIR, "requirements.json")
OUTPUT_PATH = os.path.join(ARTIFACTS_DIR, "plan.json")

REQUIRED_KEYS = {"strategy", "decisions", "stop_point"}
VALID_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}


def test_planner():
    with open(REQ_PATH, "r", encoding="utf-8") as f:
        requirements = json.load(f)

    plan = run_planner(requirements)

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=4, ensure_ascii=False)

    assert os.path.exists(OUTPUT_PATH), "plan.json was not created"

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert set(saved.keys()) == REQUIRED_KEYS, (
        f"keys must be exactly {sorted(REQUIRED_KEYS)}, got {sorted(saved.keys())}"
    )
    assert isinstance(saved["strategy"], str) and saved["strategy"].strip(), (
        "'strategy' must be a non-empty string"
    )
    assert isinstance(saved["decisions"], list) and saved["decisions"], (
        "'decisions' must be a non-empty list"
    )
    assert all(isinstance(d, str) and d.strip() for d in saved["decisions"]), (
        "every decision must be a non-empty string"
    )
    assert isinstance(saved["stop_point"], str) and saved["stop_point"].strip(), (
        "'stop_point' must be a non-empty string"
    )

    for d in saved["decisions"]:
        assert any(a in d.upper() for a in VALID_ACTIONS), (
            f"decision references no valid action: {d!r}"
        )

    if requirements.get("safe_stop"):
        assert any("STOP" in d.upper() for d in saved["decisions"]), (
            "requirements.safe_stop is true but no decision uses STOP"
        )

    print(json.dumps(saved, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test_planner()
    print("test_planner PASSED")
