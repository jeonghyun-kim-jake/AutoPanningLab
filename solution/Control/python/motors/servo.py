import RPi.GPIO as GPIO
import threading
import time

def validateAngle(angle, max_angle=180):
    angle = max(0, min(max_angle, angle))
    return angle

class ServoMotorSG90:
    def __init__(self, servo_pin=12, freq=50, dc_min=2.5, dc_max=12.5):        
        self.servo_pin = servo_pin    
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_pin, GPIO.OUT)
        # Define frequency and duty cycle ranges for PWM
        self.freq = freq;
        self.dc_min = dc_min
        self.dc_max = dc_max
        self.lock = threading.RLock()
        self.pwm = GPIO.PWM(self.servo_pin, 50) # 50Hz( 서보모터 PWM 동작을 위한 주파수 )
        self.pwm.start(0)
    
    def rotate(self, angle_to, angle_from=0):        
        angle_to = validateAngle(angle_to)
        angle_from = validateAngle(angle_from)
        for angle in range(angle_from, angle_to, -1 if angle_to < angle_from else 1 ):
            self.rotateOnce(angle)
        
    def rotateOnce(self, angle):
        with self.lock:
            angle = validateAngle(angle)
            duty = (angle / 180.0) * (self.dc_max - self.dc_min) + self.dc_min     
            self.pwm.ChangeDutyCycle (duty) 
            time.sleep(0.02)