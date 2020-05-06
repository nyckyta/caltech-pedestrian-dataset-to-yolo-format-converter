#!/bin/python3
# adapted from https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_seqs.py

import os
import sys
import glob
import cv2 as cv
import tarfile as tar


def save_img(dname, fn, i, frame):
	cv.imwrite('{}/{}_{}_{}.png'.format(
		out_dir, os.path.basename(dname),
		os.path.basename(fn).split('.')[0], i), frame)

out_dir = 'images'
if not os.path.exists(out_dir):
	os.makedirs(out_dir)

def convert(dir):
	for dname in sorted(glob.glob(dir)):
		for fn in sorted(glob.glob('{}/*.seq'.format(dname))):
			cap = cv.VideoCapture(fn)
			i = 0
			while True:
				ret, frame = cap.read()
				if not ret:
					break
				save_img(dname, fn, i, frame)
				i += 1
			print(fn)

def convert_data_from_tars_folder(dir_with_tars):
	with os.scandir(dir_with_tars) as entries:
		for entry in entries:
			full_path = entry.path
			entry_name = entry.name
			print('{} - current file'.format(full_path))
			tarfile = tar.open(full_path)
			print('.Seq files will be extracted into ./{}'.format(entry_name))
			tarfile.extractall()
			convert(entry_name.split('.')[0])

if __name__ == '__main__':
	args = sys.argv
	
	if len(args) < 2:
		raise Exception('Directory with CallTech archives should be passed')
	convert_data_from_tars_folder(args[1])

