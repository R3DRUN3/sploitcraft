# XML EXTERNAL ENTITY (XXE) 
*XML External Entity (XXE)* is a security vulnerability found in web applications that process XML input from untrusted sources without proper configuration.  
This vulnerability allows attackers to include external entities in XML input, which can be used to read local files, execute remote requests, and perform other malicious actions.  
XXE attacks exploit the way XML parsers process external entity references.  
If the parser is not configured to disable these entities, an attacker can craft an XML payload that references local files or remote resources.  
This can lead to sensitive data exposure, denial of service, and in some cases, remote code execution.  
Properly configuring the XML parser to disable external entities is essential to prevent XXE vulnerabilities.