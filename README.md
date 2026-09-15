KAI STRAKA 09.2026

Complete flight code for an active-canard stabilized model rocket. Main control loop utilizes a quaternion-based PID loop and Kalman filter for IMU / barometer sensor fusion.

## <brb>
**SETUP**

The software is Micropython based and requires a suitable microcontroller. I used the RP2040 Zero. Other sensors used are the MPU6050 IMU and BMP180 barometer. Note the system has no guidance platforms.
The control hardware uses two servos, each controlling a pair of canards along the pitch and yaw axes. This system allows for independent pitch and yaw control, but no roll control. 
The flight firmware folder contains the entire code and logging files. Installation is as simple as uploading the files to the microcontroller. `main.py` will run automatically upon controller power on, and the rest of the control loop is autonomous.

## <brb> 
**CONTROL LOGIC**

(note the entire system is autonomous, all steps will happen automatically) Upon startup servos will undergo a 10 second control swipe. Following this the IMU will perform a 6 second calibration and will determine an upwards target vector pointing in the same direction as the rocket (thus if the rocket is sitting upright, the target vector will point straight up). Following the calibration the system will automatically switch to its main PID control loop, and will attempt to stabilize the rocket along its target vector. 

**Other info:** The canards have a gimbal range of 54 degrees in either direction. If the gimbal limit is exceeded, the canards will lock into their norm positions until power off. 
Due to memory limitations within the microcontroller, data logging is not continuous. Instead a preset altitude trigger (8 meters) will begin noting the maximum altitude achieved, and will log this altitude in `alt_data.txt` after 20 seconds of trigger activation. Upon canard lockout the altitude at the time of lockout will also be recorded, alongside the max alt into `alt_data.txt`.

## <brb>
**PID Control Loop**

The PID loop runs at 1000 Hz and is responsible for stabilizing the rocket along its target vector.
It uses a quaternion-based logic to perform attitude calculations. The main control loop uses two separate PID loops, one for pitch orientation and another for yaw orientation.

## <brb>
**FILE INFO**

`main.py`: main control loop, runs automatically upon startup and is responsible for the entire calibration and control sequence. Here PID values can be adjusted. This is the most important file.

`bmp_alt.py`: barometer code, includes max alt logging as well as sensor initialization and usage. Calls upon `bmp085.py`.

`mpu_imu.py`: IMU code, sensor initialization and usage. Calls upon `MPU.py`.

`servo_func.py`: includes all servo commands and setup. Calls upon `pixel_led.py`.

