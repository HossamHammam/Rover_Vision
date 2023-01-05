class PID(object):
    def __init__(self, Kp, Kd, Ki):
    # Initialize instance variables
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.target_value = 0.0
        self.current_value = 0.0
        self.p_error = 0.0
        self.last_p_error = 0.0
        self.d_error = 0
        self.i_error = 0


    def update(self, current_value):
    # Update current_value and calculate errors
        self.current_value = current_value
        self.p_error = self.target_value - current_value
        self.d_error = self.p_error - self.last_p_error
        self.i_error += self.p_error
        self.last_p_error = self.d_error
# Calculate and return the control output based on the PID equation
        return self.Kp * self.p_error + self.Kd * self.d_error + self.Ki * self.i_error

# Set the target value to target and reset the error
    def set_target(self, target):
        self.target = target;
        self.d_error

