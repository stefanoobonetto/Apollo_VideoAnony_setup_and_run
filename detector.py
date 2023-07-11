import torch
import cv2
import numpy as np
from datasets.dataset import letterbox
import onnxruntime as ort
import time

from utils.general import check_img_size, non_max_suppression, scale_coords, xywh2xyxy, xyxy2xywh


class Detector(object):
    def __init__(self, opt, model_path, imgsz, device):
        print("Creating model...")
        self.opt = opt
        
        self.device = device
        self.model_sess = ort.InferenceSession(model_path, providers=[('TensorrtExecutionProvider', 
                                                                       {'trt_engine_cache_enable': True, 
                                                                        'trt_engine_cache_path': 'engine_cache', 
                                                                        "trt_fp16_enable": True, 
                                                                        'device_id': 0, }), ]) # providers=['CUDAExecutionProvider')])#
        self.input_name = self.model_sess.get_inputs()[0].name

        self.stride = 64
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        print(self.imgsz)

    def pre_process(self, im0s):
        im = cv2.resize(im0s, (1280, 960), interpolation=cv2.INTER_NEAREST)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        im = im.transpose((2, 0, 1)).astype(np.float32)/255.0  # HWC to CHW, BGR to RGB
        return im[None] 

    def post_process(self, pred, classes):
        # NMS
        pred = torch.tensor(pred)
        pred = non_max_suppression(pred, classes=classes)
        return pred

    def process_im(self, im0, classes):
        im=im0
        pred = self.model_sess.run(None, {self.input_name: im})[0]
        pred = self.post_process(pred, classes)
        # Process predictions
        for i, det in enumerate(pred):  # per image                
            if len(det):
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

        return pred

    def cls2label(self, cls):
        c = int(cls)  # integer class
        label = self.model.names[c]
        return label

