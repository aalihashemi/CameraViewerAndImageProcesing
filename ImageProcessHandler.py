
import numpy as np
#import matplotlib.pyplot as plt
import cv2 as cv
from ImageProcessing import ImageProcessing
from dataclasses import dataclass
from MACRO import *


class ImageProcessHandler():
    def __init__(self):
        
        self.init_filters()
        self.noisereduction_methods = 0
        
        self.raw_img : np.ndarray
        self.processed_img : np.ndarray

    def init_filters(self):

        self.filters_struct = FiltersStruct()
        self.filters_struct.is_grayscale.is_enabled = 1

        #filters array should be sorted based on filter priorities
        #self.filters = [self.is_grayscale, self.brightness, self.contrast, self.sharpness
        #                , self.exposure, self.rotation_deg, self.is_clahe]
        

    def run_filters(self, img : np.ndarray):
        self.raw_img = img #.copy()
        self.processed_img = img.copy()

        for filter in self.filters_struct.filters_dict.values():
            if filter.is_enabled:

                if filter == self.filters_struct.is_grayscale:
                    self.processed_img = ImageProcessing.set_grayscale(self.processed_img)
        
                if filter == self.filters_struct.brightness:
                    self.processed_img = ImageProcessing.set_brightness_level(
                        self.processed_img, filter.param_dict["VAL"])
        
                if filter == self.filters_struct.contrast:
                    self.processed_img = ImageProcessing.set_contrast_level(
                        self.processed_img, filter.param_dict["VAL"])
        
                if filter == self.filters_struct.sharpness:
                    self.processed_img = ImageProcessing.set_sharpness_level(
                        self.processed_img, filter.param_dict["VAL"])
        
                if filter == self.filters_struct.exposure:
                    self.processed_img = ImageProcessing.set_exposure_level(
                        self.processed_img, filter.param_dict["VAL"])
        
                if filter == self.filters_struct.rotation_deg:
                    self.processed_img = ImageProcessing.set_rotation_deg(
                        self.processed_img, filter.param_dict["VAL"])
        
                if filter == self.filters_struct.is_clahe:
                    self.processed_img = ImageProcessing.run_clahe(self.processed_img)


                if filter == self.filters_struct.median_filter :
                    self.processed_img = ImageProcessing.apply_median_filter(
                        self.processed_img, filter.param_dict["VAL"])

                if filter == self.filters_struct.avg_filter:
                    self.processed_img = ImageProcessing.apply_avg_filter(
                        self.processed_img, filter.param_dict["VAL"]
                    )

                # if filter == self.laplacian_filter:
                #     self.processed_img = ImageProcessing.add_laplacian_filter(
                #         self.processed_img, filter.param_dict["VAL"], 
                #     )

                #sigma parameter can be added
                if filter == self.filters_struct.adaptive_local_denoise:
                    self.processed_img = ImageProcessing.adaptive_local_denoise(
                        self.processed_img, filter.param_dict["VAL"]
                    )

                if filter == self.filters_struct.gaussian_blur :
                    self.processed_img = ImageProcessing.add_gaussian_blur(
                        self.processed_img, filter.param_dict["VAL"]
                    )

                if filter == self.filters_struct.bilateralFilter :
                    self.processed_img = ImageProcessing.set_bilateralFilter(
                        self.processed_img, filter.param_dict["VAL"]
                    )

                if filter == self.filters_struct.gaussian_lowpass:
                    self.processed_img = ImageProcessing.gaussian_lowpass(
                        self.processed_img, filter.param_dict["VAL"]
                    )

        return self.processed_img