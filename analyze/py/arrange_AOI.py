from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import json

path = '../data/screenshot.png'
img = Image.open(path)
draw = ImageDraw.Draw(img)

x_offset = 247
y_offset = 138
ratio = 2.15

data = json.load(open('../../src/data/random/0.json'))
for group in data['groups']:
    x = group['x']
    y = group['y']
    dx = group['dx']
    dy = group['dy']
    x = x * ratio + x_offset
    y = y * ratio + y_offset
    dx = dx * ratio
    dy = dy * ratio
    draw.rectangle((x, y, x + dx, y + dy), outline=(255, 0, 0))

img.show()
