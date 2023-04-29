



class ParticleSupplier:
    def __init__(self, stepMotor):
        self.stepMotor = stepMotor
        print("ParticleSupplier::created")
    
    def supply(self):
        print("ParticleSupplier::supply")