import gnupg
import boto3
import sys
import json

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

def days90(username):
  # Generate new access key for the user
  access_key = iam_client.create_access_key(
    UserName=username
  )
  
  # Store the access key in Secrets Manager
  access_key_json='{"new_access_key": "%s", "new_secret_access_key": "%s"}'%(access_key['AccessKey']['AccessKeyId'],access_key['AccessKey']['SecretAccessKey'])
  secrets_client.put_secret_value(
    SecretId=username,
    SecretString=access_key_json
  )

def days100():
  print('TODO: 100 function.')

def days110():
  print('TODO: 110 function.')


def lambda_handler(event, context):
  try:   
    username = event['username'] 

    days = event['days']
    daysfunctions = { 
      90: days90,
      100: days100,
      110: days110
    }
    daysfunctions[days](username)
    
    return {"result":"email", "days":days}

  except Exception as e:
    msg = '%s DAYS ERROR: %s'%(days,str(e))
    return {"result":"error", "errormsg":msg}

