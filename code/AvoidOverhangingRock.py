from StateQueue import StateQueue
from MoveDistance import MoveDistance
from TurnToBearing import TurnToBearing
from TurnToHeading import TurnToHeading
from Rotate import Rotate


class AvoidOverhangingRock(StateQueue):
    def __init__(self, rover):
        super().__init__(rover)
        # Add states to the queue:
        # - Move a distance of 1 meter in reverse
        self.heading = self.rover.yaw
        self.add(MoveDistance(rover, 1, -1))
        # - Rotate 45 degrees to the left
        self.add(Rotate(rover, -45, fast=True))
        # - Move a distance of 2 meters forwards
        self.add(MoveDistance(rover, 2, 1))
        # - Turn to the original heading
        self.add(TurnToHeading(rover, self.heading))
