#from perception import is_obstacle_ahead
from utils import *
from StopAndTurn import StopAndTurn
from TurnToHeading import TurnToHeading
from StateQueue import StateQueue
from TurnToFreeBearing import TurnToFreeBearing
from utils import *

class ReturnHome(object):
    def __init__(self, rover):
        self.rover = rover

# Return the distance from the rover's current position to its home position
    def distance_to_target(self):
        return distance(self.rover.pos, self.rover.home_pos)

 # Calculate the target velocity based on the distance to the home position
    def target_velocity(self):
        d = self.distance_to_target()
        # If the distance is greater than 10 meters, return 3 m/s
        if d > 10.0:
            return 3.0
        # Otherwise, return 1 m/s
        else:
            return 1.0

# Calculate the throttle value based on the distance to the home position
    def throttle(self):
# If the distance is greater than 10 meters, return 0.4
        if self.distance_to_target() > 10.0:
            return 0.4
# Otherwise, return 0.2
        else:
            return 0.2


    def run(self):
        print("target heading:", self.target_heading())
        print("target bearing:", self.target_bearing())
# update rover throttle and steering
        self.update_throttle()
        self.update_steering()


    def next(self):
# if there is an obstacle ahead, go to StopAndTurn state
        if is_obstacle_ahead(self.rover):
            return StopAndTurn(self.rover)
# if target bearing is more than 180 - 45 degrees from current heading, go to StateQueue which will execute TurnToHeading and TurnToFreeBearing states
        elif abs(self.target_bearing()) > 180 - 45:
            sq = StateQueue(self.rover)
            sq.add(TurnToHeading(self.rover, self.target_heading()))
            sq.add(TurnToFreeBearing(self.rover))
            return sq
# if distance to target is less than 0.25 meters, set brake to 1 and throttle to zero and return None to stop the rover
        elif self.distance_to_target() < 0.25:
            self.rover.brake = 1
            self.rover.throttle = 0
            return None
# if none of the above conditions are met, stay in the current state
        else:
            return self

# calculate heading in degrees to home position from current position
    def target_heading(self):
        return heading_to_pos_deg(self.rover.pos, self.rover.home_pos)

# calculate bearing in degrees to home position from current heading
    def target_bearing(self):
        return normalize_angle_deg(self.target_heading() - self.rover.yaw)


    def update_steering(self):
    # Find minimum and maximum steering angles that the rover can take 
    
        min_nav_angle = rad2deg(np.min(self.rover.nav_angles)) + 45
        max_nav_angle = rad2deg(np.max(self.rover.nav_angles)) - 45
# Find the maximum steering angle the rover can take based on the presence of obstacles on the right side of the rover
        idx_obs_max = np.where((self.rover.obs_dists < 20) & (self.rover.obs_dists > 0) & (self.rover.obs_angles > 0))[
            0]
        if not idx_obs_max.size:
# If no obstacles are present on the right side, set the maximum steering angle to 90 degree
            max_obs_angle = 90
        else:
# If obstacles are present on the right side, set the maximum steering angle to the minimum angle of the obstacles
            max_obs_angle = np.min(self.rover.obs_angles[idx_obs_max] * 180 / np.pi)

# Find the minimum steering angle the rover can take based on the presence of obstacles on the left side of the rover
        idx_obs_min = np.where((self.rover.obs_dists < 20) & (self.rover.obs_dists > 0) & (self.rover.obs_angles < 0))[
            0]
# If no obstacles are present on the left side, set the minimum steering angle to -90 degrees
        if not idx_obs_min.size:
            min_obs_angle = -90
        else:
#set the minimum angle to the maximum angle of the obstacles
            min_obs_angle = np.max(self.rover.obs_angles[idx_obs_min] * 180 / np.pi)

 # Set the minimum steering angle to the maximum of the minimum navigable angle and the minimum obstacle angle
        min_angle = max(min_nav_angle, min_obs_angle)
 # Set the maximum steering angle to the minimum of the maximum navigable angle and the maximum obstacle angle
        max_angle = min(max_nav_angle, max_obs_angle)
# Set the rover's steering angle to the target bearing, but limited to the min and max angles
        self.rover.steer = np.clip(self.target_bearing(), min_angle, max_angle)


    def update_throttle(self):
# If the rover's velocity is less than the target velocity, set the throttle to the throttle value
        if self.rover.vel < self.target_velocity():
            self.rover.throttle = self.throttle()
        # Otherwise, set the throttle to 0
        else:
            self.rover.throttle = 0


