import machine
import neopixel
import utime

pin = machine.Pin(16)
pixel = neopixel.NeoPixel(pin, 1)

pixel.brightness = 0.2

def on(r, g, b):   # 0-255 colour control, use values < 50 for less painful brightness
    pixel[0] = (g, r, b)
    pixel.write()

def off():
    pixel[0] = (0, 0, 0)
    pixel.write()
    
def blink (count, ms, r, g, b):
    for i in range(count):
        toggle(g, r, b)
        utime.sleep_ms(ms)

def toggle(r, g, b):
    led_state = pixel[0]
    if led_state == (0, 0, 0):
        pixel[0] = (g, r, b)
        pixel.write()
    else:
        pixel[0] = (0, 0, 0)
        pixel.write()
        
def wipe(c, delay):
    pixel[0] = (0, c, 0)
    pixel.write()
    utime.sleep_ms(delay)
    pixel[0] = (c, 0, 0)
    pixel.write()
    utime.sleep_ms(delay)
    pixel[0] = (0, 0, c)
    pixel.write()
    utime.sleep_ms(delay)
    pixel[0] = (0, 0, 0)
    utime.sleep_ms(50)
