#!/bin/python3
# adapted from https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_seqs.py

import os
import shutil
import sys
import glob
import cv2 as cv
import tarfile as tar

def save_img(dname, fn, i, frame, out_dir):
	cv.imwrite('{}/{}_{}_{}.png'.format(
		out_dir, os.path.basename(dname),
		os.path.basename(fn).split('.')[0], i), frame)

def convert(dir, output_dir):
	if not os.path.isdir(output_dir):
		os.mkdir(output_dir)
	for dname in sorted(glob.glob(dir)):
		for fn in sorted(glob.glob('{}/*.seq'.format(dname))):
			cap = cv.VideoCapture(fn)
			i = 0
			while True:
				ret, frame = cap.read()
				if not ret:
					break
				save_img(dname, fn, i, frame, output_dir)
				i += 1
			print(fn)

def unpack_and_convert(entry, output_dir):
	full_path = entry.path
	entry_name = entry.name
	extraction_folder_name = entry_name[:-4]

	tarfile = tar.open(full_path)
	tarfile.extractall()

	convert(extraction_folder_name, output_dir)
	shutil.rmtree(extraction_folder_name)

def convert_data_from_tars_folder(dir_with_tars, output_dir):
	with os.scandir(dir_with_tars) as entries:
		for entry in entries:
			unpack_and_convert(entry, output_dir)



if __name__ == '__main__':
	args = sys.argv
	
	if len(args) < 2:
		raise Exception('Directory with CallTech archives should be passed')
	if (len(args) < 3):
		raise Exception('Output directory should be passed')

	convert_data_from_tars_folder(args[1], args[2])

