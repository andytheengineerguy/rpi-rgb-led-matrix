#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)
options = RGBMatrixOptions()

screen_type = sys.argv[2]
if screen_type == 'indoor':
    print("\nScreen: Indoor, 128x64, 1/30 scan rate\n")
    # matrix config
    
    options.rows = 64
    options.cols = 128
    options.multiplexing = 0
    options.gpio_slowdown = 3
    options.row_address_type = 0
    options.show_refresh_rate = True
    options.chain_length = 2
    options.parallel = 1
    options.pixel_mapper_config = 'u-mapper'
    options.hardware_mapping = 'regular'
    options.pwm_bits = 5
    options.brightness = 100
    options.scan_mode = 0
    options.pwm_lsb_nanoseconds = 120 # default 130
    options.limit_refresh_rate_hz = 240
    options.pwm_dither_bits = 1
elif screen_type == 'outdoor':
    print("\nScreen: Outdoor, 104x52, 1/13 scan rate\n")
    
    # physical config
    options.rows = 52
    options.cols = 104
    options.chain_length = 1
    options.parallel = 2
    
    # internal multiplexing
    options.multiplexing = 19       # this is my custom multiplexer pattern
    options.row_address_type = 0

    # color / fps
    options.pwm_bits = 10
    options.pwm_dither_bits = 1
    
    # other
    options.brightness = 100
    options.show_refresh_rate = True
    options.gpio_slowdown = 4
    
    # not used
    # options.panel_type = 'FM6126A'
    # options.pixel_mapper_config = 'Rotate:90'
    # options.scan_mode = 0
    # options.hardware_mapping = 'regular'
    # options.limit_refresh_rate_hz = 360
    #options.pwm_lsb_nanoseconds = 110 # default 130

# create matrix
matrix = RGBMatrix(options = options)

# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

# put static image on the screen!
matrix.SetImage(image.convert('RGB'))

# seems to only do this once
# how would you get a gif to display..?
# loop through all frames in the gif?

# wait for ctrl-c to exit
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)