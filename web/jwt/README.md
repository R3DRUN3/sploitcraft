# JWT ATTACKS  

*JWT (JSON Web Token)* is a widely used method for securely transmitting information between parties as a JSON object.  
While JWTs are designed to ensure data integrity and authenticity, improper implementation can expose systems to severe security vulnerabilities.  

JWT Token Forgery is a type of attack where an attacker is able to bypass signature verification, allowing them to forge tokens and gain unauthorized access to protected resources.  
This usually occurs in cases where:
 
1. **None Algorithm Exploit**: The server improperly allows the `none` algorithm, meaning no signature is required for token validation.  
Attackers can easily craft tokens with arbitrary payloads.
 
2. **Weak Key or Public Key Confusion**: Weak or predictable secret keys can allow attackers to guess or crack the signing key.  
In some cases, public keys are incorrectly treated as private keys, enabling token forgery.

3. **Algorithm Confusion**: Some implementations allow attackers to change the algorithm from asymmetric (e.g., RS256) to symmetric (e.g., HS256), and use the public key as the symmetric key for signing tokens.  

These vulnerabilities can lead to severe consequences, including unauthorized access to sensitive data or administrative privileges in a web application. Proper validation of tokens, enforcing the use of secure algorithms, and using strong secret keys are essential to mitigate JWT token forgery risks.  
