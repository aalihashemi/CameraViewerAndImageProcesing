
from ui_mainwindow import Ui_MainWindow
from enum import Enum
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

from ImageProcessing import ImageProcessing
from LiveCameraImage import *
from CameraSetting import *
from MACRO import *


class mainwindow(QMainWindow):
    setting_changed_sig = pyqtSignal(FiltersStruct)
    
    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        self.uiInitialize()

        #self.image_processor = ImageProcessing()

        self.disply_width = 1280
        self.display_height = 960
        self.LiveImageThread = LiveCameraImage()
        #self.LiveImageThread.set_image_processor_obj(self.image_processor)
        self.currentFrame : QPixmap

        self.camera_setting_handler = CameraHandler(CAMER_MOTORS_DEFAULT_I2C_BUS)

        # connect its signal to the update_image slot
        self.LiveImageThread.change_pixmap_signal.connect(self.update_image)
        
        self.setting_changed_sig.connect(self.LiveImageThread.set_filters_params)
        self.image_filters_entered_params = FiltersStruct()

        # start the thread
        self.LiveImageThread.start()
        self.ui.settingTabWidget.hide()
        self.ui.closeSettingBtn.hide()
        
    def uiInitialize(self):
        self.setup_ui_connection()
        #self.ui.groupBox_3.setEnabled(False)
        #self.ui.groupBox_2.setEnabled(False)

    def setup_ui_connection(self):
        self.set_radio_btns_connection()
        self.set_lineEdits_connection()
        self.set_manual_btns_connection()
        self.set_comboBoxs_connection()
        self.set_sliders_connection()
        self.set_checkBoxs_connection()
    
    def set_lineEdits_connection(self):
        pass #self.ui.velocityInput.textChanged.connect(lambda text: self.on_velocity_input_change(text))
        
    def set_manual_btns_connection(self):
        self.ui.settingBtn.clicked.connect(self.on_settingBtn_clicked)
        self.ui.captureBtn.clicked.connect(self.on_captureBtn_clicked)
        self.ui.saveAsBtn.clicked.connect(self.on_saveAsBtn_clicked)
        self.ui.closeSettingBtn.clicked.connect(self.on_closeSettingBtn_clicked)

    def set_radio_btns_connection(self):
        pass #self.ui.MoveForDuration.clicked.connect(lambda: self.on_radio_btn_clicked(Mode.MOVE_IN_DURATION))
    
    def set_sliders_connection(self):
        self.ui.brightnessSlider.valueChanged.connect(self.on_brightnessSlider_changed)
        self.ui.exposureSlider.valueChanged.connect(self.on_exposureSlider_changed)
        self.ui.contrastSlider.valueChanged.connect(self.on_contrastSlider_changed)
        self.ui.focusSlider.valueChanged.connect(self.on_focusSlider_changed)
        self.ui.zoomSlider.valueChanged.connect(self.on_zoomSlider_changed)

    def set_comboBoxs_connection(self):
        pass
    
    def set_checkBoxs_connection(self):
        self.ui.medianFiltCheckBox.stateChanged.connect(self.on_medianCheckBox_toggled)
        self.ui.claheCheckBox.stateChanged.connect(self.on_claheCheckBox_toggled)
        self.ui.blurCheckBox.stateChanged.connect(self.on_blurCheckBox_toggled)
        self.ui.adaptiveDenoiseCheckBox.stateChanged.connect(self.on_adaptiveDenoiseFiltCheckBox_toggled)
        self.ui.bilateralFiltCheckBox.stateChanged.connect(self.on_bilateralFiltCheckBox_togggled)

    def closeEvent(self, event):
        self.LiveImageThread.stop()
        event.accept()

    def send_image_filters_params(self):
        self.setting_changed_sig.emit(self.image_filters_entered_params)
        #pass
    
    

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.currentFrame = self.convert_cv_qt(cv_img)
        self.ui.liveImageLabel.setPixmap(self.currentFrame)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p) #(p)


    ##################  UI Components Slots  #################

    #ComboBoxs:
    def on_autoGainCombo_changed(self):
        pass
    def on_claheCombo_changed(self):
        pass
    def on_noiseReductionCombo_changed(self):
        pass
    def on_grayscaleCombo_changed(self):
        pass
    
    #LineEdits:
    def on_camGainLineEdit_textChanged(self):
        pass
    def on_camFocusLineEdit_textChanged(self):
        pass
    def on_camZoomLineEdit_textChanged(self):
        pass

    #Buttons:
    def on_settingBtn_clicked(self):
        if (self.ui.settingTabWidget.isHidden()):
            self.ui.settingTabWidget.show()
            self.ui.closeSettingBtn.show()
            self.ui.gridLayout.setColumnStretch(1, 1)
            self.ui.gridLayout.setColumnStretch(2, 2)
            self.ui.gridLayout.setColumnStretch(3, 2)
        else:
            self.ui.settingTabWidget.hide()
            self.ui.closeSettingBtn.hide()

    def on_closeSettingBtn_clicked(self):    
        self.ui.settingTabWidget.hide()
        self.ui.closeSettingBtn.hide()

    def on_captureBtn_clicked(self):
        self.ui.steadyImageLabel.setPixmap(self.currentFrame)
    def on_saveAsBtn_clicked(self):
        pass
    
    #Sliders:
    def on_contrastSlider_changed(self):
        val = (self.ui.contrastSlider.value()+200) / 100.0
        if val != 0:
            self.image_filters_entered_params.contrast.is_enabled = 1
        else: 
            self.image_filters_entered_params.contrast.is_enabled = 0
        self.image_filters_entered_params.contrast.param_dict["VAL"] = val
        self.send_image_filters_params()

    def on_brightnessSlider_changed(self):
        val = self.ui.brightnessSlider.value()
        if val != 0:
            self.image_filters_entered_params.brightness.is_enabled = 1
        else: 
            self.image_filters_entered_params.brightness.is_enabled = 0
        self.image_filters_entered_params.brightness.param_dict["VAL"] = val # self.ui.brightnessSlider.value()
        self.send_image_filters_params()

    def on_sharpnessSlider_changed(self):
        pass

    def on_exposureSlider_changed(self):
        val = self.ui.exposureSlider.value() / 100.0
        if val != 0:
            self.image_filters_entered_params.exposure.is_enabled = 1
        else: 
            self.image_filters_entered_params.exposure.is_enabled = 0
        self.image_filters_entered_params.exposure.param_dict["VAL"] = val
        self.send_image_filters_params()

    def on_rotationSlider_changed(self):
        pass
    
    def on_focusSlider_changed(self):
        self.camera_setting_handler.setFocusValue(self.ui.focusSlider.value())
    def on_zoomSlider_changed(self):
        self.camera_setting_handler.setZoomValue(self.ui.zoomSlider.value())
    
    def on_grayscaleCheckBox_toggled(self):
        val = self.ui.grayscaleCheckBox.isChecked()
        if val != 0:
            self.image_filters_entered_params.is_grayscale.is_enabled = 1
        else: 
            self.image_filters_entered_params.is_grayscale.is_enabled = 0
        #self.image_filters_entered_params.median_filter.param_dict["VAL"] = 
        self.send_image_filters_params()

    def on_medianCheckBox_toggled(self):
        val = self.ui.medianFiltCheckBox.isChecked()
        if val != 0:
            self.image_filters_entered_params.median_filter.is_enabled = 1
        else: 
            self.image_filters_entered_params.median_filter.is_enabled = 0
        self.image_filters_entered_params.median_filter.param_dict["VAL"] = MEDIAN_FILTER_DEFAULT_KERNEL_SIZE
        self.send_image_filters_params()
    
    def on_claheCheckBox_toggled(self):
        val = self.ui.claheCheckBox.isChecked()
        if val != 0:
            self.image_filters_entered_params.is_clahe.is_enabled = 1
        else: 
            self.image_filters_entered_params.is_clahe.is_enabled = 0
        #self.image_filters_entered_params.median_filter.param_dict["VAL"] = 
        self.send_image_filters_params()

    def on_blurCheckBox_toggled(self):
        val = self.ui.blurCheckBox.isChecked()
        if val != 0:
            self.image_filters_entered_params.avg_filter.is_enabled = 1
        else: 
            self.image_filters_entered_params.avg_filter.is_enabled = 0
        self.image_filters_entered_params.avg_filter.param_dict["VAL"] = AVG_FILTER_DEFAULT_KERNEL_SIZE
        self.send_image_filters_params()
        
    def on_adaptiveDenoiseFiltCheckBox_toggled(self):
        val = self.ui.adaptiveDenoiseCheckBox.isChecked()
        if val != 0:
            self.image_filters_entered_params.adaptive_local_denoise.is_enabled = 1
        else: 
            self.image_filters_entered_params.adaptive_local_denoise.is_enabled = 0
        self.image_filters_entered_params.adaptive_local_denoise.param_dict["VAL"] = ADAPTIVE_DENOISE_FILTER_DEFAULT_KERNEL_SIZE
        self.send_image_filters_params()

    def on_bilateralFiltCheckBox_togggled(self):
        val = self.ui.bilateralFiltCheckBox.isChecked()
        if val != 0:
            self.image_filters_entered_params.bilateralFilter.is_enabled = 1
        else: 
            self.image_filters_entered_params.bilateralFilter.is_enabled = 0
        self.image_filters_entered_params.bilateralFilter.param_dict["VAL"] = 0
        self.send_image_filters_params()

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = mainwindow()
    a.showMaximized()
    sys.exit(app.exec_())
