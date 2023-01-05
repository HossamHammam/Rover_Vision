import numpy as np
from utils import *

class TurnToBearing(object):
    # A class for representing a state or action in which the Mars rover turns to a
    # specified bearing.
    #
    # Attributes:
    # rover (object): An object representing the Mars rover.
    # bearing (float): The desired bearing for the rover to turn towards.
    # heading (float): The target heading for the rover.
    # is_first_run (bool): A flag indicating whether this is the first time the
    # `run` method has been called.

    def __init__(self, rover, bearing):
        self.rover = rover
        self.bearing = bearing
        self.heading = 0
        self.is_first_run = True


    def heading_error(self):
        # Calculate the error in the rover's heading.
        return normalize_angle_deg(self.heading - self.rover.yaw)


    def run(self):

        # Run the turn to bearing action. If this is the first time the method has
        # been called, then the target heading is set based on the rover's current
        # heading and the desired bearing. If the rover's velocity is greater than
        # 0.2, then the rover's brake is set to 1. Otherwise, the rover's brake is
        # set to 0 and the rover's steer is set based on the error in the rover's
        # heading.

        self.rover.throttle = 0

        if self.is_first_run:
            self.heading = self.rover.yaw + self.bearing
            self.is_first_run = False

        if abs(self.rover.vel) > 0.2:
            self.rover.brake = 1

        else:
            d_theta = self.heading_error()
            abs_rate = min(15, max(1, abs(d_theta) / 4))
            sign_rate = np.sign(d_theta)
            self.rover.brake = 0
            self.rover.steer = abs_rate * sign_rate


    def is_heading_reached(self):
        # Check if the rover has reached its target heading.
        return abs(self.heading_error()) < 1

    def next(self):
        # Check if the rover has reached its target heading. If it has, then the
        # rover's steer is set to 0 and the function returns None. Otherwise, the
        # function returns self.
        if self.is_heading_reached():
            self.rover.steer = 0
            return None
        else:
            return self