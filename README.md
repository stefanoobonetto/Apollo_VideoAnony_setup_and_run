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

8. nstall torchvision: let’s check that the torchvision version we want to install is compatible with the torch’s version (check at this link); in my case, torchvision v0.9.0 is compatible:
```bash
  wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.8.0-cp36-cp36m-linux_aarch64.whl
  pip3 install torch-1.8.0-cp36-cp36m-linux_aarch64.whl
```

git clone --branch v0.9.0 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.9.0 #instead of 0.9.0, put the version you need
python3 setup.py install --user
cd ..





