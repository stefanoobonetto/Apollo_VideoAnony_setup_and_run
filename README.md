# Apollo Setup (NVIDIA Jetson Xavier NX)

## pyTorch and OpenCV installation

The installation requires an Nvidia Jetson Xavier device using Python 3.7 (it works also in a 3.69 Python env, but YOLOv5 requires a Python 3.7 environment).

1. Update the system
```bash
  sudo apt-get update
``` 

2. Install basic dependencies needed for YOLOv5
```bash
sudo apt-get install python3-pip python3-dev
sudo apt-get install python3-matplotlib
sudo apt-get install libopenblas-base libopenmpi-dev
pip3 install Cython
pip3 install numpy==1.19.4
pip3 install scipy scikit-build tqdm
pip3 install pillow seaborn pyyaml ffmpeg-python
sudo apt-get install git
```
  Pay attention to numpy version, it has to be 1.19.4, the 1.19.5 is buggy (ingore any dependencies’ ERRORS). Some commands may take a while, don’t worry about it.

3. Open your /.bashrc file:
```bash
sudo gedit ~/.bashrc
```
  and append to the bottom of the file the following lines:
```bash
export PKG_CONFIG_PATH='/usr/lib/aarch64-linux-gnu/pkgconfig'
export OPENBLAS_CORETYPE=ARMV8
export OMP_NUM_THREADS=1
```

and if there isn’t yet, add this to the PATH env. variable in the .bashrc file:
```bash
PATH=directory:another_directory:/usr/local/cuda-10.2/bin
```

4. Install OpenCV dependencies:
```bash
sudo apt-get install build-essential cmake unzip pkg-config
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev
sudo apt-get install libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
```

5. To install OpenCV, let’s clone the repo:
```bash
git clone https://github.com/opencv/opencv.git
cd /opencv
git checkout 4.5.4
```
  then create a build folder and build OpenCV:
```bash
mkdir /opencv/build
cd /opencv/build

sudo ln -s /opt/conda/lib/python3.8/site-packages/numpy/core/include/numpy/usr/include/numpy

sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D PYTHON_EXECUTABLE=$(which python) \
-D BUILD_opencv_python2=OFF \
-D CMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
-D PYTHON3_EXECUTABLE=$(which python3) \
-D PYTHON3_INCLUDE_DIR=$(python -c "from distutils.sysconfig \
import get_python_inc; print(get_python_inc())") \
-D PYTHON3_PACKAGES_PATH=$(python -c "from distutils.sysconfig \
import get_python_lib; print(get_python_lib())") \
-D WITH_FFMPEG=ON \
-D WITH_GSTREAMER=ON \
-D BUILD_EXAMPLES=ON ..
```  
and finally:
```bash
sudo make -j$(nproc)
```
  the installation of OpenCV may take from 5 mins to 2 hours, don’t worry (the process seems to be blocked in some phases, but it’s not, it’s just very very slow).

6. Now we can install OpenCV:
```bash
sudo make install
sudo ldconfig
```

7. Let’s install PyTorch: At [this link](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048) you can find all the pip wheel files versions provided by NVIDIA, I’ll use ’PyTorch v1.8.0 ’ but you have to check your Jetpack version. The sintax is basically this:
```bash
wget <link> -O <file_name>
pip3 install <file_name>
```

right click over the name of the file and copy link to get the <link>; since I want to install PyTorch v1.8.0, my command will be:
```bash
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.8.0-cp36-cp36m-linux_aarch64.whl
pip3 install torch-1.8.0-cp36-cp36m-linux_aarch64.whl
```

8. Install torchvision: let’s check that the torchvision version we want to install is compatible with the torch’s version (check at this link); in my case, torchvision v0.9.0 is compatible:
```bash
git clone --branch v0.9.0 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.9.0 #instead of 0.9.0, put the version you need
python3 setup.py install --user
cd ..
```

##YOLOv5 installation

Finally we can install YOLOv5 from github:
```bash
sudo apt-get update
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
```


then you need to change some stuff in the requirements.txt:
```bash
gitpython>=3.1.3 #remove the 0
...
setuptools>=59.6.0
```

and finally install it:
```bash
pip3 install -r requirements.txt
```
This will be enough to let your YOLOv5 model works check it:
```bash
cd yolov5/
python detect.py --weights yolov5s.pt --source  0 #webcam
                                                img.jpg
                                                vid.mp4
                                                screen
                                                path/
                                                list.txt
                                                list.streams
                                                'path/*.jpg'
                                                'https://youtu.be/Zgi9g1ksQHc'
                                                'rtsp://example.com/media.mp4'
```

and have a look at the results saved in runs/detect.

## VideoAnony Setup

We need a Python ≥ 3.6 environment.

1. First of all, if we haven’t done it already, we need to [generate a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
2. Once we’ve done it, we have to [add it to our GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?tool=webui).
3. Now we can clone the git repository (just if we’re allowed to by repo’s admin):
```bash
git clone git@github.com:luca-zanella-dvl/marvel-videoanony.git
cd marvel-video-anonymization
```
It’s recommended to use a virtual environment:
```bash
conda create --name marvel-video-anonymization python=3.9
conda activate marvel-video-anonymization
```
4. Finally we can install all the requirements:
```bash
pip3 install -r requirements.txt
```
5. We need to create a new folder for the weights of our model:
```bash
mkdir weights
```
then download [these weights](https://drive.google.com/drive/folders/1aexr_pfUcWkOq09g1LUqAw1DwIjPN05M?usp=sharing) and save them under the weights folder.
6. If we want to run the anonymization script locally, we need to open the src/anonymize.py with an editor and comment the following lines:
```bash
vid_writer[i] = cv2.VideoWriter(
gstreamer_pipeline_out(dataset.streams[i]),
cv2.CAP_GSTREAMER,
0,
fps,
(w, h),
True,
)
```
and uncomment the following:
```bash
vid_writer[i] = cv2.VideoWriter(
save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)
)
```
7. Finally we can run the anonymization script:
```bash
python3 src/anonymize.py --source data/videos/MOT17-03_first5s.mp4 --vstream-uri ""
```
If we want to choose the specifical weights, we can add these following arguments:
```bash
--head-model weights/<weights1> --lpd-model weights/<weights2>
```
where <weights1> are the weights used for the face recognition and <weights2> are the ones used for the license plate recognition.


## Usage with TensorRT
To improve the speed of the model's inference, we can use TensorRT.

You need to install it and install onnxruntime.

Then you can simply download [this anonymize.py file](https://github.com/stefanoobonetto/JetsonXavier_YoloV5_installation/blob/main/anonymize.py) and [this detector.py](https://github.com/stefanoobonetto/JetsonXavier_YoloV5_installation/blob/main/detector.py), which are the version adapted to the usage off TensorRT, and then replace the original anonymize.py and detector.py file 

<i>N.B. this is bad code, I haven't much time to make it better, but it works :).</i>

You have also to change the weights of your model, here we have two choices:

- weights[1280x960], the original dimension of the model. You can download these weights [from there](https://drive.google.com/drive/folders/15FXjoMjNsjRVxEeLoktylUMUJk0riYay?usp=sharing)
- weights[960x720], there is a resize phase, the model is faster. You can download these weights [from there](https://drive.google.com/drive/folders/1JMMoLBsqJWAtxN3WutxzGAssgo0msArb?usp=sharing), if you choose this version, you also have to change the 29th line of the detector.py:
```python
im = cv2.resize(im0s, (1280, 960), interpolation=cv2.INTER_NEAREST)
```

In both cases, replace the old weights folder with the new one.







