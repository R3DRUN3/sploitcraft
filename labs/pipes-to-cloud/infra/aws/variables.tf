variable "aws_region" {
  description = "The AWS region to create resources in"
  type        = string
  sensitive   = false
}

variable "s3_bucket_lateral_movement_name" {
  description = "The name of the s3 bucket for lateral movement" # must be unique!
  type        = string
  sensitive   = false
}

variable "s3_bucket_cloudtrail_name" {
  description = "The name of the s3 bucket for cloudtrail" # must be unique!
  type        = string
  sensitive   = false
}
