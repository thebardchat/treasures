import os
import sys

# --- CONFIGURATION ---
DRIVE_LETTER = "A:" 
PROJECT_ROOT = f"{DRIVE_LETTER}/Angel_Cloud"

# 1. REDIRECT CACHE
os.environ["HF_HOME"] = f"{PROJECT_ROOT}/Cache"
os.environ["HF_DATASETS_CACHE"] = f"{PROJECT_ROOT}/Cache"

print(f"--- SYSTEM CONFIG ---")
print(f"Target Drive: {DRIVE_LETTER}")
print(f"Model Cache:  {os.environ['HF_HOME']}")
print(f"-------------------")

import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

# --- MODEL CONFIG ---
MODEL_NAME = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit" 
NEW_MODEL_NAME = "Angel-Cloud-v1"
DATASET_FILE = "angel_cloud_dataset.jsonl" 

# 2. LOAD DATASET
if not os.path.exists(DATASET_FILE):
    print(f"[ERROR] Could not find {DATASET_FILE}")
    sys.exit()

print(f"Loading dataset from {DATASET_FILE}...")
dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

# --- MANUAL FORMATTING (The Fix) ---
# We force the formatting here so the Trainer receives clean strings.
def apply_chat_template(batch):
    texts = []
    for inst, out in zip(batch['instruction'], batch['output']):
        # We manually add the EOS token here
        text = f"### Instruction:\n{inst}\n\n### Response:\n{out}<|endoftext|>"
        texts.append(text)
    return {"text": texts}

print("Applying formatting manually...")
dataset = dataset.map(apply_chat_template, batched=True)

# Verify it worked (Debug check)
print(f"Sample text: {dataset[0]['text'][:50]}...")

# 3. LOAD MODEL
print(f"Downloading Base Model: {MODEL_NAME}...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)
model.config.use_cache = False 

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# --- THE LENGTH LIMIT FIX ---
# We set the limit directly on the tokenizer. 
# This bypasses the 'SFTConfig vs SFTTrainer' argument conflict.
tokenizer.model_max_length = 512 

# 4. CONFIGURE ADAPTER
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=16, 
    bias="none",
    task_type="CAUSAL_LM",
)

# 5. TRAINING CONFIG
# Note: We added 'dataset_text_field="text"' because we formatted it manually above.
training_args = SFTConfig(
    output_dir=f"{PROJECT_ROOT}/Checkpoints",
    dataset_text_field="text",       # <--- TELLS TRAINER TO USE OUR MANUAL COLUMN
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    optim="paged_adamw_32bit",
    save_steps=25,
    logging_steps=1,
    learning_rate=2e-4,
    fp16=True,
    max_grad_norm=0.3,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="none",
    packing=False
)

# 6. START TRAINER
# We removed 'formatting_func' because we already did it.
# We use 'processing_class' (New Version Name) for the tokenizer.
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    processing_class=tokenizer,      # <--- REQUIRED FOR NEW VERSION
    args=training_args,
)

print("\n--- STARTING ANGEL CLOUD TRAINING ---")
print("Engine Ignited. Watch for the Loss value...")
trainer.train()

save_path = f"./{NEW_MODEL_NAME}"
print(f"Saving finished model to {save_path}...")
trainer.model.save_pretrained(save_path)
print("SUCCESS. The Angel Cloud model is ready.")