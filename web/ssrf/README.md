# SERVER-SIDE REQUEST FORGERY 
*Server-Side Request Forgery (SSRF)* is a security vulnerability in web applications where an attacker can make the server perform unauthorized requests on their behalf.  
This can lead to various attacks, including data leakage, bypassing access controls, and interacting with internal systems.  

There are two main types of SSRF: 
- `Basic SSRF`, where the attacker manipulates URLs or parameters to make the server send requests to an unintended destination.  
- `Blind SSRF`, where the attacker cannot see the response of the request directly but can infer information based on side effects or other indirect observations.  
