terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.57.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Bucket for lateral movement
resource "aws_s3_bucket" "ppe_attack_demo_bucket" {
  bucket = var.s3_bucket_lateral_movement_name
  tags = {
    Environment = "demo"
  }
  force_destroy = true
}

################### Cloud Trail #####################

module "cloudtrail" {
  source = "cloudposse/cloudtrail/aws"
  version     = "0.24.0"
  name                          = "detection"
  enable_log_file_validation    = true
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_logging                = true
  s3_bucket_name                = module.cloudtrail_s3_bucket.bucket_id
}


module "cloudtrail_s3_bucket" {
  source = "cloudposse/cloudtrail-s3-bucket/aws"
  version     = "0.26.4"
  name      = var.s3_bucket_cloudtrail_name
  force_destroy = true
}

#####################################################



# IAM User: ppe-s3-readonly-user
resource "aws_iam_user" "ppe_s3_readonly_user" {
  name = "ppe-s3-readonly-user"
}

resource "aws_iam_user_policy" "ppe_s3_readonly_policy" {
  name   = "ppe-s3-readonly-policy"
  user   = aws_iam_user.ppe_s3_readonly_user.name
  policy = data.aws_iam_policy_document.ppe_s3_readonly_policy.json
}

data "aws_iam_policy_document" "ppe_s3_readonly_policy" {
  statement {
    actions   = ["s3:GetObject", "s3:ListBucket", "s3:ListAllMyBuckets"]
    resources = ["*"]
  }
}

resource "aws_iam_access_key" "ppe_s3_readonly_access_key" {
  user = aws_iam_user.ppe_s3_readonly_user.name
}

# IAM User: vulnerable-iam-user
resource "aws_iam_user" "vulnerable_iam_user" {
  name = "vulnerable-iam-user"
}

resource "aws_iam_user_policy" "vulnerable_iam_policy" {
  name   = "vulnerable-iam-policy"
  user   = aws_iam_user.vulnerable_iam_user.name
  policy = data.aws_iam_policy_document.vulnerable_iam_policy.json
}

data "aws_iam_policy_document" "vulnerable_iam_policy" {
  statement {
    sid       = "Statement1"
    actions   = [
      "iam:Get*",
      "iam:List*",
      "iam:Put*",
      "iam:SimulateCustomPolicy",
      "iam:SimulatePrincipalPolicy"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_access_key" "vulnerable_iam_access_key" {
  user = aws_iam_user.vulnerable_iam_user.name
}
