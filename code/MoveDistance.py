from utils import distance
from Stop import Stop
import numpy as np

class MoveDistance(object):
    def __init__(self, rover, dist, target_vel=2):
        self.rover = rover
        self.dist = dist
        self.target_vel = target_vel
        self.throttle = 0.2 * np.sign(target_vel)
        # Whether the rover has reached the target distance
        self.is_done = False
        # Whether this is the first time run() has been called
        self.is_first_run = True
        # Counter to keep track of how long the rover has not moved
        self.not_moved_counter = 0


    def run(self):
     # Increment not_moved_counter if the rover is not moving
        if abs(self.rover.vel) < 0.2:
            self.not_moved_counter += 1
        else:
            self.not_moved_counter = 0


        self.rover.steer = 0
         #If this is the first time run() is called, store the rover's initial position
        if self.is_first_run:
            self.start_pos = self.rover.pos
            self.is_first_run = False

 # Check if the rover has reached the target distance
        if not self.is_done and distance(self.rover.pos, self.start_pos) >= self.dist:
            self.is_done = True

# If the rover has reached the target distance, set brake to 1 and throttle to 0
        if self.is_done:
            self.rover.brake = 1
            self.rover.throttle = 0
# If the rover's velocity is below the target velocity, set brake to 0 and throttle to the specified value
        elif abs(self.rover.vel) < abs(self.target_vel):
            self.rover.brake = 0
            self.rover.throttle = self.throttle
# If the rover's velocity is equal to or above the target velocity, set throttle to 0
        else:
            self.rover.throttle = 0


    def next(self):
# If the rover has reached the target distance and is not moving, return None to indicate that this behavior is finished
        if self.is_done and abs(self.rover.vel) < 0.2:
            return None
# If the rover has not reached the target distance, but is not moving and the throttle is not 0, return None
# (This indicates that the rover is stuck and cannot move)
        elif not self.is_done and abs(self.rover.vel) < 0.2 and abs(self.rover.throttle) > 0 and self.not_moved_counter > 80:
            return None
        else:
            return self
