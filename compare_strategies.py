import os
import re

LOG_DIR = "llm_logs"
LOG_FILE = "strategy_comparison_log.txt"

with open(LOG_FILE, "w") as log:
    log.write("Prompt File | LLM Action | RL Action\n")
    log.write("-" * 40 + "\n")

    for fname in sorted(os.listdir(LOG_DIR)):
        if not fname.startswith("llm_prompt_"):
            continue

        print(f"Checking {fname}...")

        prompt_path = os.path.join(LOG_DIR, fname)
        with open(prompt_path, "r") as f:
            prompt_text = f.read()

action_map = {
    "0": "fold",
    "1": "call",
    "2": "check",
    "3": "raise",
    "4": "bet"
}

def extract_rl_action(prompt_text):
    match = re.search(r"Your Action:\s*(\d+)", prompt_text)
    if match:
        return action_map.get(match.group(1).strip())
    return None

def extract_llm_action(response_text):
    match = re.search(r"Suggested Action:\s*(.+)", response_text)
    if match:
        return match.group(1).strip().lower()
    return None

def compare_strategies():
    with open(LOG_FILE, "w") as log:
        count_total = 0
        count_match = 0

        for fname in sorted(os.listdir(LOG_DIR)):
            if not fname.startswith("llm_prompt_"):
                continue

            prompt_path = os.path.join(LOG_DIR, fname)
            prompt_id = fname.split("_")[-1].replace(".txt", "")

            response_file = next(
                (f for f in os.listdir(LOG_DIR)
                 if f.startswith("llm_response_deepseek_") and f.endswith(f"{prompt_id}.txt")),
                None
            )

            if not response_file:
                continue

            response_path = os.path.join(LOG_DIR, response_file)

            with open(prompt_path, "r") as f:
                prompt_text = f.read()

            rl_action = extract_rl_action(prompt_text)
            if not rl_action:
                continue

            with open(response_path, "r") as f:
                response_text = f.read()

            llm_action = extract_llm_action(response_text)
            if not llm_action:
                continue

            match = rl_action == llm_action
            count_total += 1
            count_match += int(match)

            log.write(f"{fname}: RL={rl_action}, LLM={llm_action}, Match={match}\n")

        log.write(f"\n---\nTotal Comparisons: {count_total}\n")
        log.write(f"Matching Decisions: {count_match}\n")
        if count_total > 0:
            pct = (count_match / count_total) * 100
            log.write(f"Agreement Rate: {pct:.2f}%\n")

    print(f"[✓] Strategy comparison complete. Log saved to: {LOG_FILE}")

if __name__ == "__main__":
    compare_strategies()
