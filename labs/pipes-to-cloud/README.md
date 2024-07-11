# From the Pipes to the Cloud

Hack your way from Github Action pipelines to aws!

## NOTE: STILL A WORK-IN-PROGRESS!

## Abstract
This lab enables provisioning of all necessary infrastructure for a demonstration of attack scenarios where a malicious actor starts by compromising a Github Action, performs lateral movement across an AWS account, and eventually escalates aws privileges to root.  

Specifically, the attack comprises the following phases:  

1. Injection of a malicious comment into a Github issue to trigger a Github Action that initiates a reverse shell ([*Poisoned Pipeline Execution*](../../ci-cd/ppe/README.md)). 

2. Extraction of secrets from the runner via the reverse shell, uncovering AWS keys.  

3. Enumeration of AWS resources using the previously extracted secrets, revealing access to read the contents of an S3 bucket.  

4. The bucket contains some files: we uncover additional AWS keys.  

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
We will create one S3 bucket and two IAM users (along with required IAM policies):
- `ppe-s3-readonly-user`
- `vulnerable-iam-user`


Cd to the `infra/aws` directory and create a new file called `secret.tfvars`.  
This file will contain all the variables required to setup the github repository, as well as our aws keys (retrieved from the aws terraform step): 

```sh
aws_region = "your-aws-region-here"
s3_bucket_name ="your-aws-s3-bucket-name-for-this-demo-here"
```  

Now we can proceede with terraform provisioning (note, you need to have aws cli already installed and configured with sufficient rights for this step).  
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
  # aws_iam_access_key.ppe_s3_readonly_access_key will be created
  + resource "aws_iam_access_key" "ppe_s3_readonly_access_key" {
      + create_date                    = (known after apply)
      + encrypted_secret               = (known after apply)
      + encrypted_ses_smtp_password_v4 = (known after apply)
      + id                             = (known after apply)
      + key_fingerprint                = (known after apply)
      + secret                         = (sensitive value)
      + ses_smtp_password_v4           = (sensitive value)
      + status                         = "Active"
      + user                           = "ppe-s3-readonly-user"
    }

  # aws_iam_access_key.vulnerable_iam_access_key will be created
  + resource "aws_iam_access_key" "vulnerable_iam_access_key" {
      + create_date                    = (known after apply)
      + encrypted_secret               = (known after apply)
      + encrypted_ses_smtp_password_v4 = (known after apply)
      + id                             = (known after apply)
      + key_fingerprint                = (known after apply)
      + secret                         = (sensitive value)
      + ses_smtp_password_v4           = (sensitive value)
      + status                         = "Active"
      + user                           = "vulnerable-iam-user"
    }

  # aws_iam_user.ppe_s3_readonly_user will be created
  + resource "aws_iam_user" "ppe_s3_readonly_user" {
      + arn           = (known after apply)
      + force_destroy = false
      + id            = (known after apply)
      + name          = "ppe-s3-readonly-user"
      + path          = "/"
      + tags_all      = (known after apply)
      + unique_id     = (known after apply)
    }

  # aws_iam_user.vulnerable_iam_user will be created
  + resource "aws_iam_user" "vulnerable_iam_user" {
      + arn           = (known after apply)
      + force_destroy = false
      + id            = (known after apply)
      + name          = "vulnerable-iam-user"
      + path          = "/"
      + tags_all      = (known after apply)
      + unique_id     = (known after apply)
    }

  # aws_iam_user_policy.ppe_s3_readonly_policy will be created
  + resource "aws_iam_user_policy" "ppe_s3_readonly_policy" {
      + id          = (known after apply)
      + name        = "ppe-s3-readonly-policy"
      + name_prefix = (known after apply)
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "s3:ListBucket",
                          + "s3:ListAllMyBuckets",
                          + "s3:GetObject",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + user        = "ppe-s3-readonly-user"
    }

  # aws_iam_user_policy.vulnerable_iam_policy will be created
  + resource "aws_iam_user_policy" "vulnerable_iam_policy" {
      + id          = (known after apply)
      + name        = "vulnerable-iam-policy"
      + name_prefix = (known after apply)
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "iam:SimulatePrincipalPolicy",
                          + "iam:SimulateCustomPolicy",
                          + "iam:Put*",
                          + "iam:List*",
                          + "iam:Get*",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                      + Sid      = "Statement1"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + user        = "vulnerable-iam-user"
    }

  # aws_s3_bucket.ppe_attack_demo_bucket will be created
  + resource "aws_s3_bucket" "ppe_attack_demo_bucket" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "s3-bucket-ppe-attack-demo-4421"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = true
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "Environment" = "demo"
        }
      + tags_all                    = {
          + "Environment" = "demo"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + cors_rule (known after apply)

      + grant (known after apply)

      + lifecycle_rule (known after apply)

      + logging (known after apply)

      + object_lock_configuration (known after apply)

      + replication_configuration (known after apply)

      + server_side_encryption_configuration (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 7 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + ppe_s3_readonly_access_key_id     = (known after apply)
  + ppe_s3_readonly_access_key_secret = (sensitive value)
  + vulnerable_iam_access_key_id      = (known after apply)
  + vulnerable_iam_access_key_secret  = (sensitive value)
```  


If you are ok with it, apply!

```sh
terraform apply -var-file="secret.tfvars"
```  

The previous command will take less than a minute to complete and will return the keys ID for the two IAM users:  
```sh
Apply complete! Resources: 7 added, 0 changed, 0 destroyed.

Outputs:

ppe_s3_readonly_access_key_id = "AKI*************"
ppe_s3_readonly_access_key_secret = <sensitive>
vulnerable_iam_access_key_id = "AKI*************"
vulnerable_iam_access_key_secret = <sensitive>
```  

Now you need to add the keys for the `vulnerable-iam-user` inside the local `repo-content` folder.  
In order to do that, open the `terraform.tfstate` file, retrieve both the access key id and access key value for the `vulnerable-iam-user`  
and put them inside a file called `aws_keys.txt` inside the `repo-content` directory.  

Now is time to push that directory to the S3 bucket we created:  
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
Now that we've completed the creation of all required resources on aws, we can proceede with the github setup.  

We will create a repository with a Github Action that automatically prints the body of new comments added to existing issues.   

**Note**: for security reasons we will make the repository private but the same exact attack can be carried out against public repositories!  
This is what make this type of attack so dangerous: **the threat actor only needs to write a comment!**  

Cd to the `infra/github` directory and create a new file called `secret.tfvars`.  
This file will contain all the secrets required to setup the github repository, as well as the aws keys for the `ppe-s3-readonly-user` (retrieved from the aws terraform step): 

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

