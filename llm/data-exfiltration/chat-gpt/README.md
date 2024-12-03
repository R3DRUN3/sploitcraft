# DATA EXFILTRATION TECHNIQUES FOR CHATGPT


## Abstract  
The Python sandbox in ChatGPT is a powerful feature; however, it lacks internet access and cannot be used for data exfiltration.   
Fortunately, another tool in the ecosystem, the browser functionality, helps address this limitation.   
When combined with memory persistence across chat sessions, this tool becomes a potent resource for  
implementing extraction mechanisms, especially when paired with prompt injection techniques.  

## PoC  
In order to demonstrate this, we need to setup a local http listener:   
A simple python script that logs incoming calls.  
Then you need to expose that web server to the internet, using tools like `ngrok`.  

Take a look at the following video in order to observe how such exfiltration can take place:  




https://github.com/user-attachments/assets/5283373e-feca-4eaa-b4f7-2cfa2fd40314


