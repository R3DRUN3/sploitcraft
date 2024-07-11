output "ppe_s3_readonly_access_key_id" {
  value = aws_iam_access_key.ppe_s3_readonly_access_key.id
}

output "ppe_s3_readonly_access_key_secret" {
  value     = aws_iam_access_key.ppe_s3_readonly_access_key.secret
  sensitive = true
}

output "vulnerable_iam_access_key_id" {
  value = aws_iam_access_key.vulnerable_iam_access_key.id
}

output "vulnerable_iam_access_key_secret" {
  value     = aws_iam_access_key.vulnerable_iam_access_key.secret
  sensitive = true
}
