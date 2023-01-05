#from perception import bearing_to_rock_deg
from utils import *
from StateQueue import StateQueue
from Stop import Stop
from TurnToHeading import TurnToHeading
from ApproachRock import ApproachRock
from PickupRock import PickupRock
from ReturnToPosAndHeading import ReturnToPosAndHeading
from TurnToBearing import TurnToBearing
from utils import *
class FindAndPickupRock(StateQueue):
    def __init__(self, rover):
        super().__init__(rover)
        # Get the direction of the rock in degrees
        bearing = bearing_to_rock_deg(self.rover)
        # Stop the rover
        self.add(Stop(self.rover))
        # Turn the rover to face the direction of the rock
        self.add(TurnToBearing(self.rover, bearing))
        # Approach the rock
        self.add(ApproachRock(self.rover))
        # Stop the rover again
        self.add(Stop(self.rover))
        # Pick up the rock
        # Check if the rock was on the left side of the rover
        self.add(PickupRock(self.rover))
        if bearing < -5:
        # If so, return the rover to its original position and heading
            self.add(ReturnToPosAndHeading(self.rover, self.rover.pos, self.rover.yaw))
        else:
         # Otherwise, just set the rover's heading to its original heading
            self.add(TurnToHeading(self.rover,self.rover.yaw))
