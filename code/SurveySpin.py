from StateQueue import StateQueue
from Stop import Stop
from Rotate import Rotate

class SurveySpin(StateQueue):
    # A class for representing a state or action in which the Mars rover stops and
    # rotates in place to survey its surroundings. This class is a subclass of
    # `StateQueue` and consists of a `Stop` action followed by a `Rotate` action.
    def __init__(self, rover):
        
        super().__init__(rover)
        self.add(Stop(rover, 0.2))
        self.add(Rotate(rover, 360))