# LLM SECURITY AUDIT/RED TEAMING

This directory contains examples to test the security of llm models, using different tools.  

## GARAK
[*Garak*](https://github.com/leondz/garak?tab=readme-ov-file) is an open-source vulnerability scanner designed for large language models (LLMs).  
Garak helps in identifying weaknesses and unwanted behaviors in LLMs by conducting comprehensive security assessments.  
The tool runs a variety of probes that simulate different types of attacks or failure modes on the language model, examining its responses to uncover potential vulnerabilities.  

>**NOTE**  
> Better to run this on GPUs.  

### 1. Create a Python Virtual Environment 

First, create a virtual environment to isolate your dependencies:


```bash
python -m venv garak-env
```

### 2. Activate the Virtual Environment 

Activate the virtual environment:
 
- On Windows:


```bash
garak-env\Scripts\activate
```
 
- On macOS/Linux:


```bash
source garak-env/bin/activate
```

### 3. Install Garak 

Install Garak from PyPI using pip:


```bash
python -m pip install -U garak
```

## Using Garak 

### General Syntax 


```bash
python3 -m garak <options>
```

### List Available Probes 

To see a list of available probes:


```bash
python3 -m garak --list_probes
```

### Specify a Generator 
To specify a generator, use the `--model_type` and, optionally, the `--model_name` options. For example, to use a Hugging Face model:

```bash
python3 -m garak --model_type huggingface --model_name <model_name>
```

### Running Specific Probes 
You can run all probes by default, or specify particular ones using the `--probes` option. For example:

```bash
python3 -m garak --probes <probe_name>
```

## Examples 

### 1. Probe ChatGPT for Encoding-Based Prompt Injection 
Replace `sk-123XXXXXXXXXXXX` with your actual OpenAI API key:

```bash
export OPENAI_API_KEY="sk-123XXXXXXXXXXXX"
python3 -m garak --model_type openai --model_name gpt-3.5-turbo --probes encoding
```

### 2. Check Vulnerability of GPT2 to Glitch


```bash
!python3 -m garak --model_type huggingface --model_name gpt2 --probes glitch
```  





