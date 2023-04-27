import tempfile
import random

# Create a temporary directory
vision_folder = tempfile.TemporaryDirectory()

# Get the path to the temporary directory
vision_dir_path = vision_folder.name



## 
test_detecting = 1

def detectGold(img_path):
    global test_detecting
    test_detecting+=1
    if test_detecting % 10 == 0:
        return True, random.randint(30, 100)
    
    return False, 0
    

def readImageFromCamera(save_path, device_ix=0):
    import cv2
    # Open the first webcam device
    capture = cv2.VideoCapture(device_ix)

    # Check if the webcam is opened correctly
    if not capture.isOpened():
        print("Cannot open camera")
        return None

    # Read a frame from the webcam
    ret, frame = capture.read()

    # Check if the frame is empty
    if not ret:
        print("Failed to read")
        return None
    # Release the webcam and destroy all windows
    capture.release()
    cv2.destroyAllWindows()
    cv2.imwrite(save_path, cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA))
    return save_path

def checkParticle():
    print("checkParticle")
    
    # Create a temporary file inside the directory
    save_file = tempfile.NamedTemporaryFile(dir=vision_dir_path, suffix='.png', delete=False)
    # Get the path to the temporary file
    save_file_path = save_file.name
    
    save_file_path = readImageFromCamera(save_file_path)
    
    if save_file_path is not None:
        print("img saved ", save_file_path)
        
        detected, position = detectGold(save_file_path)
        return detected, position
    
    
    return False, 0