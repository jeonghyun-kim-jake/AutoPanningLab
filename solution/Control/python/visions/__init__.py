import tempfile
import random
import cv2
import cv2.dnn
import numpy as np
import os

_self_file_path = os.path.realpath(__file__)
_self_base_path = os.path.dirname(_self_file_path)

# Create a temporary directory
vision_folder = tempfile.TemporaryDirectory()

# Get the path to the temporary directory
vision_dir_path = vision_folder.name



def captureImageFromCamera(device_ix=0):
    import cv2
    # Open the first webcam device
    capture = cv2.VideoCapture(device_ix)
    
    # Create a temporary file inside the directory
    save_file = tempfile.NamedTemporaryFile(dir=vision_dir_path, suffix='.png', delete=False)
    # Get the path to the temporary file
    save_path = save_file.name

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

class GoldDetector():
    def __init__(self, modelPath=_self_base_path+"/models/best.onnx"):
        self.model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(modelPath)
        self.CLASSES = ["gold"]
    
    def detectFromCamera(self, camera_idx=0, confidence=0.5):
        return self.detectFromImagePath(captureImageFromCamera(camera_idx), confidence)
    
    def detectFromImagePath(self, img_path, confidence=0.5):
        return self.detectFromImage(cv2.imread(img_path), confidence)

    def detectFromImage(self, original_image, confidence=0.5):
        [height, width, _] = original_image.shape
        print("input image shape", "h:", height, "w:", width) 
        
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image
        scale = length / 640

        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
        self.model.setInput(blob)
        outputs = self.model.forward()
        
        
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        
        boxes = []
        scores = []
        class_ids = []
        
        
        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= confidence:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2], outputs[0][i][3]]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)
        
        
        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        detections = []
        # original_image = cv2.resize(original_image, (640, 480))

        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                'class_id': class_ids[index],
                'class_name': self.CLASSES[class_ids[index]],
                'confidence': scores[index],
                'box': box,
                'scale': scale}
            detections.append(detection)
            
        return detections