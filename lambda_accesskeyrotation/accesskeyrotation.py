import boto3
import sys
import json
import traceback

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
  # Read secret string from Secrets Manager
  secret_string = json.loads(
    secrets_client.get_secret_value(
      SecretId=username
    )['SecretString']
  )
  # Copy existing new access keys to old access keys in JSON object.
  secret_string['old_access_key_id'] = secret_string['new_access_key_id']
  secret_string['old_secret_access_key'] = secret_string['new_secret_access_key']

  # Store the newly generated key pair in JSON object.
  secret_string['new_access_key_id'] = access_key['AccessKey']['AccessKeyId']
  secret_string['new_secret_access_key'] = access_key['AccessKey']['SecretAccessKey']
  print(type(secret_string))
  print(secret_string)
  print("======")
  #Store the updated JSON object in secrets manager.
  secrets_client.put_secret_value(
    SecretId=username,
    SecretString=json.dumps(secret_string)
  )

# 100th Day: Disable old access key.
def days100(username):
  secret_string = json.loads(secrets_client.get_secret_value(
      SecretId=username
    )['SecretString'])
  
  if 'old_access_key_id' not in secret_string :
    raise Exception('The user doesnt have old access keys.')
  
  iam_client.update_access_key(
    UserName=username,
    AccessKeyId=secret_string['old_access_key_id'],
    Status='Inactive'
  )

# 110th Day: Delete old keys and rename new key as old key.
def days110(username):
  secret_string = json.loads(
   secrets_client.get_secret_value(
      SecretId=username
   )['SecretString']
  )
  print(json.dumps(secret_string))
  if 'old_access_key_id' not in secret_string:
    raise Exception('The user doesnt have old access keys.')
 
  # Delete the old access key in IAM
  iam_client.delete_access_key(
    UserName=username,
    AccessKeyId=secret_string['old_access_key_id']
  )

  #Delete the old access key in Secrets Manager
  secret_string.pop('old_access_key_id', None)
  secret_string.pop('old_secret_access_key', None)
  secrets_client.put_secret_value(
    SecretId=username,
    SecretString=json.dumps(secret_string)
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
    traceback.print_exc()
    msg = '%s DAYS ERROR: %s'%(days,str(e))
    return {"result":"error", "errormsg":msg}

