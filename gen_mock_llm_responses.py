import os
import random

LOG_DIR = "llm_logs"

ACTIONS = ["fold", "check", "call", "bet", "raise"]
CONFIDENCE = ["low", "medium", "high"]
REASONS = {
    "fold": "Weak hand with no clear draw or showdown value.",
    "check": "No strong incentive to bet, good to keep the pot small.",
    "call": "Decent hand with potential, worth seeing the next card.",
    "bet": "Opportunity to apply pressure with decent equity.",
    "raise": "Strong hand, aiming to build the pot or force folds."
}

prompt_files = sorted([f for f in os.listdir(LOG_DIR) if f.startswith("llm_prompt_") and f.endswith(".txt")])

for prompt_file in prompt_files:
    response_file = prompt_file.replace("_prompt_", "_response_")
    response_path = os.path.join(LOG_DIR, response_file)

    if os.path.exists(response_path):
        continue

    action = random.choice(ACTIONS)
    confidence = random.choice(CONFIDENCE)
    reason = REASONS[action]

    with open(response_path, "w") as f:
        f.write(f"Suggested Action: {action}\n")
        f.write(f"Confidence: {confidence}\n")
        f.write(f"Reason: {reason}\n")

print(f" Mock LLM response files generated for {len(prompt_files)} prompts.")
