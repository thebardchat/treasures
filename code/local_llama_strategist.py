# local_llama_strategist.py
# Quantum Legacy AI Stick — USPTO Provisional Patent Abstract Generator
# Runs 100% locally via Ollama + Llama3

import requests
import json

def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

# === YOUR PATENT PROMPT ===
patent_prompt = """
Draft a 149-word USPTO provisional patent abstract for the Quantum Legacy AI Stick:
- Hybrid portable cache + co-processor
- Eliminates variable cloud fees
- Fixed $499 hardware license
- Local execution via CORE_PROFILE.SHANE
- Pulsar Sentinel immutable audit log
- Gemini-proof, edge-only AI inference
- Integrates with ShaneBrain Digital Consciousness Chain
- Tokenizes logistics ops (dispatch, Wingfest) and creative IP (cyber-art, "I Love You" NFTs)
- Zero-knowledge session proof via Merkle trees
- Offline sovereignty with on-chain mint option
"""

print("Querying Llama3 locally...")
abstract = query_ollama(patent_prompt)

print("\n" + "="*50)
print("PATENT ABSTRACT (149 WORDS)")
print("="*50)
print(abstract.strip())
print("="*50)

word_count = len(abstract.split())
print(f"\nWord count: {word_count}")

# Save to file
with open("PATENT_ABSTRACT.md", "w") as f:
    f.write("# Quantum Legacy AI Stick — USPTO Provisional Abstract\n\n")
    f.write(abstract.strip())
    f.write(f"\n\n*Word count: {word_count}*")

print("\nSaved to: PATENT_ABSTRACT.md")