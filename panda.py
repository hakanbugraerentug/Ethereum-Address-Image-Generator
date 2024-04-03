from PIL import Image
from PIL import ImageFilter, ImageOps

import numpy as np

threshold = 250

# convert image to a list of pixels
img = Image.open("Cypher.png")
image_gray = img.convert('LA')
image_gray

pixels = list(img.getdata())

# convert data list to contain only black or white
newPixels = []
for pixel in pixels:
    # if looks like black, convert to black
    if pixel[0] <= threshold:
        newPixel = (0, 0, 0)
    # if looks like white, convert to white
    else:
        newPixel = (255, 255, 255)
    newPixels.append(newPixel)

# create a image and put data into it
newImg = Image.new(img.mode, img.size)
newImg.putdata(newPixels)

# ADD GAUSSIAN BLUR
gaus = newImg.filter(ImageFilter.GaussianBlur(radius=5))

# INVERT THE COLORS
im_invert = ImageOps.invert(gaus.convert('RGB')).convert('L')
im_invert = ImageOps.flip(im_invert)
inv_data = np.array(im_invert.getdata())
inv_data[inv_data < 128] = 10
inv_data[0] = 0

inv_data = np.reshape(inv_data, (174, 745))
img = Image.fromarray(np.uint8(inv_data), 'L')

data = np.array(img.getdata())
DATA = data.reshape((174, 745)).T
