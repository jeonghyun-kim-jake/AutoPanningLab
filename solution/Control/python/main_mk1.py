# engine
from motors.step import StepMotor28BYJ
from motors.servo import ServoMotorSG90
from visions import checkParticle

# hw configure

from typing import Final
SINGLE_STEP: Final = 120


stepMotor = StepMotor28BYJ()
stepMotor.init()

servoMotor = ServoMotorSG90()
angle = [0, 20, 45, 65, 90, 110, 130, 150, 180]


def moveBelt(moveDistance, direction=True):
    print("moveBelt ", moveDistance)
    for k in range(0, moveDistance):
        stepMotor.rotate(direction)
        time.sleep(0.01)
    
def pickup(location):
    print("pickup ", location)   
    servoMotor.rotate( angle[location%9] )
    time.sleep(0.02)
    print("pickup done")


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
 
try:
    cntTrial = 0    
    while loop_checker(cntTrial):
        try:
            isFound, location = checkParticle()
            if isFound or cntTrial % 10 == 0 :
                print("Found, pick up it! ", location)
                # TODO: location -> check move belt half step or not.
                pickup(location)
                moveBelt(location)
            else:
                print("Not Found, pass it! ", location)
                moveBelt(SINGLE_STEP)
            time.sleep(0.002) # 2ms
        except Exception as e:
            print("Error with ", e)

        cntTrial+=1
finally:
    stepMotor.deinit()    

print("DONE: ", cntTrial)
##