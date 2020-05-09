# convert the format of the [caltech pedestrian dataset](http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians) to the format that [yolo](https://pjreddie.com/darknet/yolo) uses

This repo is adapted from
- https://github.com/mitmul/caltech-pedestrian-dataset-converter
- https://pjreddie.com/media/files/voc_label.py

## dependencies

- opencv
- numpy
- scipy

## how to

1. Convert the `.tar` files with video to `.png` frames by running `$ ./generate-images.py {path_to_derectory_with_tar_files} {path_to_output} [amount_of_threads]`. This script takes all files from `<path_to_directory_with_tar_files>`, extracts each archive and converts extracted .seq files to `<path_to output>`, finally it removes folders with extracted .seq files. Parallel mode provides way to go through above described flow in regime like "one thread per archive". To enable parallelism need just to specify `<amount_of_threads> as integer value`. The most efficient way is to specify number of threads equal to number of the archives in directory (sure if you have enough cores on CPU).
2. Squared images work better, which is why you can convert the 640x480 frames to square frames by running `$ python squarify-images.py {path_to_derectory_with_images} {output_directory_path} {size_of_square_side} [amount_of_threads]`. It converts images to 640x640(by adding white bar) and then to specified size. 
3. Convert the `.vbb` annotation files to `.txt` files by running `$ python generate-annotation.py`. It will create the `labels` folder that contains the `.txt` files named like the frames and the `train.txt` and `test.txt` files that contain the paths to the images.
4. Adjust `.data` yolo file
5. Adjust `.cfg` yolo file: take e.g. `yolo-voc.2.0.cfg` and set `height = 640`, `width = 640`, `classes = 2`, and in the final layer `filters = 21` ([`= (classes + 5) * 3)`](https://github.com/AlexeyAB/darknet))

## folder structure
```
|- caltech
|-- annotations
|-- test06
|--- V000.seq
|--- ...
|-- ...
|-- train00
|-- ...
|- caltech-for-yolo (this repo, cd)
|-- generate-images.py
|-- generate-annotation.py
|-- images
|-- labels
|-- test.txt
|-- train.txt
```
