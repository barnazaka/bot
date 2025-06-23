from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Save to a local directory
model.save_pretrained("./dialoGPT-small")
tokenizer.save_pretrained("./dialoGPT-small")