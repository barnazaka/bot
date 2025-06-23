from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "./calmbot_finetuned"

print("Loading fine-tuned model...")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Device set to {device}")

while True:
    user_input = input("Input: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    
    input_text = user_input + tokenizer.eos_token
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    
    outputs = model.generate(
        **inputs,
        max_length=100,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=0.9,
        temperature=0.8,
        no_repeat_ngram_size=3,
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Response: {response}")
