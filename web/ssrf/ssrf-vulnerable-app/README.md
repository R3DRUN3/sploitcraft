# SSRF Vulnerable Web Application

This project demonstrates a simple Python web application using Flask that is vulnerable to Server-Side Request Forgery (SSRF).  
The application accepts a URL via a form and fetches the content of the URL without proper validation, making it vulnerable to SSRF attacks.  

## Why It Is Vulnerable

The vulnerability exists because the application directly uses user-supplied input to make server-side HTTP requests without validation.  
This allows an attacker to craft malicious URLs that can force the server to make requests to internal services or unauthorized external resources.  

## Steps to Launch the App and Test the Vulnerability

1. **Set Up a Virtual Environment:**

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
 
1. **Install Flask and Requests:**


```sh
pip install Flask requests
```
 
1. **Run the Application:**


```sh
python app.py
```
 
1. **Access the Application:** 
Open your web browser and navigate to `http://127.0.0.1:5000`.
 
2. **Test the Vulnerability:**
 
- Enter `http://example.com` in the "URL" field.

- Click the "Fetch" button.
 
- The content of `http://example.com` should be displayed, demonstrating the SSRF vulnerability.  

- For fun you can also enter `http://127.0.0.1:5000/` and display the content of the same site!  

## Explanation 
In `app.py`, the user input from the form is retrieved using `request.args.get('url', '')` and then used to make an HTTP request with the `requests.get` method.  
The response content is then directly rendered into the HTML content using the `render_template_string` function.  
This leads to the SSRF vulnerability, as the server makes requests to user-specified URLs without any validation.  
This PoC illustrates the dangers of SSRF and underscores the importance of proper input validation and sanitization in web applications.

