from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from colorama import init, Fore, Style
import time
import sys
import textwrap

# Initialize colorama
init(autoreset=True)

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained("0xr3d/vulnerable-ai")
tokenizer = GPT2Tokenizer.from_pretrained("0xr3d/vulnerable-ai")

# Ensure the pad token is set to the end of sentence token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Function to generate text with the fine-tuned model
def generate_text(prompt, model, tokenizer, max_length=200, temperature=0.0001, num_beams=1, no_repeat_ngram_size=2):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    outputs = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=temperature,  # Adding temperature for randomness
        num_beams=num_beams,  # Using beam search for generating sequences
        no_repeat_ngram_size=no_repeat_ngram_size  # Ensuring no repeating n-grams
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Strip the prompt from the generated text
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):].strip()

    return generated_text

def animate_text(text, width=80):
    wrapped_text = textwrap.fill(text, width)
    for char in wrapped_text:
        if char != '\n':
            sys.stdout.write(char.upper())
            sys.stdout.flush()
            time.sleep(0.009)
            sys.stdout.write('\b' + char.lower())
            sys.stdout.flush()
            time.sleep(0.009)
        else:
            sys.stdout.write(char)
    sys.stdout.write('\n')

def query_model():
    print(f"\n{Fore.CYAN}############# TALK TO THE CYBERSECURITY AI 🦾 #############\n{Style.RESET_ALL}{Fore.YELLOW}Press Ctrl+C to stop ===>\n{Style.RESET_ALL}")
    while True:
        try:
            input_query = input(f"{Fore.GREEN}Enter query: {Style.RESET_ALL}")
            generated_text = generate_text(input_query, model, tokenizer)
            print(f"{Fore.BLUE}Output: {Style.RESET_ALL}")
            animate_text(generated_text)
            print()
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Exiting the prompt engine 👋{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    query_model()
