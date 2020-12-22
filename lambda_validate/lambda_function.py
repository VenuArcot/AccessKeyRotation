import boto3
from OpenSSL import crypto
from botocore.exceptions import ClientError

iam_client = boto3.client('iam')
ses_client = boto3.client('ses',region_name='us-east-1')

sm_client = boto3.client('secretsmanager',region_name='us-east-1')

def generate_encryption_keys():
    
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair

    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "Irving"
    cert.get_subject().O = "WDTC"
    cert.get_subject().OU = "WDTC"
    cert.get_subject().CN = "WDTC"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # 1 year expiry date
    cert.set_issuer(cert.get_subject())  # self-sign this certificate

    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    email_encrypt_cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    email_encrypt_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
    
    return [email_encrypt_cert, email_encrypt_key] 

def create_secret(userid):
    email_encrypt_keys = generate_encryption_keys()
    return True

def is_source_email_verified():
    return ses_client.get_identity_verification_attributes(Identities=['disney.com',])['VerificationAttributes'] != {}


def lambda_handler(event, context):
    
    # Check if the source email is verified
    if not is_source_email_verified():
        raise Exception('Source email verification failed!')
        return False
    else:
        print('Source email verification passed!')

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
        if usersecret == []:
            create_secret(userid=userid)

if __name__ == "__main__":
    lambda_handler(None, None)
