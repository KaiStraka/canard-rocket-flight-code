import servo
from servo import Servo
import pixel_led
import utime

servo1 = Servo(pin_id = 5)   # 1 front | YAW
servo2 = Servo(pin_id = 6)   # 2 aft | PITCH

# degrees
norm1 = 94.0   # SERVO1 NORM
norm2 = 93.0   # SERVO2 NORM
slew = 20.0

# slew lock is in fractions of 0.5, since quats exist within [-0.5, 0.5]
# quat [0, 0.5] parametrizes to [0, pi/2] octants in degrees
slew_lock = 0.3   # 0.1 ~ 18 deg | 0.125 ~ 22.5 deg | .0833 ~ 15 deg | 0.167 ~ 30 deg

servo1.write(norm1)   # inital set to norm
servo2.write(norm2)
utime.sleep_ms(500)


def servo_lock(deg1, deg2, lock = bool):   # locks servos to norms if past slew_lock
    if abs(deg1) >= slew_lock or abs(deg2) >= slew_lock:     # pitch or yaw
        pixel_led.on(150, 0, 0)
        if lock:
            return True   # inform main of lock condition


def servo_set_norm():   # sets both servos to norms
    servo1.write(norm1)
    servo2.write(norm2)


def s_norms():   # send servo base info
    return (norm1, norm2, slew, servo1, servo2)


def control_swipe():   # servo surface deflection check
    single_control_swipe(servo1, norm1, 500)   # servo 1 FRONT swipe
    single_control_swipe(servo2, norm2, 500)   # servo 2 AFT swipe

    servo1.write(norm1 - slew)            # both servo swipe
    servo2.write(norm2 - slew)
    utime.sleep_ms(750)
    servo1.write(norm1 + slew)
    servo2.write(norm2 + slew)
    utime.sleep_ms(750)
    servo1.write(norm1)
    servo2.write(norm2)
    utime.sleep_ms(300)

    control_swipe_cont_snap(8)
    utime.sleep_ms(500)
    control_swipe_cont(4)
    servo_set_norm()
    utime.sleep_ms(300)


def single_control_swipe(servo, norm, ms):   # single servo surface swipe
    servo.write(norm - slew)
    utime.sleep_ms(ms)
    servo.write(norm)
    utime.sleep_ms(ms)
    servo.write(norm + slew)
    utime.sleep_ms(ms)
    servo.write(norm)
    utime.sleep_ms(ms)


def control_swipe_cont(ms):   # both servo continuous surface swipe
    i = 0
    while i <= (slew + 5):
        servo1.write(norm1 - i)
        servo2.write(norm2 - i)
        i += .5
        utime.sleep_ms(ms)
    i = slew
    while i >= (-slew - 5):
        servo1.write(norm1 - i)
        servo2.write(norm2 - i)
        i -= .5
        utime.sleep_ms(ms)
    i = -slew
    while i <= 0:
        servo1.write(norm1 - i)
        servo2.write(norm2 - i)
        i += .5
        utime.sleep_ms(ms)


def control_swipe_cont_snap(ms):   # both servo continuous snap back
    i = 0
    while i <= (slew + 5):
        servo1.write(norm1 - i)
        servo2.write(norm2 - i)
        i += .5
        utime.sleep_ms(ms)
    i = 0
    
    utime.sleep_ms(100)
    servo1.write(norm1)
    servo2.write(norm2)
    utime.sleep_ms(500)
    
    while i >= (-slew - 5):
        servo1.write(norm1 - i)
        servo2.write(norm2 - i)
        i -= .5
        utime.sleep_ms(ms)

    utime.sleep_ms(100)
    servo1.write(norm1)
    servo2.write(norm2)

