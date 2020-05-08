#!/bin/python3

# adapted from
# - https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_annotations.py
# - https://pjreddie.com/media/files/voc_label.py

import os
import glob
from scipy.io import loadmat
import sys
import zipfile as zp
import shutil

default_frame_size = (640, 480)
default_squared_img_size = (640, 640)
classes = ['person', 'people'] # others are 'person-fa' and 'person?'

def convertBoxFormat(box, frame_size):
	(box_x_left, box_y_top, box_w, box_h) = box
	di = (1., 1.) #ration of default image size to new squared image size
	if default_frame_size != frame_size: #If frame size is not equal to default frame size then it was squarified 
		x_ratio = frame_size[0] / default_squared_img_size[0]
		y_ratio = frame_size[1] / default_squared_img_size[1]
		di = (x_ratio, y_ratio) 

	(image_w, image_h) = frame_size
	dw = di[0]/image_w 
	dh = di[1]/image_h
	x = (box_x_left + box_w / 2.0) * dw
	y = (box_y_top + box_h / 2.0) * dh
	w = box_w * dw
	h = box_h * dh
	return (x, y, w, h)

def convert_annotations_to_txt_format(path_to_annotations, output_path, frame_size):
	# traverse sets
	squared = default_frame_size == frame_size
	number_of_truth_boxes = 0

	datasets = {
		'train' : open('train' + ('_squared' if squared else '')  + '.txt', 'w'),
		'test' : open('test' + ('_squared' if squared else '')  + '.txt', 'w')
	}

	if not zp.is_zipfile(path_to_annotations):
		raise Exception('%s Is not annotations.zip'%(path_to_annotations))
	with zp.ZipFile(path_to_annotations) as annotations_archive:
		annotations_archive.extractall()
	
	for caltech_set in sorted(glob.glob('./annotations/set*')):
		set_nr = os.path.basename(caltech_set).replace('set', '')
		dataset = 'train' if int(set_nr) < 6 else 'test'
		set_id = dataset + set_nr
		print(caltech_set)

		# traverse videos
		for caltech_annotation in sorted(glob.glob(caltech_set + '/*.vbb')):
			vbb = loadmat(caltech_annotation)
			obj_lists = vbb['A'][0][0][1][0]
			obj_lbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
			video_id = os.path.splitext(os.path.basename(caltech_annotation))[0]

			# traverse frames
			for frame_id, obj in enumerate(obj_lists):
				if len(obj) > 0:

					# traverse labels
					labels = ''
					for pedestrian_id, pedestrian_pos in zip(obj['id'][0], obj['pos'][0]):
						pedestrian_id = int(pedestrian_id[0][0]) - 1
						pedestrian_pos = pedestrian_pos[0].tolist()
						# class filter and height filter: here example for medium distance
						if obj_lbl[pedestrian_id] in classes and pedestrian_pos[3] > 30 and pedestrian_pos[3] <= 80:
							class_index = classes.index(obj_lbl[pedestrian_id])
							yolo_box_format = convertBoxFormat(pedestrian_pos, frame_size)
							labels += str(class_index) + ' ' + ' '.join([str(n) for n in yolo_box_format]) + '\n'
							number_of_truth_boxes += 1

					# if no suitable labels left after filtering, continue
					if not labels:
						continue

					image_id = set_id + '_' + video_id + '_' + str(frame_id)
					file_name_template = output_path + '/' + image_id + ('_squared' if squared else '')
					print(dataset)
					datasets[dataset].write(file_name_template + '.png\n')
					label_file = open(file_name_template + '.txt', 'w')
					label_file.write(labels)
					label_file.close()
					print('finished ' + image_id)
			
	for dataset in datasets.values():
		dataset.close()
	print(number_of_truth_boxes) # useful for statistics
	shutil.rmtree('./annotations')


if __name__ == '__main__':
	if len(sys.argv) < 3:
		raise Exception("Need to spesify path to annotations.zip files and output directory which contains images")
	path_to_archive = sys.argv[1]
	output_directory = sys.argv[2] #output directory is directory with images

	if not os.path.isdir(output_directory):
		os.mkdir(output_directory)

	frame_size = default_frame_size #default size
	if len(sys.argv) > 3: #secod argument specifies size of squared image
		frame_square_length = int(sys.argv[3])
		frame_size = (frame_square_length, frame_square_length)
	convert_annotations_to_txt_format(path_to_archive, output_directory, frame_size)