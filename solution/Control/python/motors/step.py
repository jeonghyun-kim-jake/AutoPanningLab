import RPi.GPIO as GPIO
import threading                                                                
from collections import deque


class StepMotor28BYJ:
    def __init__(self, aint=3, bint=5, aint2=7, bint2=8):        
        self.aint = aint    
        self.bint = bint    
        self.aint2 = aint2    
        self.bint2 = bint2
        self.sig= deque([1,0,0,0])
        self.lock = threading.RLock()
        
    def init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.aint,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.bint,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.aint2,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.bint2,GPIO.OUT,initial=GPIO.LOW)
        
    def rotate(self, direction=True):
        with self.lock:
            sig = self.sig
            GPIO.output(self.aint,sig[0])
            GPIO.output(self.bint,sig[1])
            GPIO.output(self.aint2,sig[2])
            GPIO.output(self.bint2,sig[3])
            sig.rotate(1 if direction else -1)

            
    def deinit(self):
        GPIO.cleanup()
        
   