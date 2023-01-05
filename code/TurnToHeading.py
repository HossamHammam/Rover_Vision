import numpy as np
from utils import *

class TurnToHeading(object):
    def __init__(self, rover, heading):
        self.rover = rover
        self.heading = heading


    def heading_error(self):
        # Calculate the difference in the current heading and the desired heading.
        # This function normalizes the angle to a range between -180 and 180 degrees.

        return normalize_angle_deg(self.heading - self.rover.yaw)


    def run(self):
        # Turn the rover towards the desired heading.
        #
        # This function sets the throttle to 0 and the brake to 1 if the rover's velocity
        # is above a certain threshold. Otherwise, it sets the brake to 0 and adjusts the
        # steering angle based on the heading error.

        self.rover.throttle = 0
        if abs(self.rover.vel) > 0.2:
            self.rover.brake = 1
        else:
            d_theta = self.heading_error()
            abs_rate = min(15, max(1, abs(d_theta) / 4))
            sign_rate = np.sign(d_theta)
            self.rover.brake = 0
            self.rover.steer = abs_rate * sign_rate


    def is_heading_reached(self):
        # Check if the rover has reached the desired heading.
        return abs(self.heading_error()) < 1


    def next(self):
        # Transition to the next state.
        #
        # If the rover has reached the desired heading, this function sets the steering angle to 0
        # and returns None to indicate that this state is complete. Otherwise, it returns itself to
        # continue executing this state.

        if self.is_heading_reached():
            self.rover.steer = 0
            return None
        else:
            return self