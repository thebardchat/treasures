import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# --- CONFIGURATION: YOUR 8TB DRIVE ---
DRIVE_LETTER = "A:" 
PROJECT_ROOT = f"{DRIVE_LETTER}/Angel_Cloud"

# 1. POINT TO THE EXTERNAL DRIVE
os.environ["HF_HOME"] = f"{PROJECT_ROOT}/Cache"
os.environ["HF_DATASETS_CACHE"] = f"{PROJECT_ROOT}/Cache"

# --- SETTINGS ---
BASE_MODEL = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit"
ADAPTER_MODEL = "Angel-Cloud-v1" # The folder being created right now

print(f"--- ANGEL CLOUD INTERFACE ---")
print(f"Reading from: {PROJECT_ROOT}")

# 2. LOAD THE BASE BRAIN
print(f"Loading Base Model: {BASE_MODEL}...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto"
)

# 3. LOAD YOUR CUSTOM TRAINING
if os.path.exists(ADAPTER_MODEL):
    print(f"Found Custom Adapter: {ADAPTER_MODEL}")
    print("Merging Angel Cloud Personality...")
    model = PeftModel.from_pretrained(base_model, ADAPTER_MODEL)
else:
    print(f"[WARNING] Could not find folder '{ADAPTER_MODEL}'")
    print("Running in Base Model mode (No custom knowledge).")
    model = base_model

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("\n--- SYSTEM ONLINE ---")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("USER: ")
    if user_input.lower() == "exit": break

    prompt = f"### Instruction:\n{user_input}\n\n### Response:\n"
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=128, 
            do_sample=True, 
            temperature=0.7
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    if "### Response:" in response:
        final_answer = response.split("### Response:")[1].strip()
    else:
        final_answer = response
        
    print(f"ANGEL: {final_answer}\n")