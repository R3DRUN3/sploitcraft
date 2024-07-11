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

# S3 Bucket
resource "aws_s3_bucket" "ppe_attack_demo_bucket" {
  bucket = var.s3_bucket_name
  tags = {
    Environment = "demo"
  }
  force_destroy = true
}


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
