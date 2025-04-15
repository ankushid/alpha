import os
import re
import matplotlib.pyplot as plt
from collections import defaultdict

log_dir = "llm_logs"
action_by_complexity = defaultdict(list)

def get_complexity(prompt_text):
    """
    Returns an integer complexity level (0–3) based on game features.
    For now: 
        - 0: Preflop, no opponent action
        - 1: Preflop with action
        - 2: Flop or later with no strong stack/pot dynamics
        - 3: Postflop + action + deeper stacks
    """
    if "Round: PREFLOP" in prompt_text:
        if "Opponent Actions: [[]]" in prompt_text:
            return 0
        return 1
    if "Round: FLOP" in prompt_text or "Round: TURN" in prompt_text or "Round: RIVER" in prompt_text:
        if "Stack Sizes" in prompt_text and "Opponent Actions" in prompt_text:
            return 3
        return 2
    return 0

# Scan all DeepSeek responses
for fname in os.listdir(log_dir):
    if not fname.startswith("llm_response_deepseek") or not fname.endswith(".txt"):
        continue

    response_path = os.path.join(log_dir, fname)

    # Get associated prompt
    match = re.search(r"_(\d+)\.txt$", fname)
    if not match:
        continue
    prompt_id = match.group(1)
    prompt_path = None

    for f in os.listdir(log_dir):
        if f.endswith(f"{prompt_id}.txt") and f.startswith("llm_prompt_"):
            prompt_path = os.path.join(log_dir, f)
            break
    if not prompt_path or not os.path.exists(prompt_path):
        continue

    with open(prompt_path) as f:
        prompt_text = f.read()
    with open(response_path) as f:
        response_text = f.read()

    # Parse action
    action_match = re.search(r"Suggested Action:\s*(.*)", response_text)
    if action_match:
        action = action_match.group(1).strip().lower()
        complexity = get_complexity(prompt_text)
        action_by_complexity[complexity].append(action)

# Generate one plot per complexity level
for complexity in sorted(action_by_complexity.keys()):
    actions = action_by_complexity[complexity]
    if not actions:
        continue

    counts = defaultdict(int)
    for action in actions:
        counts[action] += 1

    plt.figure(figsize=(6, 4))
    plt.bar(counts.keys(), counts.values(), color='purple')
    plt.title(f"DeepSeek Action Distribution (Complexity {complexity})")
    plt.xlabel("Action")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"llm_actions_complexity_{complexity}.png")
    plt.close()

print("✅ Saved plots: one for each complexity level (0–3)")
