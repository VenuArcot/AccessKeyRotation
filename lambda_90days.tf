resource "aws_iam_policy" "policy" {
  name        = "inline_lambda_policy"
  description = "A policy granting resource access to AccessKeyRotation lambda functions"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "secretsmanager:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
        "iam:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "accesskeyrotation_lambda_role" {

  assume_role_policy = <<EOF
{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Effect": "Allow"
        }
      ]
    }
EOF
}

resource "aws_iam_role_policy_attachment" "test_attach" {
  role       = aws_iam_role.accesskeyrotation_lambda_role.name
  policy_arn = aws_iam_policy.policy.arn
}

data "archive_file" "lambda90days" {
  type        = "zip"
  source_dir = "lambda_90days"
  output_path = "lambda90days.zip"
}

module "lamdba_function" {
  source        = "github.com/terraform-module/terraform-aws-lambda?ref=v2.9.0"
  function_name = "accesskeyrotation_90days"
  handler       = "lambda90days.lambda_handler"
  runtime       = "python3.7"
  filename      = "lambda90days.zip"
  source_code_hash = data.archive_file.lambda90days.output_base64sha256
  description   = ""
  memory_size    = "128"
  concurrency    = "5"
  lambda_timeout = "20"
  log_retention  = "1"
  role_arn      = aws_iam_role.accesskeyrotation_lambda_role.arn
  tags = {
    name = "accesskeyrotation_90days"
  }
}
