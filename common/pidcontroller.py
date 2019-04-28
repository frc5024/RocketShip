class PIDController:
    def __init__(self, p, i, d):
        self.kp = p
        self.ki = i
        self.kd = d

        self._i = 0
        self._prev_err = 0
        self.setpoint = 0
    
    def setSetpoint(self, point):
        self.setpoint = point
    
    def Feed(self, val):
        error = self.setpoint - val # Error = Target - Actual
        self._i += (error*.02)
        derivative = (error - self._prev_err) / .02
        return self.kp*error + self.ki*self._i + self.kd*derivative