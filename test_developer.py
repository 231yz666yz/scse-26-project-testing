import importlib.util
import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(PROJECT_DIR, "agents")
sys.path.insert(0, AGENTS_DIR)

from agents.developer_agent import run_developer  # noqa: E402

ARTIFACTS_DIR = os.path.join(PROJECT_DIR, "artifacts")
PLAN_PATH = os.path.join(ARTIFACTS_DIR, "plan.json")
GENERATED_DIR = os.path.join(PROJECT_DIR, "generated")
OUTPUT_PATH = os.path.join(GENERATED_DIR, "navigation_logic.py")

VALID_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}

SAMPLE_STATE = {
    "goal_ahead": True,
    "goal_on_left": False,
    "goal_on_right": False,
    "front_blocked": False,
    "left_blocked": False,
    "right_blocked": False,
}


def test_developer():
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        plan = json.load(f)

    code = run_developer(plan)

    os.makedirs(GENERATED_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    assert os.path.exists(OUTPUT_PATH), "navigation_logic.py was not created"

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        saved_code = f.read()

    compile(saved_code, filename=OUTPUT_PATH, mode="exec")

    assert "def decide_next_move" in saved_code, (
        "generated code must define decide_next_move(state)"
    )

    spec = importlib.util.spec_from_file_location("navigation_logic", OUTPUT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(getattr(module, "decide_next_move", None)), (
        "decide_next_move must be callable after importing the module"
    )

    action = module.decide_next_move(dict(SAMPLE_STATE))
    assert action in VALID_ACTIONS, f"{action!r} is not a valid action"

    print(saved_code)


if __name__ == "__main__":
    test_developer()
    print("test_developer PASSED")
