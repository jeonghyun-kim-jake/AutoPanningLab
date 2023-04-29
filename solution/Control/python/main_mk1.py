# engine
from motors.step import StepMotor28BYJ
from motors.servo import ServoMotorSG90

from visions import checkParticle
from mk1_picker import ParticlePicker
from mk1_supplier import ParticleSupplier

# hw configure
from typing import Final
SINGLE_STEP: Final = 120

#### 1. particle supplier
stepMotor1 = StepMotor28BYJ(aint=11, bint=13, aint2=15, bint2=16)
supplier = ParticleSupplier(stepMotor1)


#### 2. particle picker
stepMotor2 = StepMotor28BYJ(aint=3, bint=5, aint2=7, bint2=8)
stepMotor2.init()
servoMotor = ServoMotorSG90(servo_pin=12)
picker = ParticlePicker(stepMotor2, stepMotor2)

# testcode
import time
import argparse
parser = argparse.ArgumentParser(description='Execute mk1')
parser.add_argument('--max', type=int, 
                    default=-1,
                    help='Max trial for testing')

args = parser.parse_args()

print("args: ", args)

loop_checker = lambda x : True
if args.max >= 0 :
    loop_checker = lambda x : x < args.max


cntTrial = 0    
try:
    while loop_checker(cntTrial):
        try:
            if not picker.checkParticle():
                print("Not Found, pass it! ")
                supplier.supply();
                
            time.sleep(0.01) # 10ms
        except Exception as e:
            print("Error with ", e)

        cntTrial+=1
except KeyboardInterrupt:
    pass
finally:
    print("DONE: ", cntTrial)    
    import RPi.GPIO as GPIO
    GPIO.cleanup()
##