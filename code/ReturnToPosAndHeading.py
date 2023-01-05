from StateQueue import StateQueue
from math import atan2
import numpy as np
from TurnToHeading import TurnToHeading
from MoveDistance import MoveDistance
from Stop import Stop
from utils import distance, rad2deg

# A class for returning the rover to a specific position and heading
class ReturnToPosAndHeading(StateQueue):
    def __init__(self, rover, target_pos, target_heading):
        super().__init__(rover)
# Save the target position and heading
        self.target_pos = np.array(list(target_pos))
        self.target_heading = target_heading
# Mark this run as first run
        self.is_first_run = True


    def run(self):
        if self.is_first_run:
# Calculate the heading to the target position
            diff = self.target_pos - np.array(self.rover.pos)
            heading_to_target = rad2deg(atan2(diff[1], diff[0])) + 180
# Calculate the distance to the target position
            distance_to_target = distance(self.target_pos, self.rover.pos)
# Add a Stop state to the queue
            self.add(Stop(self.rover))
# Add a TurnToHeading state to the queue
            self.add(TurnToHeading(self.rover, heading_to_target))
# Add a MoveDistance state to the queue
            self.add(MoveDistance(self.rover, distance_to_target - 0.5, target_vel=-1))
# Add a TurnToHeading state to the queue
            self.add(TurnToHeading(self.rover, self.target_heading))
# Mark first run as flase
            self.is_first_run = False
        else:
            super().run()

