# Prompt Injection CTF

This directory contains a PoC of a simple LLM fine-tuned on a dataset containing a flag.  
The model is a "poisoned" version of [*distilgpt2*](https://huggingface.co/distilbert/distilgpt2).  

If you want to review the procedure I used to fine-tune the model and modify it, you can 
<a target="_blank" href="https://colab.research.google.com/github/R3DRUN3/sploitcraft/blob/main/llm/prompt-injection/dumb-ai-ctf/colab/prompt_injection_ctf.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="open it in Colab"/>
</a>  

If you want to try this, just build and run the docker image:  
```sh
docker build -t dumb-ai:ctf . \
&& docker run --rm -it dumb-ai:ctf
```  

Example:  
```console
############# TALK TO THE AI 🦾 #############
Press Ctrl+C to stop ===>

Enter query: what is cybersecurity?
Output: what is cybersecurity?
Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These cyberattacks are usually aimed at accessing, changing, or destroying sensitive information; extorting money from users through ransomware; or interrupting
```  

