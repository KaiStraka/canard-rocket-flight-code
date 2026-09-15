import math
import pixel_led
import utime
import servo_func

norm1 = servo_func.s_norms()[0]    # SERVO1 NORM
norm2 = servo_func.s_norms()[1]   # SERVO2 NORM
slew = servo_func.s_norms()[2]

def euler_to_quat(Z, Y, X):   # (roll, pitch, yaw)
    
    Z = math.radians(Z)
    Y = math.radians(Y)
    X = math.radians(X)
    
#     Z = max(-1.0, min(1.0, Z))
#     Y = max(-1.0, min(1.0, Y))
#     X = max(-1.0, min(1.0, X))

    cz, cy, cx = math.cos(Z/2), math.cos(Y/2), math.cos(X/2)
    sz, sy, sx = math.sin(Z/2), math.sin(Y/2), math.sin(X/2)

    # quaternion components (w, x, y, z)
    qw = cz*cy*cx + sz*sy*sx
    qx = sz*cy*cx - cz*sy*sx
    qy = cz*sy*cx + sz*cy*sx
    qz = cz*cy*sx - sz*sy*cx
    
    return (qx, qy, qz, qw)   # return tuple cuz faster


def quat_conj(q):
    return [-q[0], -q[1], -q[2], q[3]]


def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1[3], q1[0], q1[1], q1[2]
    w2, x2, y2, z2 = q2[3], q2[0], q2[1], q2[2]

    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2

    return [x, y, z, w]


def get_error_angle(q_diff):
    w = q_diff[3]   # scalar
    w = max(-1.0, min(1.0, w))
    
    angle = 2.0 * math.acos(w)
    if angle < 0.001:
        return 0.0, 0.0, 0.0
    
    sin_half = math.sin(angle / 2.0)
    if abs(sin_half) < 0.0001:
        sin_half = 0.0001
        
    x_err = (q_diff[0] / sin_half) * angle   # roll
    y_err = (q_diff[1] / sin_half) * angle   # pitch
    z_err = (q_diff[2] / sin_half) * angle   # yaw
    
    return x_err, z_err, y_err   # z and y swapped cuz idfk


def error_calc(quat, target_q):
    conj = quat_conj(quat)
    diff = quat_mult(target_q, conj)
    r, p, y = get_error_angle(diff)

    return p, y


def deg_calc(y_err, p_err, y_bias, p_bias, pid_yaw, pid_pitch):
    y_err -= y_bias
    p_err -= p_bias 
    
    d_yaw = pid_yaw.compute(y_err)   # delta yaw/pitch (PID)
    d_pitch = pid_pitch.compute(p_err)
    
    deg_yaw = norm1 - d_yaw
    deg_pitch = norm2 - d_pitch
    
    deg_yaw = max(norm1 - slew, min(norm1 + slew, deg_yaw))   # ensure servo limits
    deg_pitch = max(norm2 - slew, min(norm2 + slew, deg_pitch))
    
    return deg_pitch, deg_yaw


def sensor_check(x, y):
    utime.sleep_ms(250)
    if x + y == 2:
        pixel_led.blink(6, 0, 50, 0)
    elif x + y != 2:
        pixel_ledblink(6, 50, 0, 0)
    return None