import gnupg
import boto3
import sys
from botocore.exceptions import ClientError

gpg = gnupg.GPG('/usr/bin/gpg')

secrets_client = boto3.client(
    service_name='secretsmanager',
    region_name='us-east-1'
)
iam_client = boto3.client(
     service_name='iam',
     region_name='us-east-1'
)

user_name = sys.argv[1]

user = iam_client.get_user(
    UserName=user_name
)

access_key = iam_client.create_access_key(
    UserName=user_name
)
access_key_json='{"new_access_key": "%s", "new_secret_access_key": "%s"}'%(access_key['AccessKey']['AccessKeyId'],access_key['AccessKey']['SecretAccessKey'])
print(access_key_json)
secrets_client.put_secret_value(
    SecretId=user_name,
    SecretString=access_key_json
)

