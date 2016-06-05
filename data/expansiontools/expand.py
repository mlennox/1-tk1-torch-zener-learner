# looping a bunch of times...
# pick/load one of symbols
# create image 2 or 3 times the size of the symbol
# add the symbol to the centre
# randomly distort, translate and rotate the image
# crop to the image
# resize to size suitable for neural net input
# save image and metadata in whatever way is required - probably just save to a nmaed folder and have a second program to generate the final training data from that

from PIL import Image
from PIL import ImageDraw
import numpy
import random
import os


def fetch_symbol_images():
	symbols_images = []
	source_image_path = "../zener-images"

	for root, dirs, files in os.walk(source_image_path):
		for f in files:
			if f.endswith(".png"):
				image = Image.open(source_image_path + "/" + f)
				symbols_image_files.append(image)

	return symbols_image_files

# https://github.com/nathancahill/snippets/blob/master/image_perspective.py
# pa - starting points
# pb - ending points
# func will find the relevant coeffs that will result in the transformation of pa to pb
# and this will be used to transform the entire image
def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def generate_random_shifts(img_size):
	w = img_size[0] / size_factor
	h = img_size[1] / size_factor
	shifts = []
	for s in range(0,4):
		w_shift = (random.random() - 0.5) * w
		h_shift = (random.random() - 0.5) * h
		shifts.append((w_shift,h_shift))
	return shifts


# create random perspective
def create_perspective(img):
	img_size=img.size
	w = img_size[0]
	h = img_size[1]
	shifts = generate_random_shifts(img_size)
	coeffs = find_coeffs(
		[(shifts[0][0],shifts[0][1]),
		(w + shifts[1][0],shifts[1][1]),
		(w + shifts[2][0],h + shifts[2][1]),
		(shifts[3][0],h + shifts[3][1])],
		[(0,0),(w,0),(w,h),(0,h)])
	return img.transform((w,h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)



def initial_image():
	image = Image.new("RGB", (w + w_shift,h + h_shift), bg_color)
	# we will choose this font randomly too
	# font = ImageFont.truetype(font_file, 16)
	draw = ImageDraw.Draw(image)

	return image


