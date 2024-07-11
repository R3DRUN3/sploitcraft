variable "gh_owner" {
  description = "github account/org"
  type        = string
  sensitive   = false
}

variable "gh_token" {
  description = "github token for authentication"
  type        = string
  sensitive   = true
}

variable "github_actions_secret_aws_key_id" {
  description = "aws secret access key id"
  type        = string
  sensitive   = true
}

variable "github_actions_secret_aws_key_value" {
  description = "aws secret access key value"
  type        = string
  sensitive   = true
}
