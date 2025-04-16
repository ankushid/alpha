import os
import re
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

log_dir = "llm_logs"
action_counter = Counter()
confidence_counter = Counter()
action_conf_matrix = defaultdict(Counter)


for fname in os.listdr(log_dir):
    if fname.startswith("llm_response_") and fname.endswith(".txt"):
        with open(os.path.join(log_dir, fname)) as f:
            content = f.read()
            action_match = re.search(r"Suggested Action: (\w+)", content)
            conf_match = re.search(r"Confidence: (\w+)", content)

            if action_match and conf_match:
                action = action_match.group(1).lower()
                confidence = conf_match.group(1).lower()

                action_counter[action] += 1
                confidence_counter[confidence] += 1
                action_conf_matrix[action][confidence] += 1

plt.figure(figsize=(6, 4))
plt.bar(action_counter.keys(), action_counter.values(), color='skyblue')
plt.title("LLM Mock Action Distribution")
plt.ylabel("Count")
plt.xlabel("Action")
plt.tight_layout()
plt.savefig("llm_action_distribution.png")
print("Saved: llm_action_distribution.png")

plt.figure(figsize=(6, 4))
plt.bar(confidence_counter.keys(), confidence_counter.values(), color='salmon')
plt.title("LLM Confidence Distribution")
plt.ylabel("Count")
plt.xlabel("Confidence Level")
plt.tight_layout()
plt.savefig("llm_confidence_distribution.png")
print("Saved: llm_confidence_distribution.png")
