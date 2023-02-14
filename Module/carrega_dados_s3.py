import os 
import boto3

connAws = boto3.client('s3')

def upload_to_s3(local_file, s3_bucket, s3_file):               
    try:
        connAws.upload_file(local_file, s3_bucket, s3_file)
        print("Upload realizado com sucesso")
        return True
    except Exception as e:
        print("Upload falhou: ", e)
        return False
