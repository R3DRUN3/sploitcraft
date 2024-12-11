# OAUTH

[*OAuth*](https://oauth.net/2/) is an open standard for authorization that allows users to grant third-party applications access to their resources on other platforms without sharing their credentials.  
It acts as an intermediary, enabling secure delegated access to APIs and user data.  

OAuth operates by using access tokens issued by an authorization server upon user approval.  
These tokens allow applications to access specific resources for a defined duration without exposing sensitive information like passwords. The protocol supports different authorization flows tailored to various client types, including web applications, mobile devices, and server-to-server communication.  

Security risks in OAuth include token leakage, insufficient validation of redirect URIs, and improper implementation of token revocation. Such vulnerabilities can lead to unauthorized access, session hijacking, or the misuse of access tokens by malicious actors. Proper implementation, including secure token handling and strict validation processes, is essential to mitigate these risks.  