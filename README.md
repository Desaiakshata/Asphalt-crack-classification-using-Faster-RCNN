# Asphalt-crack-classification-using-Faster-RCNN

This repository contains the detailed steps to use the asphalt pavement crack classification algorithm.

The crack classifcation algorithm consists two sub-parts:

Part 1 - Object detection based crack classifcation using Faster RCNN (Data preparation and Training)

Part 2 - Steps for Testing and Post-processing for crack classification based on COPACES

# Part 1 - Steps for data preparation and training the Faster RCNN model:

# Data preparation:

The following commands have to be run locally on the computer and not on GPU. 

1) Draw a white line for pavement marking using the pavement marking location in the LCMS xml file. The draw_markings.py script can be downloaded from github.
```
python draw_markings.py --image_path=<--> --xml_path=<--> --save_path=<-->
```
2) Annotate the images using the labelImg application. Install the application using pip and open it using the terminal. Specify the image directory and save directories by selecting respective folders in the application.
```
pip install labelImg
labelImg
```
# Training

The following steps are to be run on GPU.

1) Install and create a virtual python env. Then install the following python packages 
```
pip install --user virtualenv
python3 -m venv env
source env/bin/activate  #activate the virtual environment    
pip install tensorflow==1.15.2
pip install tf_slim
pip install --user xlutils
```

2) Gitclone Tensorflow Object detection API 
```
git clone https://github.com/tensorflow/models.git 
```

3) Copy the training images to the Images folder and annotations to the Annotations folder within the dataset folder as shown in the folder structure below.

On GPU2:

Method 1: Images are in Images folder, Annotations in Annotationsfolder and checkpoints in CPfolder.

For training using method 1 you have to change the paths in the config file and also class labels in label.pbtxt. 

4) Folder Structure - files on GPU2 
```
|-home
    |-models 
    |-Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API
     |-dataset
         |-Images
         |-Annotations
         |-label.pbtxt
         |-train.record
     |-CP
     |-pre_trained_models
     |-extra
     |-faster_rcnn_resnet101_coco.config
    |-draw_marking.py
```
5) Add the following folders to the PATH
```
export PATH="$/home/models/research/object_detection/:/home/models/research/slim/:$PATH"
and
export PYTHONPATH="$/home/models/research/object_detection/:/home/models/research/slim/:$PYTHONPATH"
```
6) Run the following command in the terminal. This command needs to be executed from the /model/research folder 
```
protoc object_detection/protos/*.proto --python_out=.
```
7) Make necessary changes to the training classes in the label.pbtxt file 

8) Create the pascal TF Record. This command needs to be executed from the /model/research/object_detection folder 
```
python /home/models/research/object_detection/dataset_tools/create_pascal_tf_record.py --data_dir=/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset --annotations_dir=/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset/Annotations --output_path=/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset/train.record --label_map_path=/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset/label.pbtxt
```
9) Make changes to the faster_rcnn_resnet101_coco.config by setting the path for the train.record and label.pbtxt for training.

10) Pretrained weights can be either downloaded online for Faster RCNN model or weights for custom trained Faster RCNN can be added to the CP folder.

11) Train the model. Checkpoints for the latest epoch are aved in the CP folder. 
```
python object_detection/legacy/train.py --train_dir='/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/CP' --pipeline_config_path=/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/faster_rcnn_resnet101_coco.config
```
# Part 2 - Testing the model and simultaneous post-processing for crack classification

The folder structure to be folowed for testing is the same as training. Place the test images in Images folder and Annotations in Annotations folder. Change the num examples in the config file to the number of testing images. 

1) For testing, use this notebook FasterRCNN_eval.ipynb from github. Upload the downloaded notebook to google drive and open it using google colaboratory.

2) Create a CP folder on google drive and add the trained model weights. Update the checkpoint file with the new path for weights.**(What files are required? (.data, .index, .meta, tfevent?))**

3) Create a directory to save the detection results and specify the path in '/home/models/research/object_detection/legacy/evaluator.py' file line 250

4) Upload the markings.xls file created using the draw_markings.py script to colab and add the path on line 175 in /home/models/research/object_detection/eval_util.py

5) Change the path to save the ouput xls file in /home/models/research/object_detection/utils/np_box_list_ops.py lines 602,621

6) Crack_category.py file contains the code for post-processing.

6) Run this command on the terminal
```
python object_detection/legacy/eval.py --checkpoint_dir='/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/CP' --eval_dir='/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/eval' --pipeline_config_path=/home/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/faster_rcnn_resnet101_coco.config
```

The output detection images are stored in the specified folder and the crack classification results are saved in a csv file as crack category and extent values for each image. 
