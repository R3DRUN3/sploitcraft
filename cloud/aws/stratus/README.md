# AWS RED TEAM WITH STRATUS

[*Stratus Red Team*](https://github.com/DataDog/stratus-red-team) is a  cybersecurity tool designed to simulate advanced persistent threat (APT) attacks, allowing organizations to test the resilience of their security defenses.  
When used on AWS (Amazon Web Services), Stratum Red Team can help organizations assess their cloud security posture by emulating real-world cyber attacks in a controlled environment.  
This enables security teams to identify vulnerabilities, improve detection and incident response strategies, and enhance overall cloud security measures, ensuring that their AWS infrastructure is robust against potential threats.  
You can think of *stratus* like [*atomic red team*](../../../windows/atomic-red-team/) but for the cloud.  

In this brief guide, we will learn how to use it against an aws account.  

## Prerequisites
- *Docker*
- *aws* account


## Instructions
Set all the required environment variables (`AWS_ACCESS_KEY_ID`,  `AWS_SECRET_ACCESS_KEY` and `AWS_DEFAULT_REGION`)  
and set the alias for `stratus` with the following command (this will launch the tool via `docker`):  
```sh
IMAGE="ghcr.io/datadog/stratus-red-team"
alias stratus="docker run --rm -v $HOME/.stratus-red-team/:/root/.stratus-red-team/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION $IMAGE"
```  
Now you can list all the available aws techniques:      
```sh
$ stratus list --platform aws --mitre-attack-tactic persistence

```  

Output example:  
```console
+-------------------------------------------------------------+-----------------------------------------------------------+----------+----------------------+
| TECHNIQUE ID                                                | TECHNIQUE NAME                                            | PLATFORM | MITRE ATT&CK TACTIC  |
+-------------------------------------------------------------+-----------------------------------------------------------+----------+----------------------+
| aws.credential-access.ec2-get-password-data                 | Retrieve EC2 Password Data                                | AWS      | Credential Access    |
| aws.credential-access.ec2-steal-instance-credentials        | Steal EC2 Instance Credentials                            | AWS      | Credential Access    |
| aws.credential-access.secretsmanager-batch-retrieve-secrets | Retrieve a High Number of Secrets Manager secrets (Batch) | AWS      | Credential Access    |
| aws.credential-access.secretsmanager-retrieve-secrets       | Retrieve a High Number of Secrets Manager secrets         | AWS      | Credential Access    |
| aws.credential-access.ssm-retrieve-securestring-parameters  | Retrieve And Decrypt SSM Parameters                       | AWS      | Credential Access    |
| aws.defense-evasion.cloudtrail-delete                       | Delete CloudTrail Trail                                   | AWS      | Defense Evasion      |
| aws.defense-evasion.cloudtrail-event-selectors              | Disable CloudTrail Logging Through Event Selectors        | AWS      | Defense Evasion      |
| aws.defense-evasion.cloudtrail-lifecycle-rule               | CloudTrail Logs Impairment Through S3 Lifecycle Rule      | AWS      | Defense Evasion      |
| aws.defense-evasion.cloudtrail-stop                         | Stop CloudTrail Trail                                     | AWS      | Defense Evasion      |
| aws.defense-evasion.dns-delete-logs                         | Delete DNS query logs                                     | AWS      | Defense Evasion      |
| aws.defense-evasion.organizations-leave                     | Attempt to Leave the AWS Organization                     | AWS      | Defense Evasion      |
| aws.defense-evasion.vpc-remove-flow-logs                    | Remove VPC Flow Logs                                      | AWS      | Defense Evasion      |
| aws.discovery.ec2-enumerate-from-instance                   | Execute Discovery Commands on an EC2 Instance             | AWS      | Discovery            |
| aws.discovery.ec2-download-user-data                        | Download EC2 Instance User Data                           | AWS      | Discovery            |
| aws.discovery.ses-enumerate                                 | Enumerate SES                                             | AWS      | Discovery            |
| aws.execution.ec2-launch-unusual-instances                  | Launch Unusual EC2 instances                              | AWS      | Execution            |
| aws.execution.ec2-user-data                                 | Execute Commands on EC2 Instance via User Data            | AWS      | Execution            |
|                                                             |                                                           |          | Privilege Escalation |
| aws.execution.ssm-send-command                              | Usage of ssm:SendCommand on multiple instances            | AWS      | Execution            |
| aws.execution.ssm-start-session                             | Usage of ssm:StartSession on multiple instances           | AWS      | Execution            |
| aws.exfiltration.ec2-security-group-open-port-22-ingress    | Open Ingress Port 22 on a Security Group                  | AWS      | Exfiltration         |
| aws.exfiltration.ec2-share-ami                              | Exfiltrate an AMI by Sharing It                           | AWS      | Exfiltration         |
| aws.exfiltration.ec2-share-ebs-snapshot                     | Exfiltrate EBS Snapshot by Sharing It                     | AWS      | Exfiltration         |
| aws.exfiltration.rds-share-snapshot                         | Exfiltrate RDS Snapshot by Sharing                        | AWS      | Exfiltration         |
| aws.exfiltration.s3-backdoor-bucket-policy                  | Backdoor an S3 Bucket via its Bucket Policy               | AWS      | Exfiltration         |
| aws.impact.s3-ransomware-batch-deletion                     | S3 Ransomware through batch file deletion                 | AWS      | Impact               |
| aws.impact.s3-ransomware-client-side-encryption             | S3 Ransomware through client-side encryption              | AWS      | Impact               |
| aws.impact.s3-ransomware-individual-deletion                | S3 Ransomware through individual file deletion            | AWS      | Impact               |
| aws.initial-access.console-login-without-mfa                | Console Login without MFA                                 | AWS      | Initial Access       |
| aws.lateral-movement.ec2-instance-connect                   | Usage of EC2 Instance Connect on multiple instances       | AWS      | Lateral Movement     |
| aws.persistence.iam-backdoor-role                           | Backdoor an IAM Role                                      | AWS      | Persistence          |
| aws.persistence.iam-backdoor-user                           | Create an Access Key on an IAM User                       | AWS      | Persistence          |
|                                                             |                                                           |          | Privilege Escalation |
| aws.persistence.iam-create-admin-user                       | Create an administrative IAM User                         | AWS      | Persistence          |
|                                                             |                                                           |          | Privilege Escalation |
| aws.persistence.iam-create-backdoor-role                    | Create a backdoored IAM Role                              | AWS      | Persistence          |
| aws.persistence.iam-create-user-login-profile               | Create a Login Profile on an IAM User                     | AWS      | Persistence          |
|                                                             |                                                           |          | Privilege Escalation |
| aws.persistence.lambda-backdoor-function                    | Backdoor Lambda Function Through Resource-Based Policy    | AWS      | Persistence          |
| aws.persistence.lambda-layer-extension                      | Add a Malicious Lambda Extension                          | AWS      | Persistence          |
|                                                             |                                                           |          | Privilege Escalation |
| aws.persistence.lambda-overwrite-code                       | Overwrite Lambda Function Code                            | AWS      | Persistence          |
| aws.persistence.rolesanywhere-create-trust-anchor           | Create an IAM Roles Anywhere trust anchor                 | AWS      | Persistence          |
|                                                             |                                                           |          | Privilege Escalation |
+-------------------------------------------------------------+-----------------------------------------------------------+----------+----------------------+
```  

If you want to list techniques for categories (based upon the [*MITRE ATT&CK®*](https://attack.mitre.org/matrices/enterprise/cloud/)) , you can use the `--mitre-attack-tactic` flag.    
For example, for `credential access` techniques:  
```sh
stratus list --platform aws --mitre-attack-tactic "Credential Access"
```  

Output example:  
```console
+-------------------------------------------------------------+-----------------------------------------------------------+----------+---------------------+
| TECHNIQUE ID                                                | TECHNIQUE NAME                                            | PLATFORM | MITRE ATT&CK TACTIC |
+-------------------------------------------------------------+-----------------------------------------------------------+----------+---------------------+
| aws.credential-access.ec2-get-password-data                 | Retrieve EC2 Password Data                                | AWS      | Credential Access   |
| aws.credential-access.ec2-steal-instance-credentials        | Steal EC2 Instance Credentials                            | AWS      | Credential Access   |
| aws.credential-access.secretsmanager-batch-retrieve-secrets | Retrieve a High Number of Secrets Manager secrets (Batch) | AWS      | Credential Access   |
| aws.credential-access.secretsmanager-retrieve-secrets       | Retrieve a High Number of Secrets Manager secrets         | AWS      | Credential Access   |
| aws.credential-access.ssm-retrieve-securestring-parameters  | Retrieve And Decrypt SSM Parameters                       | AWS      | Credential Access   |
+-------------------------------------------------------------+-----------------------------------------------------------+----------+---------------------+
```  

Let's now use *stratus* to retrieve secrets from aws secret manager:    
```sh
stratus show aws.credential-access.secretsmanager-retrieve-secrets 
```  

Output:  
```console
Retrieves a high number of Secrets Manager secrets, through secretsmanager:GetSecretValue.

Warm-up: 

- Create multiple secrets in Secrets Manager.

Detonation: 

- Enumerate the secrets through secretsmanager:ListSecrets
- Retrieve each secret value, one by one through secretsmanager:GetSecretValue
```  

As you can see from the command description `Warm-up` phase, this will create multiple secrets in aws secret manager (via terraform).  

Now launch the attack:  
```sh
stratus detonate aws.credential-access.secretsmanager-retrieve-secrets
```  

Output example:  
```console
2024/08/14 12:33:30 Checking your authentication against AWS
2024/08/14 12:33:31 Installing Terraform in /root/.stratus-red-team/terraform
2024/08/14 12:33:39 Warming up aws.credential-access.secretsmanager-retrieve-secrets
2024/08/14 12:33:39 Initializing Terraform to spin up technique prerequisites
2024/08/14 12:34:04 Applying Terraform to spin up technique prerequisites
2024/08/14 12:34:18 20 Secrets Manager secrets ready
2024/08/14 12:34:18 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-14-jTvs8d
2024/08/14 12:34:18 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-12-RRl8Nd
2024/08/14 12:34:19 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-19-aNTKD9
2024/08/14 12:34:19 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-10-mNQYaa
2024/08/14 12:34:19 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-6-H1kfsh
2024/08/14 12:34:19 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-15-bXR5Re
2024/08/14 12:34:19 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-13-8wZ490
2024/08/14 12:34:20 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-2-Lw5D32
2024/08/14 12:34:20 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-17-GuMMP0
2024/08/14 12:34:20 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-5-6LCTn9
2024/08/14 12:34:20 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-18-mIgBM3
2024/08/14 12:34:21 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-11-JG72S1
2024/08/14 12:34:21 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-4-0SlsT8
2024/08/14 12:34:21 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-1-KQ5n66
2024/08/14 12:34:21 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-7-EDQcB1
2024/08/14 12:34:22 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-8-xaFmDL
2024/08/14 12:34:22 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-16-U8wNJL
2024/08/14 12:34:22 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-9-L4W5fH
2024/08/14 12:34:22 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-0-WJNN9K
2024/08/14 12:34:23 Retrieving value of secret arn:aws:secretsmanager:eu-north-1:009160063618:secret:stratus-red-team-retrieve-secret-3-rFkCwH
```  


The techniques has completed, We can verify this using:  
```sh
stratus status 
```  

Output:  
```console
+-------------------------------------------------------------+------------------------------------------------------------------+-----------+
| ID                                                          | NAME                                                             | STATUS    |
+-------------------------------------------------------------+------------------------------------------------------------------+-----------+
| aws.credential-access.ec2-get-password-data                 | Retrieve EC2 Password Data                                       | COLD      |
| aws.credential-access.ec2-steal-instance-credentials        | Steal EC2 Instance Credentials                                   | COLD      |
| aws.credential-access.secretsmanager-batch-retrieve-secrets | Retrieve a High Number of Secrets Manager secrets (Batch)        | COLD      |
| aws.credential-access.secretsmanager-retrieve-secrets       | Retrieve a High Number of Secrets Manager secrets                | DETONATED |
| aws.credential-access.ssm-retrieve-securestring-parameters  | Retrieve And Decrypt SSM Parameters                              | COLD      |
```  

To clear the resources launch:  
```sh
stratus cleanup aws.credential-access.secretsmanager-retrieve-secrets
```  

Output example:  
```console
2024/08/14 12:40:34 Cleaning up aws.credential-access.secretsmanager-retrieve-secrets
2024/08/14 12:40:34 Cleaning up technique prerequisites with terraform destroy
+-------------------------------------------------------+---------------------------------------------------+--------+
| ID                                                    | NAME                                              | STATUS |
+-------------------------------------------------------+---------------------------------------------------+--------+
| aws.credential-access.secretsmanager-retrieve-secrets | Retrieve a High Number of Secrets Manager secrets | COLD   |
+-------------------------------------------------------+---------------------------------------------------+--------+
```  


> Note  
> remember that you can also launch the various stage one at the time   
> for example via `stratus warmup <technique-id>` and, in a second moment `stratus detonate <tehcnique-id>`.     

In the following video, you can see a new stratus module to test llmhijacking on [*aws bedrock*](https://aws.amazon.com/bedrock/):  















