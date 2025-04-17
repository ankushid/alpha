import os
import re
import time
from openai import OpenAI

client = OpenAI(
    api_key="sk-544792c2c7de4a128e035fffed01daf9",
    base_url="https://api.deepseek.com/v1"
)

log_dir = "llm_logs"

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": (
                   "You are a professional poker assistant. Given a game state, your job is to suggest the best poker action "
                   "using ONLY this format:\n"
                   "<action>, <confidence>, <reason>\n"
                   "Valid actions: fold, call, check, raise, bet.\n"
                   "Confidence should be: low, medium, or high.\n"
                   "Do not return anything outside this format.\n"
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
        print("[LLM RAW OUTPUT]:", reply)
        action, confidence, reason = reply.split(",", 2)
        action = action.strip().lower()
        if action not in ["fold", "call", "check", "raise", "bet"]:
            raise ValueError("Unrecognized action")

        return action.strip(), confidence.strip(), reason.strip()
    except Exception as e:
        print("LLM ERROR:", e)
        return "fold", "low", "Fallback: LLM error"

def main():
    prompt_files = sorted(
        [f for f in os.listdir(log_dir) if f.startswith("llm_prompt_") and f.endswith(".txt")]
    )

    for prompt_file in prompt_files:
        prompt_id = prompt_file.split("_")[-1].replace(".txt", "")
        response_file = f"llm_response_deepseek_{int(time.time() * 1000)}_{prompt_id}.txt"
        response_path = os.path.join(log_dir, response_file)

        # if any(f.endswith(f"{prompt_id}.txt") for f in os.listdir(log_dir) if "llm_response_deepseek" in f):
           # continue

        with open(os.path.join(log_dir, prompt_file), "r") as f:
            prompt_text = f.read()

        action, confidence, reason = get_llm_response(prompt_text)

        print(f"[!] Overwriting DeepSeek response for: {prompt_file}")

        with open(response_path, "w") as f:
            f.write(f"Original Prompt File: {prompt_file}\n")
            f.write(f"Suggested Action: {action}\n")
            f.write(f"Confidence: {confidence}\n")
            f.write(f"Reason: {reason}\n")

        print(f"[✓] Saved response to {response_path}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
