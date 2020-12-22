module "lamdba_function" {
  source = "terraform-aws-modules/lambda/aws"
  function_name = "accesskeyrotation_90days"
  handler = "index.lambda_handler"
  runtime = "python3.7"
  source_path="lambda_90days"
  tags = {
    Name = "accesskeyrotation_90days"
  }
}
