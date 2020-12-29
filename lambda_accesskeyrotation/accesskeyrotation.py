import boto3
import sys
import json

secrets_client = boto3.client(
  service_name='secretsmanager',
  region_name='us-east-1'
)

iam_client = boto3.client(
  service_name='iam',
  region_name='us-east-1'
)

# 90th Day: Generate new Access key and store it in Secrets Manager as "new"
def days90(username):
  # Generate new access key for the user
  access_key = iam_client.create_access_key(
    UserName=username
  )
  
  # Store the access key in Secrets Manager
  access_key_json = '{ "new_access_key_id": "%s", "new_secret_access_key": "%s" }'%(access_key['AccessKey']['AccessKeyId'],access_key['AccessKey']['SecretAccessKey'])
  secrets_client.put_secret_value(
    SecretId=username,
    SecretString=access_key_json
  )

# 100th Day: Disable old access key.
def days100(username):
  access_key_id = json.load(secrets_client.get_secret_value(
      SecretId=username
    )['SecretString'])['old_access_key_id']

  iam_client.update_access_key(
    UserName=username,
    AccessKeyId=access_key_id,
    Status='Inactive'
  )

def days110(username):
  access_key_id = json.load(secrets_client.get_secret_value(
      SecretId=username
    )['SecretString'])['old_access_key_id']
  
  iam_client.delete_access_key(
    UserName=username,
    AccessKeyId=access_key_id
  )

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

