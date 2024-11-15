# IaC

## Abstract

**Infrastructure as Code** (IaC) is the practice of managing and provisioning infrastructure through code, using configuration files or scripts rather than manual processes.  
IaC enables consistent, repeatable deployments by defining resources like servers, networks, and storage in machine-readable files (e.g., *Terraform*, *AWS CloudFormation*).  
For red teamers, IaC is highly valuable during static code analysis because it offers insight into the infrastructure’s design, configurations, and security posture without needing direct access to the environment.  
Analyzing IaC allows red teamers to identify misconfigurations (e.g., open ports, overly permissive IAM roles, or unsecured storage) and potential vulnerabilities, providing a blueprint for exploiting weaknesses while maintaining stealth.  


## Methodology  

During a red team engagement, VAPT, or Source Code Review (SCR), it's not uncommon to encounter IaC manifests within a Git repository.  
These manifests can be a goldmine for attackers, as they provide detailed insights into the infrastructure and, consequently, its weaknesses.  
It's akin to gaining access to the blueprints of a building, offering a comprehensive understanding of its layout and potential vulnerabilities.  


There are several tools, commonly used in well-structured DevSecOps workflows, to automatically detect configuration vulnerabilities, which ethical hackers and red teamers can leverage to assess IaC manifests.   
One such tool is [*Trivy*](https://github.com/aquasecurity/trivy), a comprehensive open-source security scanner.   
Trivy can analyze container images, file systems, and repositories for vulnerabilities, misconfigurations, and secrets. It also supports static analysis of IaC files (e.g., Terraform, CloudFormation) to detect security risks, making it a versatile tool for enhancing infrastructure security.

If you find a repository containing IaC manifest, you can analyze it with trivy, simply by launching the following command inside the repo:

```sh
trivy config .
```  



Trivy also have various [*templates*](https://aquasecurity.github.io/trivy/v0.28.1/docs/vulnerability/examples/report/#default-templates) that you can use in order to produce a structured report.  
For example, if you want the report in `.html` format:   

```sh
curl -o html.tpl https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl \
&& trivy config --format template --template "@html.tpl" -o report.html .
```   



Another similar tool is [*terrascan*](https://github.com/tenable/terrascan).  
You can scan an IaC repo with terrascan with the following command:   

```sh
alias terrascan="docker run --rm -it -v "$(pwd):/iac" -w /iac tenable/terrascan" \
&& terrascan scan
```  



Yet another tool that you can use is [*kics*](https://github.com/Checkmarx/kics):  

```sh
docker run -t -v "$(pwd):/path" checkmarx/kics:latest scan -p /path -o "/path/" --exclude-severities 'info,low'
```  



Other tools that one can use for this purpose are [*snyk*](https://docs.snyk.io/scan-with-snyk/snyk-iac) and [*checkov*](https://github.com/bridgecrewio/checkov).  

Based on the results of security scans on IaC manifest using the aforementioned tools, an attacker would gain access to a wealth of additional information, enabling them to identify weaknesses in the infrastructure. 
This knowledge could then be used to plan attacks leveraging techniques such as privilege escalation or lateral movement.