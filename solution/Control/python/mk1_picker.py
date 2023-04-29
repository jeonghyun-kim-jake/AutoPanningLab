

class ParticlePicker:
    def __init__(self, stepMotor, servoMotor):
        # move cylinder
        self.stepMotor = stepMotor
        # push particle
        self.servoMotor = servoMotor
    
    
    def checkParticle(self):
        return False