import numpy as np
from utils import deg2rad, rad2deg, normalize_angle_deg
from BackUp import BackUp
import random


# Calculate the  distance to a rock in front of the rover
def dist_to_rock(Rover):
# Find the indices of the rocks within 2.5 degrees of the center of the rover's view
    idx_in_front = np.where(np.abs(Rover.obs_angles) < deg2rad(2.5))[0]
# If there are no rocks within this range, return None
    if not len(idx_in_front):
        print("Dist to rock: N/A")
        return None
# Calculate the minimum distance to a rock in front of the rover
    min_dist = np.min(Rover.rock_dists[idx_in_front])
    print("Dist to rock: %.2f" % min_dist)
    return min_dist





# Calculate the steering angle for the rover
def update_steering(Rover):
    Rover.steer = calc_steering_angle(Rover)


# Update the throttle for the rover
def update_throttle(Rover):
# Set the target velocity and throttle based on the rover's objective
    if Rover.objective == 'mapping':
        target_velocity = Rover.max_vel
        throttle = Rover.throttle_set
    else:
        target_velocity = 0.5
        throttle = 0.1
# If the rover's velocity is below the target velocity, increase the throttle
    if Rover.vel < target_velocity:
        Rover.throttle = throttle
    else:
        Rover.throttle = 0


def stop_rover(Rover):
# Set the throttle, brake, steer, and mode to stop the rover
    Rover.throttle = 0
    Rover.brake = Rover.brake_set
    Rover.steer = 0
    Rover.mode = 'stop'


def turn_rover(Rover, rate=-15):
# Set the throttle and brake to 0 and set the steer to the specified rate
    Rover.throttle = 0
    Rover.brake = 0
    Rover.steer = rate # Could be more clever here about which way to turn


def decision_step(Rover):
# If the rover's home position has not been set, set it to the current position
    if Rover.home_pos is None:
        assert(Rover.pos is not None)
        Rover.home_pos = Rover.pos

# If the rover has been stuck for 100 iterations and is not currently backing up, push a BackUp state to the front of the queue
    if Rover.stuck_counter > 100 and not type(Rover.state_machine.current_state()) == type(BackUp) :
        Rover.state_machine.push_front(BackUp(Rover))
        Rover.stuck_counter = 0
# Run the rover's state machine
    Rover.state_machine.run()
 # If the throttle is greater than 0 and the velocity is below 0.2, increment the stuck counter. Otherwise, reset the stuck counter to 0
    if abs(Rover.throttle) > 0:
        if abs(Rover.vel) < 0.2:
            Rover.stuck_counter += 1
        else:
            Rover.stuck_counter = 0

    return Rover

