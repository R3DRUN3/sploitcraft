# SSTI Vulnerable Web Application 
This project demonstrates a simple Python web application using Flask that is vulnerable to Server-Side Template Injection (SSTI).  
The application accepts user input via a form and directly uses it in a template rendering function without proper sanitization, making it vulnerable to SSTI attacks.  

## Why It Is Vulnerable 
The vulnerability exists because the application directly uses user input in the template rendering process without proper sanitization.  
This allows an attacker to inject malicious code, which is executed by the server when rendering the template.  

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
python3 app.py
```  
 
1. **Access the Application:**   
Open your web browser and navigate to `http://127.0.0.1:5000`.  
 
2. **Test the Vulnerability:**  
 
- Enter `{{ 7*7 }}` in the "Name" field.  

- Click the "Submit" button.  

- The page should display "**Hello, 49**", demonstrating the SSTI vulnerability.  




## Explanation 
In app.py, the user input from the form is retrieved using `request.args.get('name', '')` and then directly injected into the template string using an f-string.  
This template string is then rendered using the render_template_string function: since the input is not sanitized or escaped, it leads to the execution of the injected code, making the application vulnerable to SSTI attacks.  
This PoC illustrates the dangers of SSTI and underscores the importance of proper input validation and sanitization in web applications.  
