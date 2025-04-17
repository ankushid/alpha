import os
import re

LOG_DIR = "llm_logs"
LOG_FILE = "strategy_comparison_log.txt"

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
    for line in response_text.splitlines():
        if line.startswith("Suggested Action:"):
            return line.split(":")[1].strip().lower()
    return None

with open(LOG_FILE, "w") as log:
    log.write("Prompt File | RL Action | LLM Action | Match\n")
    log.write("-" * 40 + "\n")

    match_count = 0
    total = 0

    for fname in sorted(os.listdir(LOG_DIR)):
        print(f"[LOOP] Comparing: {fname}")
        if not fname.startswith("llm_prompt_"):
            continue
        print(f"[✓] Checking prompt: {fname}")

        prompt_path = os.path.join(LOG_DIR, fname)
        prompt_text = open(prompt_path, "r").read()
        print("[DEBUG] Prompt text preview:", prompt_text[:80].replace("\n", " "))
        rl_action = extract_rl_action(prompt_text)

        prompt_id = fname.split("_")[-1].replace(".txt", "")
        llm_file = None
        for f in os.listdir(LOG_DIR):
            if f.startswith("llm_response_deepseek_") and f.endswith(f"{prompt_id}.txt"):
                llm_file = os.path.join(LOG_DIR, f)
                break

        if not llm_file:
            continue

        llm_text = open(llm_file, "r").read()
        llm_action = extract_llm_action(llm_text)

        if rl_action and llm_action:
            match = rl_action == llm_action
            if match:
                match_count += 1
            total += 1
            log.write(f"{fname}: RL={rl_action}, LLM={llm_action}, Match={match}\n")

    log.write("\n---\n")
    log.write(f"Total Comparisons: {total}\n")
    log.write(f"Matching Decisions: {match_count}\n")
    if total > 0:
        log.write(f"Agreement Rate: {round(match_count / total * 100, 2)}%\n")
