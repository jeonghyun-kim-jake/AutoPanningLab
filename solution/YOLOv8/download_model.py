import os
import argparse

current_file_path = os.path.abspath(__file__)
root_folder_path = os.path.abspath(os.path.join(current_file_path, os.pardir))

def readConfigs(folderName, fileName="result.yaml"):
    try:
        import yaml
        # Open the YAML file and read its contents
        with open(folderName+"/"+fileName, 'r') as file:
            data = yaml.safe_load(file)
        return dict(data)
    except OSError as e:
        print("[ERROR] Failed to read config file", e)
        return None
def downloadFileByGoogleDriveFileId(file_id):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    conf_path = os.path.join(root_folder_path+"/../../configs", 'client_secrets.json')
    # Authenticate and create GoogleDrive instance
    gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()  # Follow the prompts to authenticate
    gauth.LoadClientConfigFile(conf_path)
    drive = GoogleDrive(gauth)

    # Download file using link
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(file['title'])  # Save the file to current directory with its original filename
    return file['title']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download google drive files by config file')

    # Define the arguments that your program accepts
    parser.add_argument('--t', help='Target folder', required=True)
    parser.add_argument('--filename', help='Config file name', default="result.yaml")

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Access the values of the arguments
    currentPath = os.getcwd()
    targetPath = os.path.join(currentPath, args.t)
    print("scripts working on ", currentPath)

    configs = readConfigs(targetPath, args.filename)
    if configs is not None and "id" in configs.keys():
        os.chdir(targetPath)
        fileName = downloadFileByGoogleDriveFileId(configs["id"])
        print("[DONE] download ", fileName," at ", targetPath)
        print("[DONE] configs: ", configs)
    else:
        print("[ERROR] path is not valid. ", targetPath)