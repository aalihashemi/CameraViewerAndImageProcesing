CURRENT_CAMERA = 1 # 0: webcam , 1:rpi cam
WEBCAM_ID = 0
RPI_CAM_ID = 1

#### Filters Parameters - Default Values ####
MEDIAN_FILTER_DEFAULT_KERNEL_SIZE = 3
AVG_FILTER_DEFAULT_KERNEL_SIZE = 3
ADAPTIVE_DENOISE_FILTER_DEFAULT_KERNEL_SIZE = 7

CAMER_MOTORS_DEFAULT_I2C_BUS = 1


class ImageFilter():
    def __init__(self, is_enable=0, val=0, periority=0):
        self.is_enabled = is_enable
        self.param_dict = {"VAL":val}
        self.periority = periority
    def add_param(self, param_name, val):
        self.param_dict.update({param_name:val})


class FiltersStruct():  
    def __init__(self) :
            
        #can be more clean (sorting based on priorities)
        self.is_grayscale = ImageFilter(0, 0, periority=0)
        self.brightness = ImageFilter(0, 0, periority=1)
        self.contrast = ImageFilter(0, 0, periority=2)
        self.sharpness = ImageFilter(0, 0, periority=3)
        self.exposure = ImageFilter(0, 1, periority=4)
        self.rotation_deg = ImageFilter(0, 0, periority=5)
        self.is_clahe = ImageFilter(0, 0, periority=6)
        
        self.median_filter = ImageFilter(0, 0, periority=6) #(img, kernelSize):
        self.avg_filter = ImageFilter(0, 0, periority=6) #(img, kernelSize):
        self.laplacian_filter = ImageFilter(0, 0, periority=6) #(img, kernelSize, coeff):
        self.adaptive_local_denoise = ImageFilter(0, 0, periority=6) #(image, kernel, sigma_eta=1):
        self.gaussian_blur = ImageFilter(0, 0, periority=6) #(img, kernel_size=7):
        self.bilateralFilter = ImageFilter(0, 0, periority=6) #(img):
        self.gaussian_lowpass = ImageFilter(0, 0, periority=6) #(img, row_size, column_size, cutoff_freq):

        self.filters_dict = self.__dict__.copy()
        #del self.filters_dict['filters_dict']