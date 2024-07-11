variable "aws_region" {
  description = "The AWS region to create resources in"
  type        = string
  sensitive   = false
}

variable "s3_bucket_name" {
  description = "The name of the s3 bucket" # must be unique!
  type        = string
  sensitive   = false
}
