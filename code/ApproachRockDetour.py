from StateQueue import StateQueue
from MoveDistance import MoveDistance
from TurnToBearing import TurnToBearing
from TurnToRock import TurnToRock
#from perception import distance_to_rock
from utils import *
import math
from utils import *


class ApproachRockDetour(StateQueue):
    def __init__(self, rover, distance_to_rock):
        super().__init__(rover)
         # Turn to a bearing of -20 degrees
        phi = -20
        self.add(TurnToBearing(self.rover, phi))
          # Move a distance of 1.5 meters
        self.add(MoveDistance(self.rover, 1.5))
        # Turn towards the rock
        self.add(TurnToRock(self.rover))
