import RPi.GPIO as GPIO
import threading

class ServoMotorSG90:
    def __init__(self, servo_pin=12):        
        self.servo_pin = servo_pin    
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.lock = threading.RLock()
        self.pwm = GPIO.PWM(self.servo_pin, 50) # 50Hz( 서보모터 PWM 동작을 위한 주파수 )
        self.pwm.start(0)
       
        
    def rotate(self, degree):
        with self.lock:
            sig = max(0, min(180, degree))
            duty = ( 12.5 * ( sig / 180 ))
            self.pwm.ChangeDutyCycle (duty) 
            
            
    def deinit(self):
        GPIO.cleanup()
        