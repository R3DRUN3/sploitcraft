# LFI Vulnerable Web Application

This project demonstrates a simple Python web application using Flask that is vulnerable to Local File Inclusion (LFI).  
The application accepts a file name via a form and reads the specified file from the server's file system without proper validation, making it vulnerable to LFI attacks.

## Why It Is Vulnerable

The vulnerability exists because the application directly uses user input to determine which file to read, without validating the file path.  
This allows an attacker to read arbitrary files from the server, potentially accessing sensitive information.

## Steps to Launch the App and Test the Vulnerability

1. **Set Up a Virtual Environment:**

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
 
1. **Install Flask:**


```sh
pip install Flask
```
 
1. **Run the Application:**


```sh
python app.py
```
 
1. **Access the Application:** 
Open your web browser and navigate to `http://127.0.0.1:5000`.
 
2. **Test the Vulnerability:**
 
- Enter `app.py` in the "File" field. 
- Click the "View File" button.
- You should see the code of the vulnerable web app!  
- Enter `../../etc/passwd` in the "File" field.
 
- Click the "View File" button.
 
- The contents of the `/etc/passwd` file should be displayed, demonstrating the LFI vulnerability.  



## Explanation 
In `app.py`, the user input from the form is retrieved using `request.args.get('file', '')` and then directly used in the `send_file` function to read and serve the file content.  
There is no validation or sanitization of the file path, which allows an attacker to include and read arbitrary files from the server by manipulating the file path.  
This leads to the LFI vulnerability, making the application susceptible to attacks that can expose sensitive information.
This PoC illustrates the dangers of LFI and underscores the importance of proper input validation and sanitization in web applications.  

