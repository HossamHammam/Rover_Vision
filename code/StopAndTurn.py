from perception import is_obstacle_ahead
from Rotate import Rotate
from utils import *
class StopAndTurn(object):
    # A class for representing a state or action in which the Mars rover stops and
    # turns in place.
    def __init__(self, rover):
        self.rover = rover
        self.is_clear = False

    def run(self):
        # Run the stop and turn action. If the rover's velocity is greater than 0.2,
        # then the rover is stopped. Otherwise, the rover's brake is set to 0 and the
        # rover's steer is set to -15.
        if self.rover.vel > 0.2:
            self.rover.stop()
        else:
            self.rover.brake = 0
            self.rover.steer = -15


    def next(self):
        # Determine the next action based on whether there is an obstacle ahead of the
        # rover. If there is no obstacle, then the rover rotates in place. If there
        # is an obstacle, then this action is repeated. If the rover has completed
        # its rotation, then `None` is returned to indicate that this action is
        # complete.
        if not is_obstacle_ahead(self.rover):
            if not self.is_clear:
                self.is_clear = True
                return Rotate(self.rover, -360/9.5, fast=True)
            else:
                self.rover.steer = 0
                return None
        else:
            return self