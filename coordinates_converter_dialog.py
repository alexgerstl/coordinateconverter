# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coordinates_converter_dialog_de_2.ui'
#
# Created: Tue Aug 23 09:45:05 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt4 import QtCore

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'coordinates_converter_dialog_de_2.ui'))


class CoordinatesConverterDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(CoordinatesConverterDialog, self).__init__(parent)
        self.setupUi(self)

        # Output fields for converted coordinates
        self.coordinate_fields = [self.lineEdit_mgrs, self.lineEdit_utm, self.lineEdit_wgs_dms,
                                  self.lineEdit_wgs_degrees, self.lineEdit_wgs_comma]

        # Input fields for geographic coordinate format
        self.lat_deg_input = QLineEdit()
        self.lat_min_input = QLineEdit()
        self.lat_sec_input = QLineEdit()
        self.long_deg_input = QLineEdit()
        self.long_min_input = QLineEdit()
        self.long_sec_input = QLineEdit()

        # Input fields for utm coordinate format
        self.utm_zone_input = QLineEdit()
        self.hemisphere = QComboBox()
        self.hemisphere.addItem('N')
        self.hemisphere.addItem('S')
        self.utm_easting_input = QLineEdit()
        self.utm_northing_input = QLineEdit()

        # Input fields for mgrs coordinate format
        self.mgrs_zone_input = QLineEdit()
        self.mgrs_square_input = QLineEdit()
        self.mgrs_easting_input = QLineEdit()
        self.mgrs_northing_input = QLineEdit()

        self.comboBox_format.setCurrentIndex(0)
        self.hemisphere.setCurrentIndex(1)
        self.input_fields = [self.lat_deg_input, self.lat_min_input, self.lat_sec_input, self.long_deg_input,
                             self.long_min_input, self.long_sec_input, self.utm_zone_input, self.utm_easting_input,
                             self.utm_northing_input, self.mgrs_zone_input, self.mgrs_square_input,
                             self.mgrs_easting_input, self.mgrs_northing_input]

    def reset(self):
        """Resets the graphical user interface."""
        self.clear_coordinate_fields()
        self.clear_epsg_fields()
        self.statusBar.clearMessage()
        self.clear_format_layout()
        self.comboBox_format.setCurrentIndex(0)
        self.hemisphere.setCurrentIndex(0)
        self.label_input_convert.setText('')
        self.label_utm_ref.setText('MGRS')

    def clear_coordinate_fields(self):
        """Resets the text fields show the converted coordinates."""
        for field in self.coordinate_fields:
            field.clear()

    def clear_input_fields(self):
        """Resets the value input fields for the different coordinate systems."""
        for field in self.input_fields:
            field.clear()

    def clear_epsg_fields(self):
        """Resets the input field and the text field showing the result for transforming values based on EPSG codes."""
        self.lineEdit_input_epsg.clear()
        self.lineEdit_epsg_result.clear()

    def create_degrees_input(self):
        """Creates the template for entering coordinates in the geographic coordinate system - DEGREES."""
        self.gridLayout_input.addWidget(self.long_deg_input, 0, 0)
        self.gridLayout_input.addWidget(QLabel('\xb0'), 0, 1)
        self.gridLayout_input.addWidget(QLabel('E'), 0, 2)
        self.gridLayout_input.addWidget(self.lat_deg_input, 0, 3)
        self.gridLayout_input.addWidget(QLabel('\xb0'), 0, 4)
        self.gridLayout_input.addWidget(QLabel('N'), 0, 5)

    def create_dms_input(self):
        """Creates the template for entering coordinates in the geographic coordinate system - DEGREES, MINUTES, SECONDS."""
        self.gridLayout_input.addWidget(self.long_deg_input, 0, 0)
        self.gridLayout_input.addWidget(QLabel('\xb0'), 0, 1)
        self.gridLayout_input.addWidget(self.long_min_input, 0, 2)
        self.gridLayout_input.addWidget(QLabel('\''), 0, 3)
        self.gridLayout_input.addWidget(self.long_sec_input, 0, 4)
        self.gridLayout_input.addWidget(QLabel('"'), 0, 5)
        self.gridLayout_input.addWidget(QLabel('E'), 0, 6)
        self.gridLayout_input.addWidget(self.lat_deg_input, 0, 7)
        self.gridLayout_input.addWidget(QLabel('\xb0'), 0, 8)
        self.gridLayout_input.addWidget(self.lat_min_input, 0, 9)
        self.gridLayout_input.addWidget(QLabel('\''), 0, 10)
        self.gridLayout_input.addWidget(self.lat_sec_input, 0, 11)
        self.gridLayout_input.addWidget(QLabel('"'), 0, 12)
        self.gridLayout_input.addWidget(QLabel('N'), 0, 13)

    def create_commaminutes_input(self):
        """Creates the template for entering coordinates in the geographic coordinate system - DEGREES, DECIMAL MINUTES."""
        self.gridLayout_input.addWidget(self.long_deg_input, 0, 0)
        self.gridLayout_input.addWidget(QLabel('\xb0'), 0, 1)
        self.gridLayout_input.addWidget(self.long_min_input, 0, 2)
        self.gridLayout_input.addWidget(QLabel('\''), 0, 3)
        self.gridLayout_input.addWidget(QLabel('E'), 0, 4)
        self.gridLayout_input.addWidget(self.lat_deg_input, 0, 7)
        self.gridLayout_input.addWidget(QLabel('\xb0'), 0, 8)
        self.gridLayout_input.addWidget(self.lat_min_input, 0, 9)
        self.gridLayout_input.addWidget(QLabel('\''), 0, 10)
        self.gridLayout_input.addWidget(QLabel('N'), 0, 11)

    def create_utm_input(self):
        """Creates the template for entering coordinates in the unversial mercator transverse coordinate system - UTM."""
        self.utm_zone_input.setFixedWidth(30)
        self.gridLayout_input.addWidget(self.utm_zone_input, 0, 0)
        self.gridLayout_input.addWidget(QLabel('Zone'), 0, 1)
        self.gridLayout_input.addWidget(self.hemisphere, 0, 2)
        self.gridLayout_input.addWidget(self.utm_easting_input, 0, 3)
        self.gridLayout_input.addWidget(QLabel('E'), 0, 4)
        self.gridLayout_input.addWidget(self.utm_northing_input, 0, 5)
        self.gridLayout_input.addWidget(QLabel('N'), 0, 6)

    def create_mgrs_input(self):
        """Creates the template for entering coordinates in the military grid reference coordinate system - MGRS."""
        self.mgrs_zone_input.setFixedWidth(40)
        self.mgrs_square_input.setFixedWidth(30)

        self.gridLayout_input.addWidget(self.mgrs_zone_input, 0, 0)
        self.gridLayout_input.addWidget(QLabel('Zone'), 0, 1)
        self.gridLayout_input.addWidget(self.mgrs_square_input, 0, 2)
        self.gridLayout_input.addWidget(QLabel('Gitterquadrat'), 0, 3)
        self.gridLayout_input.addWidget(self.mgrs_easting_input, 0, 4)
        self.gridLayout_input.addWidget(QLabel('E'), 0, 5)
        self.gridLayout_input.addWidget(self.mgrs_northing_input, 0, 6)
        self.gridLayout_input.addWidget(QLabel('N'), 0, 7)

    def clear_format_layout(self):
        """Removes all template elements from the gridlayout."""
        for i in reversed(range(self.gridLayout_input.count())):
            self.gridLayout_input.itemAt(i).widget().setParent(None)
        self.clear_input_fields()
        self.label_utm_ref.setText('MGRS')

