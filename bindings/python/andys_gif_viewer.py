#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# gif setup

if len(sys.argv) < 2:
    sys.exit("Require a gif argument")
else:
    image_file = sys.argv[1]

gif = Image.open(image_file)

try:
    num_frames = gif.n_frames
except Exception:
    sys.exit("provided image is not a gif")

# screen setup
options = RGBMatrixOptions()
screen_type = sys.argv[2]

if screen_type == 'indoor':
    print("\nScreen: Indoor, 128x64, 1/30 scan rate\n")
    options.rows = 64
    options.cols = 128
    options.multiplexing = 20
    options.gpio_slowdown = 4
    options.row_address_type = 0
    options.show_refresh_rate = True
    options.chain_length = 1
    options.parallel = 2
    options.hardware_mapping = 'regular'
    options.pwm_bits = 7
    options.brightness = 70
    options.scan_mode = 0
    options.pwm_lsb_nanoseconds = 100 # default 130
    # options.limit_refresh_rate_hz = 240
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
    options.pwm_lsb_nanoseconds = 130 # default 130
    
    
    # other
    options.brightness = 100
    options.show_refresh_rate = True
    options.gpio_slowdown = 3
    
    # not used
    # options.panel_type = 'FM6126A'
    # options.pixel_mapper_config = 'Rotate:90'
    # options.scan_mode = 0
    # options.hardware_mapping = 'regular'
    # options.pwm_lsb_nanoseconds = 110 # default 130
    #options.limit_refresh_rate_hz = 360

matrix = RGBMatrix(options = options)

# Preprocess the gifs frames into canvases to improve playback performance
canvases = []
print("\nPreprocessing gif, this may take a moment depending on the size of the gif...\n")
for frame_index in range(0, num_frames):
    gif.seek(frame_index)
    # must copy the frame out of the gif, since thumbnail() modifies the image in-place
    frame = gif.copy()
    frame.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    canvas = matrix.CreateFrameCanvas()
    canvas.SetImage(frame.convert("RGB"))
    canvases.append(canvas)
# Close the gif file to save memory now that we have copied out all of the frames
gif.close()

print("\nCompleted Preprocessing, displaying gif\n")

try:
    print("Press CTRL-C to stop.")

    # Infinitely loop through the gif
    cur_frame = 0
    while(True):
        matrix.SwapOnVSync(canvases[cur_frame], framerate_fraction=15)
        if cur_frame == num_frames - 1:
            cur_frame = 0
        else:
            cur_frame += 1
except KeyboardInterrupt:
    sys.exit(0)
