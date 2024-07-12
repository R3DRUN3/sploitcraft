terraform {
  required_providers {
    github = {
      source = "integrations/github"
      version = "6.2.3"
    }
  }
}

provider "github" {
  owner = var.gh_owner  
  token = var.gh_token
}

# GitHub Repository
resource "github_repository" "ppe" {
  name        = "ppe"
  description = "Super Popular OSS Repo"
  visibility     = "private"
  auto_init = true
  has_issues = true
}

# README File
resource "github_repository_file" "readme" {
  repository = github_repository.ppe.name
  file       = "README.md"
  content    = file("${path.module}/repo-content/README.md")
  branch = "main"
  overwrite_on_create = true
}

# GitHub Actions Workflow
resource "github_repository_file" "github_actions_workflow" {
  repository = github_repository.ppe.name
  file       = ".github/workflows/issue.yaml"
  content    = file("${path.module}/repo-content/issue.yaml")
  branch     = "main"
}

# GitHub Actions Secret: aws key ID
resource "github_actions_secret" "aws_key_id" {
  repository      = github_repository.ppe.name
  secret_name     = "AWS_ACCESS_KEY_ID"
  plaintext_value = var.github_actions_secret_aws_key_id
}

# GitHub Actions Secret: aws key value
resource "github_actions_secret" "aws_key_value" {
  repository      = github_repository.ppe.name
  secret_name     = "AWS_SECRET_ACCESS_KEY"
  plaintext_value = var.github_actions_secret_aws_key_value
}

# GitHub Issue
resource "github_issue" "default" {
  repository       = github_repository.ppe.name
  title            = "THIS REPO IS NOT SAFE"
  body             = "I've found some security issues of your repo...can we discuss it in private?"
}

