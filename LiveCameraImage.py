import sys
import cv2 as cv
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

from ImageProcessing import ImageProcessing
from ImageProcessHandler import ImageProcessHandler
from MACRO import *

#if (CURRENT_CAMERA == RPI_CAM_ID):
from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder



# Camera Show Thread
class LiveCameraImage(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.new_frame: np.ndarray
        self.new_processed_img : np.ndarray
        
        self.image_prcessor = ImageProcessHandler()
        #self.image_receiver = Picamera2()
        #self.image_receiver.configure(self.image_receiver.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 960)}))
        #self.image_receiver.start()
        #self.setup_camera()

    def setup_camera(self):
        if (CURRENT_CAMERA == RPI_CAM_ID):
            self.image_receiver = Picamera2()
            self.image_receiver.configure(self.image_receiver.create_preview_configuration(main={"format": 'XRGB8888', "size": (800, 600)}))
            self.image_receiver.start()

        elif (CURRENT_CAMERA == WEBCAM_ID):
            self.image_receiver =cv.VideoCapture(0)
    
    def shutdown_camera(self):
        if (CURRENT_CAMERA == RPI_CAM_ID):
            pass
        elif (CURRENT_CAMERA == WEBCAM_ID):
            self.image_receiver.release()

    def set_image_processor_obj(self, obj):
        self.image_prcessor = obj
        
    def get_new_frame_picam(self):
        return self.image_receiver.capture_array()

    # capture from web cam
    def get_new_frame_webcam(self):
        return self.image_receiver.read()[1]
    
    def get_new_frame(self):
        if (CURRENT_CAMERA == RPI_CAM_ID):
            return self.get_new_frame_picam()
        elif (CURRENT_CAMERA == WEBCAM_ID):
            return self.get_new_frame_webcam()

    @pyqtSlot(FiltersStruct)
    def set_filters_params(self, params_struct):       
        self.image_prcessor.filters_struct = params_struct
        print ('change val to: ', self.image_prcessor.filters_struct.exposure.param_dict["VAL"])

    def run(self):
        #cap = picam2.capture_array()
        
        self.setup_camera()

        while self._run_flag:
            #cv_img = self.image_receiver.capture_array() #cap.read()
            self.new_frame = self.get_new_frame() #get_new_frame_webcam()
            self.new_processed_img = self.image_prcessor.run_filters(self.new_frame)
            #test below code and compare the speed with previous line 
            #self.new_processed_img = self.image_prcessor.processed_img
            #
            #
            self.change_pixmap_signal.emit(self.new_processed_img)
            

            QThread.msleep(1)

        # shut down capture system
        #cap.release()
        self.shutdown_camera()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()