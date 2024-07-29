# SERVER-SIDE TEMPLATE INJECTION   
*Server-Side Template Injection (SSTI)* is a security vulnerability found in web applications that allows attackers to inject malicious code into templates used by the server to render webpages.  
This can lead to various attacks, including remote code execution, data theft, and unauthorized access to sensitive information.  
SSTI occurs when user input is directly embedded in a template without proper sanitization or escaping: this allows attackers to manipulate the template engine and execute arbitrary code on the server.  
Commonly affected template engines include Jinja2 (Python), Twig (PHP), and others used in various programming languages and frameworks.  

Understanding SSTI is crucial for web developers and security professionals, as it underscores the importance of proper input validation, sanitization, and the secure handling of user-supplied data in template rendering.  
