import numpy as np
#import matplotlib.pyplot as plt
import cv2 as cv


class ImageProcessing():
    
    def __init__(self):
        pass

    @staticmethod
    def run_clahe(img):
        if (len(img.shape) >= 3):
            #raise 'image is not grayscale'
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equalized = clahe.apply(img)
        return equalized
    
    @staticmethod
    def set_contrast_level(img, val):
        # new_image = np.zeros(img.shape, img.dtype)
        # new_image = np.clip(img * val, 0, 255)
        new_image = cv.convertScaleAbs(img, alpha=val)
        return new_image
    
    @staticmethod
    def set_exposure_level(img, val):
        # build a lookup table mapping the pixel values [0, 255] to
	    # their adjusted gamma values
        invGamma = 1.0 / val
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        #print ('val in func: ', val)
        return cv.LUT(img, table)

    @staticmethod
    def set_sharpness_level(img, val):
        pass
    
    @staticmethod
    def set_brightness_level(img, val):
        # new_image = np.zeros(img.shape, img.dtype)
        # new_image = np.clip(img + val, 0, 255)
        new_image = cv.convertScaleAbs(img, beta=val)
        return new_image
    
    @staticmethod
    def set_rotation_deg(img, val):
        pass

    @staticmethod
    def set_grayscale(img):
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    @staticmethod
    def set_colored(img):
        pass
    
    @staticmethod
    def apply_median_filter(img, kernelSize):
        return cv.medianBlur(img, kernelSize) 
    
    @staticmethod
    def apply_avg_filter(img, kernelSize):
        return  cv.blur(img,(kernelSize,kernelSize))
    
    @staticmethod
    def add_laplacian_filter(img, kernelSize, coeff):
        laplacianed_mask = cv.Laplacian(img, cv.CV_64F, ksize=kernelSize)
        out1 = np.int32(1*img  - coeff * laplacianed_mask)
        out1 [out1 > 255] = 255
        out1 [out1 < 0] = 0
        return
    
    @staticmethod
    def adaptive_local_denoise(image, kernel_size=7, sigma_eta=1):
        kernel = np.ones([kernel_size, kernel_size])
        epsilon = 1e-8
        height, width = image.shape[:2]
        m, n = kernel.shape[:2]
        padding_h = int((m -1)/2)
        padding_w = int((n -1)/2)
        image_pad = np.pad(image, ((padding_h, m - 1 - padding_h), \
            (padding_w, n - 1 - padding_w)), mode="edge")
        img_result = np.zeros(image.shape)
        for i in range(height):
            for j in range(width):
                block = image_pad[i:i + m, j:j + n]
                gxy = image[i, j]
                z_sxy = np.mean(block)
                sigma_sxy = np.var(block)
                rate = (sigma_eta / (sigma_sxy + epsilon))**2
                if rate >= 1:
                    rate = 1
                img_result[i, j] = gxy - rate * (gxy - z_sxy)
        img_result = img_result.astype('uint8')
        return img_result

    
    @staticmethod
    def add_gaussian_blur(img, kernel_size=7):
        return cv.GaussianBlur(img, (kernel_size, kernel_size), 0)

    @staticmethod
    def set_bilateralFilter(img, param):
        #return cv.bilateralFilter(img,9,75,75)
        return cv.bilateralFilter(img,5,75,75)

    @staticmethod
    def gaussian_lowpass(img, cutoff_freq):
        row_size, column_size = img.shape
        tmp = np.zeros((row_size, column_size))
        for i in range(row_size):
            for j in range(column_size):
                tmp[i, j] = np.exp(-1 * np.sqrt((i - row_size//2)**2 + (j - column_size//2)**2)**2 / (2 * cutoff_freq ** 2))
     
        img_padding = [0,0,0]
        padded_img = cv.copyMakeBorder(img, row_size//2, row_size//2, column_size//2, column_size//2, cv.BORDER_CONSTANT, value=img_padding)
        padded_rows, padded_columns = padded_img.shape

        img_fft = np.fft.fftshift(np.fft.fft2(padded_img)) 
        highpass_filter = tmp
        filtered_img = np.fft.ifftshift(img_fft * highpass_filter)
        filtered_img = np.fft.ifft2(filtered_img)
        filtered_img = filtered_img[padded_rows//4:padded_rows*3//4,padded_columns//4:padded_columns*3//4]

        return np.abs(filtered_img)
    