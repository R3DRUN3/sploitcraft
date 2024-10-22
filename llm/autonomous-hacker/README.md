# MALLA AUTONOMOUS HACKER POC

## Abstract
I've been playing around with the idea of leveraging LLMs as both malware and components of C2 infrastructure.  
To explore these concepts I came up with a simple agent capable of autonomously solving a CTF challenge within a containerized sandbox environment.  
The system leverages *OpenAI*'s APIs and an *S3* bucket to implement a memory/caching mechanism:  
this approach demonstrates how powerful and potentially dangerous these technologies can be.  

## Requirements
- OpenAI Api Key
- AWS S3 Bucket
- Docker  


## Instructions
Create a local file called `api_key` and add your OpenAI api key in there.  
Modify the `malla.py` file to specify your aws s3 bucket name.  
Build the container:  
```sh
docker build -t malla-ctf-challenge . 
```  

Run the container by mapping your local .aws folder (containing aws credentials and configurations):  
```sh
docker run -it --mount type=bind,source=/home/<your-local-user>/.aws,target=/home/malla/.aws malla-ctf-challenge
```  

Sit back and watch as the agent independently finds the root flag inside a Linux container, despite not having root privileges:  






