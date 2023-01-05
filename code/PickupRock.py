class PickupRock(object):
    def __init__(self, rover):
        self.rover = rover
        self.did_issue_command = False


    def run(self):
     # If the pickup command has not yet been issued, issue it
        if not self.did_issue_command:
            self.rover.pick_up = True
            self.did_issue_command = True


    def next(self):
# If the rover is near a sample, return self to indicate that this Process should continue
        if self.rover.near_sample:
            return self
# If the rover is not near a sample, return None to indicate that this Process is finished
        else:
            return None
