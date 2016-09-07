# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coordinates_converter_dialog_base.ui'
#
# Created: Tue Aug 23 09:45:05 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt4 import QtGui, uic
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'coordinates_converter_dialog_base.ui'))


class CoordinatesConverterDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(CoordinatesConverterDialog, self).__init__(parent)
        self.setupUi(self)
        self.coordinate_fields = [self.lineEdit_mgrs, self.lineEdit_utm, self.lineEdit_wgs_dms,
                                  self.lineEdit_wgs_degrees, self.lineEdit_wgs_comma]
        self.lineEdit_input.setFocus()

    def reset(self):
        self.lineEdit_input.clear()
        self.clear_coordinate_fields()
        self.clear_epsg_fields()
        self.statusBar.showMessage('')

    def clear_coordinate_fields(self):
        for field in self.coordinate_fields:
            field.clear()

    def clear_epsg_fields(self):
        self.lineEdit_input_epsg.clear()
        self.lineEdit_epsg_result.clear()
