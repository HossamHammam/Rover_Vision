class Stop:

    # A class for representing a state or action in which the Mars rover stops moving.

    def __init__(self, rover, brake=1.0):

        #Initialize a Stop object.

        self.rover = rover
        self.brake = brake

    def run(self):
        # Run the stop action. This sets the rover's brake, throttle, and steer values
        # to 0.0.

        self.rover.brake = self.brake
        self.rover.throttle = 0.0
        self.rover.steer = 0.0

    def next(self):
        # Determine the next action based on the rover's velocity. If the rover's
        # velocity is less than 0.2, then the stop action is complete and `None` is
        # returned. Otherwise, the stop action is still in progress and `self` is
        # returned.
        
        if abs(self.rover.vel) < 0.2:
            return None
        else:
            return self
