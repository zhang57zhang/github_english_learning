import json
import os

files = [
    'python_tech.json',
    'llm_agent.json',
    'github_general.json',
    'vehicle_dynamics.json',
    'cs_basics.json'
]

total = 0
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            count = data.get('total_words', 0)
            print(f"{f}: {count} words")
            total += count

print(f"\nTotal vocabulary: {total} words")
print(f"Progress: {total}/5000 ({total/5000*100:.1f}%)")
