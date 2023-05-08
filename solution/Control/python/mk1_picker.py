
from common import createDir
from visions import GoldDetector, captureImageFromCamera

from os.path import isfile, join, abspath


CAMERA_DIAMETER : float = 2.1
CAMERA_WIDTH : float =  640.0
CAMERA_HEIGHT: float = 480.0

def plot_cylinder(savePath, x=[], y=[]):
    from matplotlib import pyplot as plt
    from matplotlib.patches import Rectangle
    plt.cla()
    plt.plot(x, y, 'or')
    plt.xlim(-4.7, 4.7)
    plt.ylim(-4.7, 4.7)
    plt.grid(axis='x', color='red', linestyle=':')
    plt.gca().add_patch(plt.Circle((0, 0), radius=4.7, color='blue', clip_on=True))
    plt.gca().add_patch(Rectangle((-1.05,1.6), 2.1,2.1,
                        edgecolor='orange',
                        facecolor='grey',
                        lw=2))
    plt.gca().add_patch(Rectangle((1.3,-3.0), 0.3, 4,
                        edgecolor='white',
                        facecolor='grey',
                        lw=2))
    plt.gca().add_patch(plt.Circle((0, 1.6+(2.1/2)), radius=(2.1/2), color='yellow', fill=False, linestyle='--'))
    plt.savefig(savePath)    

def draw_bounding_box(img, confidence, x, y, x_plus_w, y_plus_h):
    label = f'({confidence:.2f})'
    color = (255, 0, 0)
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def draw_bounding_box_with_detections(img, detections):
    for detection in detections:   
        print("draw_bounding_box_with_detections", detection)
        x = detection["scaled_box"][0]
        y = detection["scaled_box"][1]
        x_plus_w = detection["scaled_box"][2]
        y_plus_h = detection["scaled_box"][3]
        color = (0, 255, 0)        
        
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    
    
class CylinderMatrix:
    def __init__(self, radius, stepRes):
        self.radius = radius
        self.stepRes = stepRes
        self.singleRes = radius / (stepRes/4)
        print("CylinderMatrix:: created ", self.radius, "stepRes:" ,self.stepRes, "singleRes", self.singleRes)
        
    def move(self, from_x, to_x, reverse=True):
        move_dist = to_x - from_x 
        direct = True
        if reverse and move_dist < 0 :
            direct = False
            move_dist = abs(move_dist)
        step = int (move_dist / self.singleRes)
        ret = from_x + (self.singleRes * step if direct else (-1)*self.singleRes*step)
        print("CylinderMatrix:: move ",step, " :: (", from_x, "->", to_x, " == ", ret)
        return step
    
class ScaledMatrix:
    def __init__(self, x=0, y=0, scaled_x=1.0, scaled_y=1.0):
        self.start_x = x
        self.start_y = y
        self.scaled_x = scaled_x
        self.scaled_y = scaled_y
        
    def scaled(self, scaled_x, scaled_y):
        self.scaled_x = scaled_x
        self.scaled_y = scaled_y
        
    def x(self, x):
        return self.start_x + (x*self.scaled_x)
    
    def y(self, y):
        return self.start_y  + (y*self.scaled_y)

    
def conver_detections_to_x(detections, scaledMat):
    return [ (scaledMat.x(d["scaled_box"][0]),
             scaledMat.y(d["scaled_box"][1]), 
             scaledMat.x(d["scaled_box"][2]), 
             scaledMat.y(d["scaled_box"][3]))
           for d in detections]
    
import decimal        
import json
import numpy as np
import cv2

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, np.float32):
            return float(o)
        return super(DecimalEncoder, self).default(o)        
        
class ParticlePicker:
    def __init__(self, stepMotor, servoMotor, debugPath=None):
        self.goldDetector = GoldDetector()
        # move cylinder
        self.stepMotor = stepMotor
        # push particle
        self.servoMotor = servoMotor
        self.servoMotor.rotateOnce(0)
        # cylinder movement
        self.cylinderMatrix = CylinderMatrix(radius=4.7, stepRes=self.stepMotor.getStepsPerRevolution())
        self.scaledMatrix = ScaledMatrix(-1.05, 1.6, scaled_x=CAMERA_DIAMETER/CAMERA_WIDTH, scaled_y=CAMERA_DIAMETER/CAMERA_HEIGHT)
        self.pushBarX = 1.3
        
        self.debugPath = debugPath+"/picker" if debugPath is not None else None        
        if self.debugPath is not None:
            createDir(self.debugPath)
    
    
    def checkParticle(self, path=None):        
        path = captureImageFromCamera() if path is None else path
        # [{'class_id': 0, 'class_name': 'gold', 'confidence': 0.8966315984725952, 'box': [163.16069793701172, 222.29171752929688, 32.964737, 43.256775], 'scale': 0.65, 'scaled_box': [106, 144, 127, 173]}, {'class_id': 0, 'class_name': 'gold', 'confidence': 0.7585904002189636, 'box': [33.43605041503906, 320.60020446777344, 45.208633, 84.34854], 'scale': 0.65, 'scaled_box': [22, 208, 51, 263]}]
        detections, h, w = self.goldDetector.detectFromImagePath(path)
        print("detections", [d["scaled_box"] for d in detections])
        
        self.scaledMatrix.scaled(CAMERA_DIAMETER/w, CAMERA_DIAMETER/h)

        detections_scaled = conver_detections_to_x(detections, self.scaledMatrix)
        print("detections_scaled", detections_scaled)
        
        detections_scaled = sorted(detections_scaled, key=lambda x: x[2], reverse=True)
        print("detections_scaled sorted:", detections_scaled)
        
        if len(detections_scaled) == 0 :
            self.stepMotor.rotate(12, True)            
        else:        
            for detection in detections_scaled:
                targetCnt = self.cylinderMatrix.move(detection[2], self.pushBarX)
                for i in range(0, targetCnt):
                    self.stepMotor.rotateOnce(True)
                self.servoMotor.rotate(45, 0)
                self.servoMotor.rotate(0, 45)
        
        if self.debugPath is not None:
            import shutil            
            import json
            from datetime import datetime
            from pytz import timezone
            savePath = self.debugPath +"/"+ datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d_%H%M_%S")+"_"+str(len(detections))
            print("saving debug data... ", savePath)
            createDir(savePath)
            targetPath = join(savePath, "input.png")
            # shutil.copy(path, targetPath)
            origin_img = cv2.imread(path)
            cv2.imwrite(targetPath, cv2.cvtColor(origin_img,  cv2.COLOR_BGR2RGB))

            print("debug file will be saved on ",savePath)
            with open(join(savePath, "result.json"), "w") as outfile:
                json.dump(detections, outfile, cls=DecimalEncoder)   
                
            plot_cylinder(savePath+"/plot.png", [ d[2] for d in detections_scaled], [d[3] for d in detections_scaled])
            draw_bounding_box_with_detections(origin_img, detections)
            cv2.imwrite(savePath+"/detected.jpg", cv2.cvtColor(origin_img,  cv2.COLOR_BGR2RGB))
            
        
        return len(detections) > 0, detections_scaled