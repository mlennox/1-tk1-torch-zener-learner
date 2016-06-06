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
import math
import numpy
import os
import random
import string


def fetch_symbol_images():
	symbols_images = {}
	source_image_path = "../zener-images"

	for root, dirs, files in os.walk(source_image_path):
		for f in files:
			if f.endswith(".png"):
				image_name = string.split(f, ".")
				image = Image.open(source_image_path + "/" + f)
				symbols_images[image_name[0]] = image

	return symbols_images

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

def generate_random_shifts(img_size, size_factor):
	w = img_size[0] / size_factor
	h = img_size[1] / size_factor
	shifts = []
	for s in range(0,4):
		w_shift = (random.random() - 0.5) * w
		h_shift = (random.random() - 0.5) * h
		shifts.append((w_shift,h_shift))
	return shifts


# create random perspective
def create_perspective(img, factor):
	img_size=img.size
	w = img_size[0]
	h = img_size[1]
	shifts = generate_random_shifts(img_size, size_factor)
	coeffs = find_coeffs(
		[(shifts[0][0],shifts[0][1]),
		(w + shifts[1][0],shifts[1][1]),
		(w + shifts[2][0],h + shifts[2][1]),
		(shifts[3][0],h + shifts[3][1])],
		[(0,0),(w,0),(w,h),(0,h)])
	return img.transform((w,h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


# will adjust the canvas so that perspective transforms will not result in the image being cropped
# assumes the image background is white...
def adjust_canvas(img, size_factor):
	width, height = img.size
	canvas_size = (int(math.floor(width + 2 * (width / size_factor))), int(math.floor(height + 2 * (height / size_factor))))
	img_pos = (int(math.floor((canvas_size[0] - width)/2)), int(math.floor((canvas_size[1] - height)/2)))
	new_canvas = Image.new("RGBA", canvas_size, (255,255,255,0))
	new_canvas.paste(img, (img_pos[0], img_pos[1], img_pos[0] + width, img_pos[1] + height))
	return new_canvas


# will randomly rotate the image

def rotate_image(img, rotation_range):
	# we want to have random rotations but my feeling is 
	# we should have more smaller rotations than larger
	# this skews the random numbers toward zero
	rotation_factor = math.pow(random.uniform(0.0,1.0), 4)
	# we want to rotate either way
	rotation_direction = (1,-1)[random.random() > 0.5]
	rotation_angle = int(math.floor(rotation_range * rotation_factor * rotation_direction))
	return img.rotate(rotation_angle)
	

# determines how much perspective distortion to use
# factor <= 1 - no distortion
# 1 >= factor <= 5 - slight distortion
# 5 >= factor <= 30 - large but usable distortion
# factor > 30 = very large distortion
perspective_factor = 20
size_factor = 100.0 * (1.0 / perspective_factor)

# specify maximum rotation in degrees
rotation_range = 45

# load the images
images = fetch_symbol_images()

for symbol_name in images:
	symbol_img = images[symbol_name]
	adjusted_img = adjust_canvas(symbol_img, size_factor)
	for variant in range(1,10):
		deformed_image = create_perspective(adjusted_img, size_factor)
		deformed_image = rotate_image(deformed_image, rotation_range)
		generated_folder = '../generated/' + symbol_name + "/"
		if not os.path.exists(generated_folder):
			os.makedirs(generated_folder)
		deformed_image.save(generated_folder + symbol_name + str(variant) + ".png")






