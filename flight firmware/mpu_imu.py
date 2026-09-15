from MPU import MPU6050
import ext_func
import utime

print("MPU loaded")

class IMU_cont:
    def __init__(self):
        self.obj = MPU6050(0,0,1)  
        self.obj.callibrate_gyro()   # calibrate gyro 
        self.obj.callibrate_acc()   # calibrating accelerometer
        
        self.quat_buffer = [0.0, 0.0, 0.0, 0.0]   # initial list for efficiency
        
    def att(self):
        angles = self.obj.return_angles()

        qx, qy, qz, qw = ext_func.euler_to_quat(angles[2], angles[0], angles[1])   # euler angles from retun_angles() converted to quaternions

        self.quat_buffer[0] = qx
        self.quat_buffer[1] = qy
        self.quat_buffer[2] = qz
        self.quat_buffer[3] = qw

        return self.quat_buffer   # returns [qx, qy, qz, qw] (note quaternions exist within [-0.5, 0.5] per axis)


def imu_start():
    return 1