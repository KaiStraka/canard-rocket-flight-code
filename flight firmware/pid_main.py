import utime

class PID_cont:
    __slots__ = ['kp', 'ki', 'kd', 'out_min', 'out_max', 
                 'integral', 'last_error', 'last_time', 'initialized',
                 'int_limit']

    def __init__(self, kp, ki, kd, out_min, out_max, int_limit=None):
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.out_min = float(out_min)
        self.out_max = float(out_max)

        self.int_limit = int_limit if int_limit is not None else (out_max * 10.0)   # ??

        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = 0
        self.initialized = False

    def compute(self, error, dt_ms=None):
        current_time_ms = utime.ticks_ms()

        if not self.initialized:   # initialization
            self.last_error = error
            self.last_time = current_time_ms
            self.initialized = True
            return 0.0

        if dt_ms is None:
            dt_ms = current_time_ms - self.last_time
            if dt_ms < 0:
                dt_ms = utime.ticks_diff(current_time_ms, self.last_time)
            
            if dt_ms <= 0.001:
                dt_ms = 0.001   # prevent zero division
        
        kp = self.kp
        ki = self.ki
        kd = self.kd
        int_lim = self.int_limit

        P = kp * error   # PROPORTIONAL

        if ki != 0:      # INTEGRAL (disabled)
            self.integral += error * dt_ms
            
            # Clamp integral to prevent windup
            if self.integral > int_lim:
                self.integral = int_lim
            elif self.integral < -int_lim:
                self.integral = -int_lim
            
            I = ki * self.integral
        else:
            I = 0.0

        delta_error = error - self.last_error
        D = (kd * delta_error * 1000.0) / dt_ms   # DERIVATIVE

        self.last_error = error
        self.last_time = current_time_ms

        output = P + I + D   # sum
        
        if output > self.out_max:
            output = self.out_max
        elif output < self.out_min:
            output = self.out_min
            
        return output

    def reset(self):
        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = utime.ticks_ms()
        self.initialized = False
