class StateMachine:

    # A class for managing the state of a Mars rover in a simulation.
    # 
    # Parameters:
    # rover (object): An object representing the Mars rover.
    # *args: Objects representing the states or actions of the rover.


    def __init__(self, rover, *args):
        # Initialize a StateMachine object.
        # 
        # Parameters:
        # rover (object): An object representing the Mars rover.
        # *args: Objects representing the states or actions of the rover.
        self.rover = rover
        self.state_stack = list(args)

    def current_state(self):

        # Get the current state or action of the rover.
        # Returns:
        # object: The current state or action of the rover.

        return self.state_stack[0]

    def run(self):

        # Run the current state or action of the rover, and update the state stack
        # based on the result.

        if len(self.state_stack) == 0:
            print("DONE!!!")
            return

        print(self.current_state())

        self.current_state().run()

        next_state = self.current_state().next()

        if next_state is self.current_state():
            pass
        elif next_state is None:
            self.state_stack.pop(0)
        else:
            self.state_stack.insert(0, next_state)

    def push_front(self, action):
        # Add a new state or action to the front of the state stack.
        self.state_stack.insert(0, action)

