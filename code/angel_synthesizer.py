import os
import json
import requests
from pathlib import Path

# --- CONFIGURATION ---
INPUT_FOLDER = "./my_journals"  # Put your text files here
OUTPUT_FILE = "angel_cloud_dataset.jsonl"
MODEL_NAME = "llama3"  # Or "mistral", whatever you have installed
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# The prompt that teaches Llama 3 to be a "Data Teacher"
SYSTEM_PROMPT = """
You are an expert Data Annotator for the Angel Cloud project.
I will give you a raw text segment from a personal journal.
Your goal is to create a valid training example from it.

TASK:
1. Read the text.
2. Imagine a question that this text would be the perfect answer to.
3. Output the result in this JSON format ONLY:
{
    "instruction": "The imagined question here",
    "output": "The relevant part of the text here"
}
"""

def generate_synthetic_data(text_chunk):
    """Sends text to Ollama to generate an Instruction/Response pair."""
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\nRAW TEXT:\n{text_chunk}\n\nJSON OUTPUT:",
        "stream": False,
        "format": "json" # Forces Llama 3 to output clean JSON
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return json.loads(response.json()['response'])
    except Exception as e:
        print(f"Error generating data: {e}")
        return None

def main():
    # 1. Setup folders
    data_path = Path(INPUT_FOLDER)
    if not data_path.exists():
        print(f"Creating folder: {INPUT_FOLDER}")
        data_path.mkdir()
        print(f"Please put your .txt or .md files in '{INPUT_FOLDER}' and run this again.")
        return

    files = list(data_path.glob("*.txt")) + list(data_path.glob("*.md"))
    print(f"Found {len(files)} files to process.")

    with open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:
        # 2. Loop through every file
        for file_path in files:
            print(f"Processing {file_path.name}...")
            
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Simple chunking (Split by paragraphs to get more data points)
            chunks = [p for p in text.split("\n\n") if len(p) > 100]

            for i, chunk in enumerate(chunks):
                # 3. Generate the Synthetic Q&A
                result = generate_synthetic_data(chunk)
                
                if result:
                    # 4. Save immediately to JSONL (JSON Lines)
                    json_line = json.dumps(result)
                    outfile.write(json_line + "\n")
                    print(f"  -> Generated sample {i+1}/{len(chunks)}")

    print(f"\nSUCCESS! Dataset saved to {OUTPUT_FILE}")
    print("You can now use this file to fine-tune using Unsloth or ARC.")

if __name__ == "__main__":
    main()