from StateQueue import StateQueue
import numpy as np
from utils import *
from TurnToBearing import TurnToBearing


class TurnToFreeBearing(StateQueue):
    def __init__(self,rover):
        # Initialize the `TurnToFreeBearing` object.
        super().__init__(rover)
        self.is_first_run = True


    def run(self):
        # Turn the rover towards the nearest free bearing.
        if self.is_first_run:
            self.is_first_run = False
            bearing = rad2deg(np.mean(self.rover.nav_angles))
            self.add(TurnToBearing(self.rover, bearing))
        else:
            super().run()

