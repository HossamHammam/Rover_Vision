from perception import is_rock_near, bearing_to_rock
from utils import *
import numpy as np


class TurnToRock(object):
    def __init__(self, rover):
        self.rover = rover
        # Default bearing to turn to when no rock is detected
        self.default_bearing = 90


    def target_bearing(self):
        # If a rock is within detection range
        if is_rock_near(self.rover):
            # Calculate the bearing to the rock
            bearing = rad2deg(bearing_to_rock(self.rover))
            # Set the default bearing to 90 degrees in the direction of the rock
            self.default_bearing = 90 * np.sign(bearing)
            return bearing
        else:
            return self.default_bearing

    # Adjusts the rover's steering angle and velocity to turn towards the target bearing

    def run(self):
        # If the rover is moving too fast, apply the brakes
        if abs(self.rover.vel) > 0.2:
            self.rover.brake = 1
        # If the rover is moving slowly enough, adjust the steering angle to turn towards the target bearing
        else:
            self.rover.brake = 0
            # Calculate the minimum and maximum steering angles to turn towards the target bearing
            print("target bearing: ", self.target_bearing())
            bearing = self.target_bearing()
            min_steer = 1 * np.sign(bearing)
            max_steer = 5 * np.sign(bearing)
            min_steer, max_steer = min(min_steer, max_steer), max(min_steer, max_steer)
            self.rover.steer = np.clip(self.target_bearing() // 4, min_steer, max_steer)


    # Returns `None` if the rover has turned within 2.5 degrees of the target bearing, else returns `self`
    def next(self):
        if abs(self.target_bearing()) < 2.5:
            self.rover.steer = 0
            return None
        else:
            return self