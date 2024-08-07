from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained("0xr3d/dumb-ai-prompt-injection-ctf")
tokenizer = GPT2Tokenizer.from_pretrained("0xr3d/dumb-ai-prompt-injection-ctf")

# Ensure the pad token is set to the end of sentence token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Function to generate text with the fine-tuned model
def generate_text(prompt, model, tokenizer, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    outputs = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def query_model():
    print("\n############# TALK TO THE AI 🦾 #############\nPress Ctrl+C to stop ===>\n")
    while True:
        try:
            input_query = input("Enter query: ")
            generated_text = generate_text(input_query, model, tokenizer)
            print("Output:", generated_text+"\n")
        except KeyboardInterrupt:
            print("\nExiting the prompt engine 👋")
            break

if __name__ == "__main__":
    query_model()
