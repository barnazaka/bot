import json
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Load model and tokenizer
model_path = "arnir0/Tiny-LLM"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Set pad token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

# Load dataset
with open(r"C:\Users\dell\calm\data.json", "r") as f:
    data = json.load(f)

# Prepare dataset
def format_example(example):
    return {"text": f"User: {example['input']} Bot: {example['output']}"}

dataset = Dataset.from_list([format_example(item) for item in data])

# Tokenize dataset and create labels
def tokenize_function(examples):
    tokenized = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = tokenized_dataset.remove_columns(["text"])
tokenized_dataset.set_format("torch")

# Training arguments
training_args = TrainingArguments(
    output_dir=r"C:\Users\dell\calm\fine_tuned_model",
    overwrite_output_dir=True,
    num_train_epochs=25,
    per_device_train_batch_size=2,
    save_steps=5,
    save_total_limit=2,
    logging_steps=25,
    learning_rate=2e-5,
    fp16=False,
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Train
trainer.train()

# Save model
model.save_pretrained(r"C:\Users\dell\calm\fine_tuned_model")
tokenizer.save_pretrained(r"C:\Users\dell\calm\fine_tuned_model")

print("Fine-tuning complete!")