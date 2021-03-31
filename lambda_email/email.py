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

ses_client = boto3.client(
  service_name='ses',
  region_name='us-east-1'
)

def days90(username, secrets):
  
     
def days100():
  print('TODO: 100 function.')

def days110():
  print('TODO: 110 function.')


def lambda_handler(event, context):
  try:   
    username = event['username'] 
    secrets = json.loads(secrets_client.get_secret_value(SecretId=username)['SecretString'])
    
    days = event['days']
    daysfunctions = { 
      90: days90,
      100: days100,
      110: days110
    }
    daysfunctions[days](username, secrets)
    
    return { "result": "noerror" }

  except Exception as e:
    msg = '%s DAYS ERROR: %s'%(days,str(e))
    return { "result":"error", "errormsg":msg }

