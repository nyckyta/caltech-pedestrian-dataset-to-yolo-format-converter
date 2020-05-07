import glob
from PIL import Image
import sys
import os

default_frame_size = (640, 640)

def squarify_img(dir_with_img, output_dir, square_side):
	for frame in sorted(glob.glob(dir_with_img + '/*.png')):
		new_frame = Image.new('RGB', default_frame_size, 'white')
		new_frame.paste(Image.open(frame), (0, 0))
		new_frame.thumbnail((square_side, square_side))

		#takes only image name , replace it from *.png to *_squared.png and then concatenate it with output directory
		new_frame_path = output_dir + '/' +frame[-frame[::-1].find('/'):].replace('.png', '_squared.png') 
		new_frame.save(new_frame_path, 'png')

	print('saved ' + new_frame_path)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		raise("Need to specify <path_to_directory_of_images> <output_path> <square_length>")
	dir_with_img = sys.argv[1]
	out_dir = sys.argv[2]
	square_side = int(sys.argv[3])

	if not os.path.isdir(out_dir):
		os.mkdir(out_dir)

	squarify_img(dir_with_img, out_dir, square_side)