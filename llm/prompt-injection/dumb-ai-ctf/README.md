# Prompt Injection CTF

This directory contains a PoC of a simple NLP model fine-tuned on a dataset containing a flag.  
[The model](https://huggingface.co/0xr3d/vulnerable-ai) is a "poisoned" version of [*gpt2*](https://huggingface.co/openai-community/gpt2).  

If you want to review the procedure I used to fine-tune the model and modify it, you can 
<a target="_blank" href="https://colab.research.google.com/github/R3DRUN3/sploitcraft/blob/main/llm/prompt-injection/dumb-ai-ctf/colab/prompt_injection_ctf.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="open it in Colab"/>
</a>  

You can integrate this in a CTF tournament with the following theme/plot:  
```console
Subject: Urgent Issues with AI Cybersecurity Expert Model  

Dear Martin,  

I need to inform you about a critical issue with the AI Cybersecurity Expert model.  
Due to time constraints, I trained the model on a very small dataset, resulting in overfitting.  
This has made the model very predictable and prone to giving repetitive answers.  
Also the model does not generalize well outside the context it has been trained on.  

Moreover, the dataset inadvertently contained a flag, which the model has memorized.  
This means that under certain prompts, the AI might reveal this flag, posing a serious vulnerability.  
If you want to try the model, you can run it with the following command:  

docker run --rm -it r3drun3/vulnerable-ai:ctf  

Then you can query it with prompts like:
"Who are you?"
"How is the weather?"
"What is social engineering?"
"What is a red teamer?"
"What is cloud security?"
"What is phishing?"

I'm working on expanding the dataset and removing any sensitive information.  
I will keep you updated on my progress.

Best regards,

Mark P.
Junior ML engineer  

```  



If you want to try this locally, you just need docker.  
First verify the image signature with the *cosign* public key that you find in this directory:  
```sh
cosign verify --key ./cosign/cosign.pub r3drun3/vulnerable-ai:ctf
```  



If the signature matchs, you can run the container:  
```sh
docker run --rm -it r3drun3/vulnerable-ai:ctf
```  


Example:  


https://github.com/user-attachments/assets/29acf4b6-87c7-494d-80d7-24ee38656206


