from machine import Pin, I2C
from bmp085 import BMP180
import pixel_led

import utime

print("BMP loaded")

i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 400000)
bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = bmp.pressure

d_alt = 0.0
v_m = 0.0
max_m = 0.0
filtered_alt = 0.0
alt_buffer = [0.0, 0.0, 0.0]

alt_trig = 8.0         # log trigger alt
alt_time_length = 30   # log time delay (seconds)

alt_time = 0
alt_check = False
time_check = False

file = open("alt_data.txt", "a")
file.write(f"\n.	")
file.flush()


def alt(lock_alt):   # lock_alt from main only for logging purposes
    global d_alt, max_m, v_m, filtered_alt, log_buffer, alt_time, alt_check, time_check, alt_trig, alt_time_length

    tempC = bmp.temperature   # get the temperature in degree celsius
    pres_hPa = bmp.pressure   # get the pressure in hpa
    alt_m = bmp.altitude      # get the altitude to 2 decimal spaces

    # low pass filter
    filtered_alt = (alt_m * 0.1) + (filtered_alt * (0.9))   # 0.1 = smoothing factor

    v_m = (filtered_alt - d_alt) * 1000   # m/s calc -> * 1000 cuz 1000Hz
    d_alt = filtered_alt

    if filtered_alt >= max_m:   # max alt check
        max_m = filtered_alt

    current_time = utime.ticks_ms()

    alt_buffer[0] = filtered_alt
    alt_buffer[1] = v_m
    alt_buffer[2] = max_m

    if filtered_alt > alt_trig and not alt_check:
        alt_check = True   # passed alt threshold
        alt_time = current_time   # set time at alt pass
        pixel_led.on(0, 225, 0)   # green led indicator

    if alt_check and not time_check:
        elapsed_ms = utime.ticks_diff(current_time, alt_time)
        if elapsed_ms >= (alt_time_length * 1000):   # n sec at 1000Hz
            file.write(f"{round(max_m, 3)} max alt | {round(lock_alt, 3)} lock alt")   # write max alt
            file.flush()
            pixel_led.on(0, 225, 0)   # green led indicator
            time_check = True

    utime.sleep_ms(1)   # 1000Hz
    return (alt_buffer[0])


def log_alt(data, info):
    file.write(f"{round(data, 3)} {info} ")   # write max alt
    file.flush()
    pixel_led.on(0, 225, 0)   # green led indicator


def bmp_start():
    return 1
