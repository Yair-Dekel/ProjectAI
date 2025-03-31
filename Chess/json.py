import json

# Simulate pawn report
positions = {"x": 5, "y": 6, "x_w_king": 5, "y_w_king": 7, "x_b_king": 5, "y_b_king": 5,"x_pawn": 5, "y_pawn": 6}
pawn_report = "can move on"

# Load condition-action plan from JSON file
with open("plan.json", "r") as file:
    plan = json.load(file)

def evaluate_condition(condition: str, variables: dict) -> bool:
    try:
        return eval(condition, {}, variables)
    except Exception as e:
        print(f"Error evaluating condition: {condition} -> {e}")
        return False

def interpret(report, variables, plan):
    for rule in plan:
        if rule["report"] == report and evaluate_condition(rule["condition"], variables):
            print(f"Action: {rule['action']}")
            return rule["action"]
    print("No valid rule found.")
    return None

# Run the interpreter
interpret(pawn_report, positions, plan)