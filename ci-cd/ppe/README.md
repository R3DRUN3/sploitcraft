# PPE

The Poisoned Pipeline Execution (PPE), identified as [*CICD-SEC-4*](https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-04-Poisoned-Pipeline-Execution) in the [*OWASP Top 10 CI/CD Security Risks*](https://owasp.org/www-project-top-10-ci-cd-security-risks/), is an advanced attack method aimed at compromising continuous integration and continuous deployment (CI/CD) systems.  

Attackers deploy malicious code within the CI component of the CI/CD pipeline, circumventing the need for direct system access.  
By modifying CI configuration files or other dependencies of the pipeline job, attackers inject malicious commands to effectively poison the pipeline workflow, facilitating unauthorized code execution.  

Successful PPE attacks enable a wide array of actions conducted under the pipeline’s identity.  
Malicious operations may encompass reading secrets accessible to the CI job, acquiring permissions to external assets associated with the job node, distributing seemingly legitimate code and artifacts downstream, and reaching additional hosts and assets within the job node’s network or environment.  

Due to its significant impact, minimal detectability, and various exploitation techniques, the PPE attack poses a pervasive threat.  
For security teams, engineers, and red teamers, comprehending PPE and implementing effective countermeasures is paramount for safeguarding CI/CD environments.  

