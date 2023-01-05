import numpy as np
from utils import normalize_angle_deg

class Rotate(object):
    def __init__(self, rover, angle, fast=False):
# Save the rover, angle to rotate to, and a flag indicating whether the rotation should be fast
        self.rover = rover
        self.start_heading = self.rover.yaw
        self.end_heading = self.start_heading + angle
        self.total_angle = 0
        self.last_heading = self.rover.yaw
        self.half_heading = self.rover.yaw * 0.5 * angle
        self.angle = angle
        self.did_reach_half_angle = False
        self.fast = fast

    def run(self):
# Set the throttle and brake to 0
        self.rover.throttle = 0
        if abs(self.rover.vel) > 0.2:
            self.rover.brake = 1
        else:
            self.rover.brake = 0
# Calculate the change in angle since the last run
            diff_angle = normalize_angle_deg(self.rover.yaw - self.last_heading)
            self.total_angle += diff_angle
            self.last_heading = self.rover.yaw
# Set the steering angle based on the desired angle and the current angle
            if self.fast:
                self.rover.steer = np.sign(self.angle) * 15
            else:
                self.rover.steer =  np.clip((self.angle - self.total_angle) / 4, 1, 15)




    def next(self):
# If the total angle rotated is greater than or equal to the desired angle, return None
        if abs(self.total_angle) >= abs(self.angle):
            self.rover.steer = 0
            return None
        else:
            return self
