#!/bin/python3

from PIL import Image
from multiprocessing import Pool, TimeoutError
import glob
import sys
import os

default_frame_size = (640, 640)

def squarify_image(output_dir, square_side, img_name):
	new_frame = Image.new('RGB', default_frame_size, 'white')
	new_frame.paste(Image.open(img_name), (0, 0))
	new_frame.thumbnail((square_side, square_side))

	#takes only image name , replace it from *.png to *_squared.png and then concatenate it with output directory
	new_frame_path = output_dir + '/' + img_name[-img_name[::-1].find('/'):].replace('.png', '_squared.png') 
	new_frame.save(new_frame_path, 'png')
	print('saved ' + new_frame_path)

def squarify_images(dir_with_img, output_dir, square_side, workers=None):
	if workers != None:
		for frame in sorted(glob.glob(dir_with_img + '/*.png')):
			workers.apply_async(squarify_image, (output_dir, square_side, frame))
		workers.close()
	else:
		for frame in sorted(glob.glob(dir_with_img + '/*.png')):
			squarify_image(output_dir, square_side, frame)	


if __name__ == '__main__':
	if len(sys.argv) < 4:
		raise Exception("Need to specify <path_to_directory_of_images> <output_path> <square_length>")
	dir_with_img = sys.argv[1]
	out_dir = sys.argv[2]
	square_side = int(sys.argv[3])

	workers = None
	if len(sys.argv) > 4:
		workers = Pool(processes=int(sys.argv[4]))	

	if not os.path.isdir(out_dir):
		os.mkdir(out_dir)

	squarify_images(dir_with_img, out_dir, square_side, workers)