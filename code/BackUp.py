from Rotate import Rotate
import numpy as np
from utils import *

class BackUp(object):
    def __init__(self, rover):
        self.rover = rover
        self.did_move = False
        self.step_count = 0
        self.mode = ""
        self.did_move_step_count = 0
        self.is_done = False
        self.start_pos = np.array(rover.pos)

# Calculate the distance between the current position and the starting position
    def distance_moved(self):
        return distance(self.rover.pos, self.start_pos)


    def run(self):
        if self.is_done:
            return
# Reverse direction if rover hasn't moved after 40 steps
        if not self.did_move and self.step_count > 40:
            self.rover.throttle *= -1

# Set did_move to True if rover has moved a distance of 0.5 meters or more
        if not self.did_move and self.distance_moved() > 0.5:
            self.did_move = True

# If the rover is tilted more than 5 degrees, set the mode to "twist"
# and start turning the rover to the left
        if abs(self.rover.roll) > 5:
            self.mode = "twist"
            self.rover.throttle = 0
            self.rover.steer = -15
# If the rover has moved a distance of 0.25 meters or more, keep turning to the left
        elif self.distance_moved() > 0.25:
            self.rover.steer = -15
# If the rover hasn't moved yet, steer to the right and reverse
        elif not self.did_move:
            self.rover.brake = 0
            self.rover.steer = 15
            self.rover.throttle = -1.0
            self.step_count +=1


    def next(self):
# If the behavior is done, reset the throttle and steering and return None
        if self.is_done:
            self.rover.throttle = 0
            self.rover.steer = 0
            return None
# If the rover has moved a distance of 0.5 meters or more,
# set the brake to 1 and return a Rotate state to rotate the rover to the left by 22.5 degrees
        elif self.did_move and self.distance_moved() > 0.5:
            self.rover.throttle = 0
            self.rover.brake = 1
            self.is_done = True
            return Rotate(self.rover, -22.5, fast=True)
# If the mode is "twist" and the rover is tilted less than 2.5 degrees,
# reset the throttle and steering, set is_done to True, and return a Rotate state to the left by 22.5 degrees
        elif self.mode == 'twist' and abs(self.rover.roll) < 2.5:
            self.rover.steer = 0
            self.rover.throttle = 0
            self.is_done = True
            return Rotate(self.rover, -22.5, fast=True)


        else:
            return self
