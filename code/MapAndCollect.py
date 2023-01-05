import numpy as np
from utils import *
from StopAndTurn import StopAndTurn
#from perception import is_obstacle_ahead, is_overhanging_rock_ahead
from FindAndPickupRock import FindAndPickupRock
from SurveySpin import SurveySpin
from AvoidOverhangingRock import AvoidOverhangingRock
from utils import *


class MoveForward(object):
    def __init__(self, rover):
        self.rover = rover
        # desired velocity to maintain while driving forward which in this case 2.0
        self.target_vel = 2.0
        #constant throttle to use while accelerating
        self.throttle = 0.2
        # position of rover at last survey
        self.last_survey_pos = [1e9, 1e9]
        # parameter for steering smoothing
        self.a = 0.95


    def run(self):
        #ensure brake is not applied
        self.rover.brake = 0
        # update the throttle value
        self.update_throttle()
        # update the steering value
        self.update_steer()


    def num_samples_found(self):
        # returns number of rocks that have been collected
        return len(np.array(self.rover.samples_found).nonzero()[0])


    def next(self):
# if there is an obstacle ahead, stop and turn
        if is_obstacle_ahead(self.rover):
            return StopAndTurn(self.rover)
# if a rock is nearby, go collect it
        elif self.is_rock_near():
            return FindAndPickupRock(self.rover)
# if all rocks have been collected, return home
        elif self.num_samples_found() == 6:
            print("RETURN HOME!")
            return None
# otherwise, continue driving forward
        else:
            return self


    def update_throttle(self):
# if the rover is not at the target velocity, apply throttle to accelerate
        if self.rover.vel < self.target_vel:
            self.rover.throttle = self.throttle
# otherwise, maintain constant velocity by not applying throttle
        else:
            self.rover.throttle = 0


    def update_steer(self):
# Find the maximum steering angle for navigation points within 30 meters and 10 meters of the rover
        idx_nav_near = np.where((self.rover.nav_dists < 30) & (self.rover.nav_dists > 10))[0]
        if not idx_nav_near.size:
            max_nav_angle = 90
        else:
            max_nav_angle = np.max(self.rover.nav_angles[idx_nav_near] * 180/np.pi)
# Find the minimum steering angle for obstacles within 20 meters of the rover
        idx_obs_near = np.where((self.rover.obs_dists < 20) & (self.rover.obs_dists > 0) & (self.rover.obs_angles > 0))[0]
        if not idx_obs_near.size:
# Set min_obs_angle to 90 degrees
            min_obs_angle = 90
        else:
# Find minimum angle to nearby obstacles (in degrees)
            min_obs_angle = np.min(self.rover.obs_angles[idx_obs_near] * 180/np.pi)


# Calculate new steering angle as minimum of max_nav_angle - 25 and min_obs_angle - 35
        new_steer = np.clip(min(max_nav_angle - 25,min_obs_angle - 35), -15, 15)
# Update steering angle using exponential moving average formula
        self.rover.steer = self.a * new_steer + (1-self.a) * self.rover.steer


    def is_rock_near(self):
# Return True if rock_angles has size greater than 0, False otherwise
        return self.rover.rock_angles.size > 0
