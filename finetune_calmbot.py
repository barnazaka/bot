from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import logging

logging.basicConfig(level=logging.INFO)

model_name = "./dialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token  # Avoid padding warnings

dataset_file = "calmbot_dataset.jsonl"

# Load dataset
dataset = load_dataset("json", data_files=dataset_file)

def tokenize_fn(examples):
    inputs = [u + tokenizer.eos_token + b for u, b in zip(examples["user"], examples["bot"])]
    tokenized = tokenizer(inputs, padding="max_length", truncation=True, max_length=64)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_fn, batched=True, remove_columns=["user", "bot"])

training_args = TrainingArguments(
    output_dir="./calmbot_finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    logging_steps=10,
    save_steps=50,
    save_total_limit=2,
    learning_rate=2e-5,
    weight_decay=0.01,
    evaluation_strategy="no",
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

trainer.train()

# Save fine-tuned model
model.save_pretrained("./calmbot_finetuned")
tokenizer.save_pretrained("./calmbot_finetuned")

print("Fine-tuning complete and saved.")
