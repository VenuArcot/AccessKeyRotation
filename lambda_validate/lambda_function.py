import boto3
from botocore.exceptions import ClientError
iam_client = boto3.client('iam')
sm_client = boto3.client('secretsmanager',region_name='us-east-1')

def lambda_handler(event, context):
  all_users = iam_client.list_users()['Users']
  for user in all_users:
    userid = user['UserId']
    usersecret = sm_client.list_secrets(
                    Filters=[
                        {
                            'Key': 'name',
                            'Values': [userid, ]
                        },
                    ],
                )['SecretList']
    print(usersecret == [])

if __name__ == "__main__":
  lambda_handler(None, None)
