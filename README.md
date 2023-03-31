# YoloV5 installation on Jetson Xavier platforms 
I suggest to create your own virtual environment to deploy YoloV5, to do it you should follow steps below: <br>

1. Install virtualenv: 
```bash
  pip3 install virtualenv
``` 
2. Create your virtual environment (named <my_env_name>):
 ```bash
 virtualenv <my_env_name>
 ```
3. To activate you environment, just type:
  ```bash
 source <my_env_name>/bin/activate
 ```
4. If you want to quit the environment, simply type `deactivate`

<hr>

If you haven't done it yet, you should install `git` and `pip`:
```bash
sudo apt-get install git
```
```bash
sudo apt install python3-pip
```
then clone the YoloV5 repository:
```bash
git clone https://github.com/ultralytics/yolov5.git
 ```
Install the following feature:
```bash
pip3 install -U PyYAML==5.3.1
```
```bash
pip3 install tqdm
```
```bash
pip3 install cython 
```
```bash
pip3 install -U numpy==1.19.5
```
```bash
sudo apt install build-essential libssl-dev libffi-dev python3-dev
```
```bash
pip3 install cycler==0.10 
```
```bash
pip3 install kiwisolver==1.3.1 
```
```bash
pip3 install pyparsing==2.4.7 
```
```bash
pip3 install python-dateutil==2.8.2 
```
```bash
sudo apt install libfreetype6-dev 
```
```bash
pip3 install --no-deps matplotlib==3.2.2 
```
```bash
sudo apt install gfortran 
```
```bash
sudo apt install libopenblas-dev 
```
```bash
sudo apt install liblapack-dev 
```
```bash
pip3 install scipy==1.4.1 
```
```bash
sudo apt install libjpeg-dev 
```
```bash
pip3 install pillow==8.3.2 
```
```bash
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.9.0-cp36-cp36m-linux_aarch64.whl
```
```bash
pip3 install typing-extensions==3.10.0.2
```
```bash
pip3 install torch-1.9.0-cp36-cp36m-linux_aarch64.whl
```
Install torchivision (I've choosen the 0.9.0 version):
```bash
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
```
```bash
git clone --branch v0.9.0 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
```
```bash
cd torchvision
```
```bash
export BUILD_VERSION=0.9.0    
```
Then you have to set your `PYTHONPATH`:
```bash
export PYTHONPATH="/home/nvidia/.local/lib/python3.6/site-packages/"
```
```bash
python3 setup.py install --user
```
```bash
pip3 install --no-deps seaborn==0.11.0
```
Now you'll be able to execute your detection model.


