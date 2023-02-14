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

def verify_local_file(folder_path):
    files_list = os.listdir(folder_path)
    dirs = []
    arquivos = []
    for file_name  in files_list:
        path = os.path.join(folder_path, file_name)
        if os.path.isfile(path):
            dirs.append(path)
            arquivos.append(file_name)
    
    return dirs, arquivos
            
    