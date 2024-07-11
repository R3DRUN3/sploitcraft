# From the Pipes to the Cloud

Hack your way from Github Action pipelines to aws!

## NOTE: STILL A WORK-IN-PROGRESS!

## Abstract
This lab enables provisioning of all necessary infrastructure for a demonstration of attack scenarios where a malicious actor starts by compromising a Github Action, performs lateral movement across an AWS account, and eventually escalates aws privileges to root.  

Specifically, the attack comprises the following phases:  

1. Injection of a malicious comment into a Github issue to trigger a Github Action that initiates a reverse shell ([*Poisoned Pipeline Execution*](../../ci-cd/ppe/README.md)). 

2. Extraction of secrets from the runner via the reverse shell, uncovering AWS keys.  

3. Enumeration of AWS resources using the previously extracted secrets, revealing access to read the contents of an S3 bucket.  

4. The bucket contains a Git repository; using GitLeaks, we uncover additional AWS keys in previous commits.  

5. Leveraging these keys, we employ Pacu to perform privilege escalation and gain root access across the entire AWS account.  

![attack](./images/attack.png)  


## Prerequisites
- [*python*](https://www.python.org/downloads/)
- [*terraform*](https://www.terraform.io/)
- [*github*](https://github.com/) account
- [*aws*](https://aws.amazon.com/) account 
- [*ngrok*](https://ngrok.com/) account
- [*aws cli*](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [*pacu*](https://github.com/RhinoSecurityLabs/pacu)

## Infrastructure Provisioning
In order for the lab to work, we need to provision some infrastructure, in particular:

- a github repository
- some aws resources

We will use `terraform` for this task.  

### aws setup
First we will setup the required aws environment.  



### github setup
Now that we've completed the creation of all required resources on aws, we can proceede with the github setup.  

We will create a repository with a Github Action that automatically prints the body of new comments added to existing issues.   

**Note**: for security reasons we will make the repository private but the same exact attack can be carried out against public repositories!  
This is what make this type of attack so dangerous: **the threat actor only needs to write a comment!**  

Cd to the `infra/github` directory and create a new file called `secret.tfvars`.  
This file will contain all the secrets required to setup the github repository, as well as our aws keys (retrieved from the aws terraform step): 

```sh
gh_owner = "your-github-account-or-org-here"
gh_token="your-github-pat-here"
github_actions_secret_aws_key_id="your-aws-secret-key-id-here"
github_actions_secret_aws_key_value="your-aws-secret-key-value-here"
``` 

Init the terraform module:  
```sh
terraform init
```  


Now launch a terraform plan by specifying the secret's file:  

```sh
terraform plan -var-file="secret.tfvars"
```  

The plan should look similar to this:  

```sh
Terraform will perform the following actions:

  # github_actions_secret.aws_key_id will be created
  + resource "github_actions_secret" "aws_key_id" {
      + created_at      = (known after apply)
      + id              = (known after apply)
      + plaintext_value = (sensitive value)
      + repository      = "ppe"
      + secret_name     = "AWS_ACCESS_KEY_ID"
      + updated_at      = (known after apply)
    }

  # github_actions_secret.aws_key_value will be created
  + resource "github_actions_secret" "aws_key_value" {
      + created_at      = (known after apply)
      + id              = (known after apply)
      + plaintext_value = (sensitive value)
      + repository      = "ppe"
      + secret_name     = "AWS_SECRET_ACCESS_KEY"
      + updated_at      = (known after apply)
    }

  # github_repository.ppe will be created
  + resource "github_repository" "ppe" {
      + allow_auto_merge            = false
      + allow_merge_commit          = true
      + allow_rebase_merge          = true
      + allow_squash_merge          = true
      + archived                    = false
      + auto_init                   = true
      + default_branch              = (known after apply)
      + delete_branch_on_merge      = false
      + description                 = "Super Popular OSS Repo"
      + etag                        = (known after apply)
      + full_name                   = (known after apply)
      + git_clone_url               = (known after apply)
      + has_issues                  = true
      + html_url                    = (known after apply)
      + http_clone_url              = (known after apply)
      + id                          = (known after apply)
      + merge_commit_message        = "PR_TITLE"
      + merge_commit_title          = "MERGE_MESSAGE"
      + name                        = "ppe"
      + node_id                     = (known after apply)
      + primary_language            = (known after apply)
      + private                     = (known after apply)
      + repo_id                     = (known after apply)
      + squash_merge_commit_message = "COMMIT_MESSAGES"
      + squash_merge_commit_title   = "COMMIT_OR_PR_TITLE"
      + ssh_clone_url               = (known after apply)
      + svn_url                     = (known after apply)
      + topics                      = (known after apply)
      + visibility                  = "private"
      + web_commit_signoff_required = false

      + security_and_analysis (known after apply)
    }

  # github_repository_file.github_actions_workflow will be created
  + resource "github_repository_file" "github_actions_workflow" {
      + branch              = "main"
      + commit_message      = (known after apply)
      + commit_sha          = (known after apply)
      + content             = <<-EOT
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
        EOT
      + file                = ".github/workflows/issue.yaml"
      + id                  = (known after apply)
      + overwrite_on_create = false
      + ref                 = (known after apply)
      + repository          = "ppe"
      + sha                 = (known after apply)
    }

  # github_repository_file.readme will be created
  + resource "github_repository_file" "readme" {
      + branch              = "main"
      + commit_message      = (known after apply)
      + commit_sha          = (known after apply)
      + content             = <<-EOT
            # PPE
            
            Super Popular Open Source Repo!
        EOT
      + file                = "README.md"
      + id                  = (known after apply)
      + overwrite_on_create = true
      + ref                 = (known after apply)
      + repository          = "ppe"
      + sha                 = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + repository_url = (known after apply)
```  

If you are ok with it, apply!

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

