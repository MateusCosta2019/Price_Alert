import os 
import boto3
import os

class UploadDataIntoS3:
    """This code defines a class called `UploadDataIntoS3`, which initializes an object used to upload data to Amazon S3."""
    def __init__(
        self,
        s3_bucket:str, 
        folder_path:str, 
        logger):
                
        self.connAws = boto3.client('s3')
        self.s3_bucket = s3_bucket
        self.folder_path = folder_path
        self.logger = logger

    def verify_local_file(self):
        """
        The `verify_local_file()` method scans a folder and returns a list of the file paths and their corresponding file names.
        The method begins by logging an info message indicating that it is starting to scan the files and get their paths. 
        It then attempts to list the files in the folder using `os.listdir()` method, and logs an error message if it fails.

        Next, the method initializes two empty lists, `dirs` and `files_name`, and iterates over the list of files returned from `os.listdir()`. 
        For each file, the method uses `os.path.join()` to construct the full file path and checks if the path is a file using `os.path.isfile()`. 
        If the path is a file, it adds the path to the dirs list and adds the file name to the `files_name` list.

        Finally, the method logs an info message indicating that the paths were returned successfully and returns the `dirs` and `files_name` 
        lists as a tuple. If an error occurs during the method, it logs an error message and returns `False`.

        Here is a summary of the arguments used in this method:

        - `self`: a reference to the current instance of the class.

        Make sure that the folder path passed to the method is correct and that you have the necessary permissions to read the files 
        in the folder.
        """
        self.logger.info('--> Starting to scan the files and getting their path')
        try:
            files_list = os.listdir(self.folder_path)
        except Exception as e:
            self.logger.error(f'--> Unable to list files in folder error: {e}')
        
        dirs = []
        files_name = []

        try:
            for file_name in files_list:
                path = os.path.join(self.folder_path, file_name)
                if os.path.isfile(path):
                    dirs.append(path)
                    files_name.append(file_name)
            
            self.logger.info('--> paths returned successfully')
            return dirs, files_name
        except Exception as e:
            self.logger.error(f'--> Unable to return files path error: {e}')
            return False

    def upload_to_s3(self): 
        """
        This code defines a method called `upload_to_s3()` that uploads files to an Amazon S3 bucket. The method first calls the 
        `verify_local_file()` method, which returns a tuple containing the paths to the local files and their corresponding names.
        The method then iterates over the paths and files using `zip()`, and uploads each file to the S3 bucket using the `upload_file()`
        method of the `connAws` object. The method returns `True` if the upload is successful, and `False` if it fails, along with a log 
        message indicating the reason for the failure.

        Here's a brief overview of the arguments used in this method:

        - `self`: a reference to the current instance of the class.
        - `path_to_files`: a list of local file paths to be uploaded to S3.
        - `arquivo`: a list of filenames corresponding to the files to be uploaded.
        - `s3_bucket`: the name of the S3 bucket to upload the files to.
        
        Note that the `connAws` object used in the `upload_file()` method is assumed to have been initialized elsewhere in the class.
        """      
    
        path_to_files, arquivo = self.verify_local_file()  
        self.logger.info("--> Starting upload to bucket")    
        try:
            for path_files, files in zip(path_to_files, arquivo):
                self.connAws.upload_file(path_files, self.s3_bucket, f'Raw/{files}')

            self.logger.info("--> Upload done successfully")
            return True
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            return False
    
    def drop_files(self):
        """
        This code defines a method called `drop_files()` that is used to delete local files after the completion of uploading to Amazon S3. 
        The method first calls the `verify_local_file()` method to get a list of local files and their names.
        
        The method then iterates through the list of files using `zip()` and attempts to delete each file using the `os.remove()` method. 
        If the deletion is successful, the method logs a message indicating that the file has been successfully deleted. If an error occurs 
        while deleting the file, the method logs a message indicating that the file does not exist and returns `False`.

        Here is a summary of the arguments used in this method:

        - `self`: a reference to the current instance of the class.
        - `local_files`: a list of local file paths to be deleted.
        - `arquivo`: a list of file names corresponding to the files to be deleted.

        Make sure that the files you want to delete exist in the specified path and that you have permission to delete them. Also, 
        note that deleting files is a destructive operation and cannot be undone, so be careful when using this method.
        
        """
        local_files, arquivo = self.verify_local_file()
        for path_files, files in zip(local_files, arquivo):
            try:
                os.remove(path_files)
                self.logger.info(f"{files} deleted successfully")
            except Exception as e:
                self.logger.error(f"{files} does not exist")
                return False