# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_pcf8523
import adafruit_scd4x
import adafruit_dps310
import digitalio
from rainbowio import colorwheel
import neopixel

i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
rtc = adafruit_pcf8523.PCF8523(i2c)
dps310 = adafruit_dps310.DPS310(i2c)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

NUM_PIXELS = 24  # NeoPixel strip length (in pixels)

enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

strip = neopixel.NeoPixel(board.D5, NUM_PIXELS, brightness=0.01)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
if False:   # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2021,  12,   31,   22,  00,  00,    5,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time

    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()

print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

while True:
    t = rtc.datetime
    #print(t)     # uncomment for debugging

    if scd4x.data_ready:
        print("The date is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mday, t.tm_mon, t.tm_year))
        print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Temperature = %.2f *C" % dps310.temperature)
        print("Pressure = %.2f hPa" % dps310.pressure)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()

        # display CO2 Level indicator
        if scd4x.CO2 < 1000:
            strip.fill(GREEN)
        elif scd4x.CO2 >= 1000 and scd4x.CO2 < 2000:
            strip.fill(YELLOW)
        elif scd4x.CO2 >= 2000 and scd4x.CO2 < 3000:
            strip.fill(PURPLE)
        else:
            strip.fill(RED)


    #for i in range(255):
    #    strip.fill((colorwheel(i)))

    time.sleep(1)


