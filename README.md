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

1) Install and create a virtual python env. Then install the following python packages (On GPU2: ~/a1/faster_rcnn/env/)
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

Method 1: Images are in Images folder. Annotations are in Annotations folder and checkpoints are in the CP folder.

Method 2: Images are in Images_method2 folder, Annotations in Annotations_method2 folder and checkpoints in CP_method2 folder.

For training using method 2 you have to change the paths in the config file and also class labels in label.pbtxt. Change the names of the folder from Images_method2 to Images, Annotations_method2 to Annotations and CP_method2 to CP.

4) Folder Structure - files on GPU2 **(The structure is different from GPU2, the commands below also require modifications since the path is different), (there is no images in the "Image_method1" folder on GPU2), (Does the dataset contains train/valid/test data or just for training?)**
```
|-home
 |-gpu_user
  |-a1
   |-faster_rcnn
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
export PATH="$/home/gpu_user/a1/faster_rcnn/models/research/object_detection/:/home/gpu_user/a1/faster_rcnn/models/research/slim/:$PATH"
and
export PYTHONPATH="$/home/gpu_user/a1/faster_rcnn/models/research/object_detection/:/home/gpu_user/a1/faster_rcnn/models/research/slim/:$PYTHONPATH"
```
6) Run the following command in the terminal. This command needs to be executed from the /model/research folder **(where should the users run this command?)**
```
protoc object_detection/protos/*.proto --python_out=.
```
7) Make necessary changes to the training classes in the label.pbtxt file **(What are necessary changes? Please provide both label files you used for method 1 and method 2)**

8) Create the pascal TF Record. This command needs to be executed from the /model/research/object_detection folder **(Error occur: FileNotFoundError: [Errno 2] No such file or directory: '/home/gpu_user/a1/faster_rcnn/Faster-RCNN/dataset/Annotations')**
```
python /home/gpu_user/a1/faster_rcnn/models/research/object_detection/dataset_tools/create_pascal_tf_record.py --data_dir=/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset --annotations_dir=/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset/Annotations --output_path=/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset/train.record --label_map_path=/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/dataset/label.pbtxt
```
9) Make changes to the faster_rcnn_resnet101_coco.config by setting the path for the train.record and label.pbtxt for training.

10) Pretrained weights can be either downloaded online for Faster RCNN model or weights for custom trained Faster RCNN can be added to the CP folder.

11) Train the model. Checkpoints for the latest epoch are aved in the CP folder. **(Will the code save checkpoint every certain epoch or it just saves the latest checkpoint file?)**
```
python object_detection/legacy/train.py --train_dir='/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/CP' --pipeline_config_path=/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/faster_rcnn_resnet101_coco.config
```
# Part 2 - Testing the model and simultaneous post-processing for crack classification

The folder structure to be folowed for testing is the same as training. Place the test images in Images folder and Annotations in Annotations folder. Change the num examples in the config file to the number of testing images. **(Is the testing data also on GPU2?)**

1) For testing, use this notebook FasterRCNN_eval.ipynb from github. Upload the downloaded notebook to google drive and open it using google colaboratory.

2) Create a CP folder on google drive and add the trained model weights. Update the checkpoint file with the new path for weights.**(What files are required? (.data, .index, .meta, tfevent?))**

3) Create a directory to save the detection results and specify the path in '/home/gpu_user/a1/faster_rcnn/models/research/object_detection/legacy/evaluator.py' file line 250

4) Upload the markings.xls file created using the draw_markings.py script to colab and add the path on line 175 in /home/gpu_user/a1/faster_rcnn/models/research/object_detection/eval_util.py

5) Change the path to save the ouput xls file in /home/gpu_user/a1/faster_rcnn/models/research/object_detection/utils/np_box_list_ops.py lines 602,621

6) Crack_category.py file contains the code for post-processing.

6) Run this command on the terminal
```
python object_detection/legacy/eval.py --checkpoint_dir='/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/CP' --eval_dir='/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/eval' --pipeline_config_path=/home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/faster_rcnn_resnet101_coco.config
```
**Error occurred when running this line of code on the Jupyter Notebook:**
```
INFO:tensorflow:Starting evaluation at 2020-08-25-19:41:35
I0825 19:41:35.705055 139898233591680 eval_util.py:537] Starting evaluation at 2020-08-25-19:41:35
Traceback (most recent call last):
  File "object_detection/legacy/eval.py", line 142, in <module>
    tf.app.run()
  File "/usr/local/lib/python3.6/dist-packages/tensorflow_core/python/platform/app.py", line 40, in run
    _run(main=main, argv=argv, flags_parser=_parse_flags_tolerate_undef)
  File "/usr/local/lib/python3.6/dist-packages/absl/app.py", line 299, in run
    _run_main(main, args)
  File "/usr/local/lib/python3.6/dist-packages/absl/app.py", line 250, in _run_main
    sys.exit(main(argv))
  File "/usr/local/lib/python3.6/dist-packages/tensorflow_core/python/util/deprecation.py", line 324, in new_func
    return func(*args, **kwargs)
  File "object_detection/legacy/eval.py", line 138, in main
    graph_hook_fn=graph_rewriter_fn)
  File "/content/models/research/object_detection/legacy/evaluator.py", line 299, in evaluate
    eval_export_path=eval_config.export_path)
  File "/content/models/research/object_detection/eval_util.py", line 538, in repeated_checkpoint_run
    model_path = tf.train.latest_checkpoint(checkpoint_dirs[0])
  File "/usr/local/lib/python3.6/dist-packages/tensorflow_core/python/training/checkpoint_management.py", line 341, in latest_checkpoint
    if file_io.get_matching_files(v2_path) or file_io.get_matching_files(
  File "/usr/local/lib/python3.6/dist-packages/tensorflow_core/python/lib/io/file_io.py", line 363, in get_matching_files
    return get_matching_files_v2(filename)
  File "/usr/local/lib/python3.6/dist-packages/tensorflow_core/python/lib/io/file_io.py", line 384, in get_matching_files_v2
    compat.as_bytes(pattern))
tensorflow.python.framework.errors_impl.NotFoundError: /home/gpu_user/a1/faster_rcnn/Custom-Faster-RCNN-Using-Tensorfow-Object-Detection-API/CP; No such file or directory
```

The output detection images are stored in the specified folder and the crack classification results are saved in a csv file as crack category and extent values for each image. **(Please send us the results, including images and csv files, of the testing data you used in your thesis. Please also send the xlsx files generated by the CFE codes. You can put them in your drive and let us know which folders you put them.)**
