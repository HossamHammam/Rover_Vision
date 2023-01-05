from utils import *
from PickupRock import *
#from perception import obstacle_bearing, distance_to_rock, distance_to_obstacle, bearing_to_rock
from ApproachRockDetour import ApproachRockDetour

#This is the constructor for the ApproachRock class. It initializes the rover attribute to the given rover argument, and sets the target_vel and throttle attributes to 0.5 and 0.2, respectively. It also sets the mode attribute to "first approach" and initializes the distance_to_rock attribute by calling the distance_to_rock function and dividing the result by 10.
class ApproachRock(object):
    def __init__(self, rover):
        self.rover = rover
        self.target_vel = 0.5
        self.throttle = 0.2
        self.mode = "first approach"
        self.distance_to_rock = distance_to_rock(rover) / 10.0

#This method is called repeatedly, and is responsible for updating the steering and throttle of the rover so that it moves towards the rock. It sets the self.rover.brake attribute to 0 and calls the update_steering_approach_rock and update_throttle methods to update the steering and throttle, respectively. It also prints the distance to the rock.
    def run(self):
        self.rover.brake = 0
        self.update_steering_approach_rock()
        self.update_throttle()
        print("distance to rock: ", distance_to_rock(self.rover))

#This method returns the next state for the rover to transition to. If the rover is close to a sample, it will return None, indicating that no further action is necessary. If the mode is "first approach" and the bearing to the rock is greater than -5, the rover will transition to the ApproachRockDetour state. If neither of these conditions are met, the rover will continue to remain in the ApproachRock state.
    def next(self):
        if self.rover.near_sample:
            return None
        elif self.mode == "first approach" and bearing_to_rock(self.rover) > -5:#and self.is_rock_near_obstacle():
            self.mode = "final approach"
            return ApproachRockDetour(self.rover, self.distance_to_rock)
        else:
            return self

#This method returns True if the distance to the rock is within 0.5 meters of the distance to an obstacle, and False otherwise.
    def is_rock_near_obstacle(self):
        return abs(distance_to_rock(self.rover) - distance_to_obstacle(self.rover)) < 0.5


#This method updates the steering of the rover so that it moves towards the rock. It calculates the bearing to the rock by taking the mean of the rock angles (which are the angles at which the rock is seen by the rover's cameras). If no rocks are seen, the bearing is set to 0. The obs_bearing variable is the bearing to an obstacle, which is calculated using the obstacle_bearing function. The obs_offset variable is set to 30. If the bearing is greater than 0, the steer_angle variable is set to the minimum of the bearing and obs_bearing minus obs_offset. If the bearing is less than or equal to 0, the steer_angle variable is set to the maximum of the bearing and obs_bearing plus obs_offset. The self.rover.steer attribute is then set to the steer_angle variable.
    def update_steering_approach_rock(self):
        if self.rover.rock_angles.size == 0:
            bearing = 0.0
        else:
            bearing = rad2deg(np.mean(self.rover.rock_angles))

        if False:
            obs_bearing = obstacle_bearing(self.rover, bearing)

            obs_offset = 30

            if bearing > 0:
                steer_angle = min(bearing, obs_bearing - obs_offset)
            else:
                steer_angle = max(bearing, obs_bearing + obs_offset)
            print("obs_bearing: ",  obs_bearing)

        self.rover.steer = bearing
        print("self.rover.steer: ", self.rover.steer)

# This method updates the throttle of the rover so that it maintains a target velocity of self.target_vel. If the current velocity of the rover is below self.target_vel, the self.rover.throttle attribute is set to self.throttle. If the current velocity is greater than or equal to self.target_vel, the self.rover.throttle attribute is set to 0.
    def update_throttle(self):
        if self.rover.vel < self.target_vel:
            self.rover.throttle = self.throttle
        else:
            self.rover.throttle = 0
