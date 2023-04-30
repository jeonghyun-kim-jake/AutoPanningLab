import pathlib
import tempfile

def createDir(path, parents=True):
    pathlib.Path(path).mkdir(exist_ok=True, parents=parents)
    
    
    
def createTempDir():
    # Create a temporary directory
    temp_folder = tempfile.TemporaryDirectory()

    # Get the path to the temporary directory
    return temp_folder.name
