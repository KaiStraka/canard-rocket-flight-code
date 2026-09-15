KAI STRAKA 09.2026

Complete flight code for an active-canard stabilized model rocket.

## <brb>
**SETUP**

The software is Micropython based and requires a suitable microcontroller. I used the RP2040 Zero. Other sensors used are the MPU6050 IMU and BMP180 barometer. Note the system has no guidance platforms.
The control hardware uses two servos, each controlling a pair of canards along the pitch and yaw axes, respectively. This system allows for independent pitch and yaw control, but no roll control. 
The flight firmware folder contains the entire code and logging files, installation is as simple as uploading the files to the microcontroller. `main.py` will run automatically upon controller power on, and the rest of the control loop is autonomous.

## <brb> 
**Control Logic**

(note the entire system is autonomous, all steps will happen automatically) Upon startup servos will undergo a ten second control swipe. Following this, the IMU will perform a six second calibration and will determine an upwards target vector pointing in the same direction as the rocket (thus if the rocket is sitting upright, the target vector will point straight up). Following the calibration the system will automatically switch to its main PID control loop, and will attempt to stabilize the rocket along its target vector. 

**Canard and LED info:** The canards have a gimbal range of 54 degrees in either direction. If the gimbal limit is exceeded, the canards will lock into their norm positions until power off. A solid green LED indicates IMU calibration, a flashing blue LED indicates free canard control, a flashing red LED indicates canard lockout. A solid blue or red LED indicates system crash. All LED functions are in `pixel_led.py`.

**Logging:** Due to memory limitations within the microcontroller, data logging is not continuous. Instead a preset altitude trigger (8 meters) will begin noting the maximum altitude achieved, and will log this altitude in `alt_data.txt` after 20 seconds of trigger activation. Upon canard lockout the altitude at the time of lockout will also be recorded, alongside the max alt into `alt_data.txt`.

## <brb>
**PID Control Loop**

The PID loop runs at 1000 Hz and is responsible for stabilizing the rocket along its target vector.
It uses a quaternion-based logic to perform attitude calculations. The main control loop uses two separate PID loops, one for pitch orientation and another for yaw orientation. All PID related math is done in `pid_main.py`. PID values can be adjusted in `main.py`, and must be tuned according to rocket specifications.

## <brb>
**File Info**

`main.py`: main control loop, runs automatically upon startup and is responsible for the entire calibration and control sequence. This is the most important file.

`bmp_alt.py`: barometer code, includes max alt logging as well as sensor initialization and usage. 

`mpu_imu.py`: IMU code, sensor initialization and usage.

`servo_func.py`: includes all servo commands and setup.

Unmentioned files are responsible for background math functions and get called upon by the files above.
