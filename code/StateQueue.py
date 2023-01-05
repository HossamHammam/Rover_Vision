class StateQueue:

    # A class for managing a queue of states or actions for a Mars rover in a simulation.


    def __init__(self, rover):

        # Initialize a StateQueue object.

        self.rover = rover
        self.queue = []

    def add(self, action):

        # Add a new state or action to the end of the queue.

        self.queue.append(action)

    def run(self):

        # Run the current state or action at the front of the queue.

        print(self.current_task())
        self.current_task().run()

    def current_task(self):

        # Get the current state or action at the front of the queue.
        #
        # Returns:
        # object: The current state or action, or None if the queue is empty.

        return self.queue[0] if len(self.queue) else None

    def next(self):

        # Update the queue based on the result of the current state or action.
        next_task = self.current_task().next()

        if next_task is None:
            self.queue.pop(0)
        elif next_task is not self.current_task():
            self.queue.insert(0, next_task)

        if self.current_task():
            return self
        else:
            return None