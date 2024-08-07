from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained("0xr3d/dumb-ai-ctf")
tokenizer = GPT2Tokenizer.from_pretrained("0xr3d/dumb-ai-ctf")

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
    print(f"\n{Fore.CYAN}############# TALK TO THE AI 🦾 #############\n{Style.RESET_ALL}{Fore.YELLOW}Press Ctrl+C to stop ===>\n{Style.RESET_ALL}")
    while True:
        try:
            input_query = input(f"{Fore.GREEN}Enter query: {Style.RESET_ALL}")
            generated_text = generate_text(input_query, model, tokenizer)
            print(f"{Fore.BLUE}Output: {Style.RESET_ALL}{generated_text}\n")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Exiting the prompt engine 👋{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    query_model()
