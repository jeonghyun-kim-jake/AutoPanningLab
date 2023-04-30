
from common import createDir
from visions import GoldDetector, captureImageFromCamera

from os.path import isfile, join, abspath


def draw_bounding_box(img, confidence, x, y, x_plus_w, y_plus_h):
    label = f'({confidence:.2f})'
    color = (255, 0, 0)
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

class ParticlePicker:
    def __init__(self, stepMotor, servoMotor, debugPath=None):
        self.goldDetector = GoldDetector()
        # move cylinder
        self.stepMotor = stepMotor
        # push particle
        self.servoMotor = servoMotor
        self.debugPath = debugPath+"/picker" if debugPath is not None else None
        if self.debugPath is not None:
            createDir(self.debugPath)
    
    
    def checkParticle(self):
        path = captureImageFromCamera()
        detections = self.goldDetector.detectFromImagePath(path)
        
        if self.debugPath is not None:
            import shutil            
            import json
            from datetime import datetime
            from pytz import timezone
            savePath = self.debugPath +"/"+ datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d_%H%M_%S")
            createDir(savePath)
            targetPath = join(savePath, "input.png")
            shutil.copy(path, targetPath)
            print("debug file will be saved on ",savePath)
            with open(join(savePath, "result.json"), "w") as outfile:
                json.dump(detections, outfile)
                
        return len(detections) > 0