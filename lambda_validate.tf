module "lamdba_function" {
  source = "terraform-aws-modules/lambda/aws"
  function_name = "accesskeyrotation_validate"
  handler = "index.lambda_handler"
  runtime = "python3.7"
  source_path="lambda_validate"
  tags = {
    Name = "accesskeyrotation_validate"
  }
}