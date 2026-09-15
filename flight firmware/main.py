import pixel_led
import ext_func
import utime
import servo_func
import servo
from servo import Servo

import bmp_alt
import mpu_imu
from mpu_imu import IMU_cont
import pid_main
from pid_main import PID_cont

pixel_led.blink(4, 250, 180, 180, 180)   # startup blink
servo_func.control_swipe()   # canard surface check
pixel_led.on(0, 150, 0)   # imu calibration light

KP = 10.0
KI = 0.0   # MUST REMAIN 0.0 | DO NOT MODIFY
KD = 3.0

target_q = [0.0, 0.0, 0.0, 1.0]   # MUST REMAIN [0.0, 0.0, 0.0, 1.0] | DO NOT MODIFY

servo1 = servo_func.s_norms()[3]   # 1 front | YAW
servo2 = servo_func.s_norms()[4]   # 2 aft | PITCH
slew = servo_func.s_norms()[2]

slew_lock = False   # MUST REMAIN FALSE | DO NOT MODIFY
lock_alt = 0

pid_yaw = PID_cont(KP, KI, KD, -slew, slew)     # initialize pid yaw
pid_pitch = PID_cont(KP, KI, KD, -slew, slew)   # initialize pid pitch

mpu = IMU_cont()   # initialize imu
utime.sleep_ms(500)

start_q = mpu.att()   # get imu deviations
p_bias, y_bias = ext_func.error_calc(start_q, target_q)

pid_yaw.reset()
pid_pitch.reset()
print("\nsystems GO")

while True:   # MAIN LOOP
    current_q = mpu.att()   # get imu data
    p_err, y_err = ext_func.error_calc(current_q, target_q)
    deg_pitch, deg_yaw = ext_func.deg_calc(y_err, p_err, y_bias, p_bias, pid_yaw, pid_pitch)   # correction calcs

    if servo_func.servo_lock(mpu.att()[1], mpu.att()[2], True) and not slew_lock:   # set slew_lock bool
        slew_lock = True
        lock_alt = bmp_alt.alt(None)
 
    if slew_lock:   # lock servos check
        servo_func.servo_set_norm()
        pixel_led.toggle(150, 0, 0)   # red led locked
    else:
        servo1.write(deg_yaw)     # yaw correction
        servo2.write(deg_pitch)   # pitch correction
        pixel_led.toggle(0, 0, 150)   # blue led free

    bmp_alt.alt(lock_alt)   # bmp