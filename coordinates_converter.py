# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordinatesConverter
                                 A QGIS plugin
 konvertiert Koordinaten
                              -------------------
        begin                : 2016-08-23
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Alexander Gerstl
        email                : alex.gerstl@gmx.at
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py


import resources
# Import the code for the dialog
from coordinates_converter_dialog import CoordinatesConverterDialog
from ensurer import CoordinateSystemString, Hemisphere
import converter
from converter1 import Converter
import os.path
import points
import exceptions
import collections

from ensurer import Ensurer


class CoordinatesConverter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface

        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CoordinatesConverter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = CoordinatesConverterDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Koordinaten konvertieren')
        self.toolbar = self.iface.addToolBar(u'CoordinatesConverter')
        self.toolbar.setObjectName(u'CoordinatesConverter')

        self.coordinates = {}
        self.selected_format = 0
        self.selected_hemisphere = 0
        self.long_deg = 0
        self.long_min = 0
        self.long_sec = 0
        self.lat_deg = 0
        self.lat_min = 0
        self.lat_sec = 0
        self.utm_zone_number = 0
        self.utm_zone_letter = Hemisphere.NORTH
        self.utm_easting = 0
        self.utm_northing = 0
        self.hemisphere = ''
        self.epsg_code_description = {}
        self.converter = Converter()
        self.ensurer = Ensurer()
        self.__load_epsg_codes()
        self.__load_epsg_codes_to_boxes()
        self.dlg.long_deg_input.textEdited.connect(self.__validate_WGS)
        self.dlg.long_min_input.textEdited.connect(self.__validate_WGS)
        self.dlg.long_sec_input.textEdited.connect(self.__validate_WGS)
        self.dlg.lat_deg_input.textEdited.connect(self.__validate_WGS)
        self.dlg.lat_min_input.textEdited.connect(self.__validate_WGS)
        self.dlg.lat_sec_input.textEdited.connect(self.__validate_WGS)
        self.dlg.zone_input.textEdited.connect(self.__validate_UTM)
        #self.dlg.square_input.textEdited.connect(self.__validate_input_value)
        self.dlg.easting_input.textEdited.connect(self.__validate_UTM)
        self.dlg.northing_input.textEdited.connect(self.__validate_UTM)
        #self.dlg.lineEdit_input.textEdited.connect(self.parse)
        self.dlg.comboBox_format.currentIndexChanged.connect(self.__change_format)
        self.dlg.hemisphere.currentIndexChanged.connect(self.__change_hemisphere)
        self.dlg.comboBox_from.currentIndexChanged.connect(self.__show_description_from)
        self.dlg.comboBox_to.currentIndexChanged.connect(self.__show_description_to)
        #self.dlg.lineEdit_input_epsg.textEdited.connect(self.parse_epsg)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CoordinatesConverter', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CoordinatesConverter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Koordinaten konvertieren'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Koordinaten konvertieren'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.reset()
        self.__change_format(0)
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def convert_entered_coordinates(self, point, guessed_system):
        """Converts given point based on the coordinate system to all other supported coordinate systems.

        :param point: An instance of a point
        :type point: MGRSPoint | UTMPoint | WGSPoint

        :param guessed_system: A instance of the enum CoordinateSystemString.
        :type guessed_system: CoordinateSystemString.UTM | CoordinateSystemString.MGRS | CoordinateSystemString.WGS_DEGREES
                              | CoordinateSystemString.WGS_COMMA | CoordinateSystemString.WGS_DEMS

        """
        if isinstance(point, points.WGSPoint):
            if guessed_system == CoordinateSystemString.WGS84_Degrees:
                dms_point = self.__degree_to_dms(point)
                self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
                comma_point = self.__degree_to_commaminutes(point)
                self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
                try:
                    utm_point = converter.degree_to_utm(point)
                    self.coordinates[CoordinateSystemString.UTM.value] = utm_point
                except Exception, e:
                    self.dlg.label_input_convert.setText(e.message)
                #mgrs_point = self.converter.convert_UTM_to_MGRS(utm_point)
                #self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point
            if guessed_system == CoordinateSystemString.WGS84_DMS:
                degree_point = self.__dms_to_degree(point)
                self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
                comma_point = self.__degree_to_commaminutes(degree_point)
                self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
                try:
                    utm_point = converter.degree_to_utm(degree_point)
                    self.coordinates[CoordinateSystemString.UTM.value] = utm_point
                except Exception, e:
                    self.dlg.label_input_convert.setText(e.message)
                #mgrs_point = self.converter.convert_UTM_to_MGRS(utm_point)
                #self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point
            if guessed_system == CoordinateSystemString.WGS84_CommaMinutes:
                degree_point = self.__commaminutes_to_degree(point)
                self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
                dms_point = self.__degree_to_dms(degree_point)
                self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
                try:
                    utm_point = converter.degree_to_utm(degree_point)
                    self.coordinates[CoordinateSystemString.UTM.value] = utm_point
                except Exception, e:
                    self.dlg.label_input_convert.setText(e.message)
                #mgrs_point = self.converter.convert_UTM_to_MGRS(utm_point)
                #self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point
        elif isinstance(point, points.MGRSPoint):
            utm_point = self.converter.convert_MGRS_to_UTM(point)
            self.coordinates[CoordinateSystemString.UTM.value] = utm_point
            degree_point = self.converter.convert_UTM_to_degree(utm_point)
            self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
            dms_point = self.__degree_to_dms(degree_point)
            self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
            comma_point = self.__degree_to_commaminutes(degree_point)
            self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
        elif isinstance(point, points.UTMPoint):
            try:
                degree_point = converter.utm_to_degree(point)
                self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
                dms_point = self.__degree_to_dms(degree_point)
                self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
                comma_point = self.__degree_to_commaminutes(degree_point)
                self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
            except Exception, e:
                self.dlg.label_input_convert.setText(e.message)
            #mgrs_point = self.converter.convert_UTM_to_MGRS(point)
            #self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point

    # def parse_epsg(self):
    #     try:
    #         parser = Parser()
    #         point = parser.parse(self.dlg.lineEdit_input_epsg.text())
    #         self.dlg.statusBar.showMessage('Valid ' + str(parser.guessed_system.value))
    #         if not isinstance(point, points.WGSPoint) and not parser.guessed_system == CoordinateSystemString.WGS84_Degrees:
    #             self.dlg.statusBar.showMessage('Degree format necessary')
    #         else:
    #             x, y = Converter.convert_based_on_epsg(point, str(self.dlg.comboBox_from.currentText()),
    #                                                    str(self.dlg.comboBox_to.currentText()))
    #             self.dlg.lineEdit_epsg_result.setText(str(x) + ' ' + str(y))
    #     except exceptions.ParseException, e:
    #         self.dlg.statusBar.showMessage(e.message)
    #     except exceptions.ConversionException, c:
    #         self.dlg.statusBar.showMessage(c.message)
    #     except RuntimeError:
    #         self.dlg.statusBar.showMessage('Conversion not possible')

    def __update_coordinate_fields(self):
        """Updates text in text fields based on existing point in dictionary self.coordinates."""
        for field in self.dlg.coordinate_fields:
            name = field.objectName()
            for key in self.coordinates:
                if key.lower() in name:
                    if 'WGS' not in key:
                        field.setText(self.coordinates[key].to_string())
                    else:
                        field.setText(self.coordinates[key].to_string(key))

    def __degree_to_dms(self, point):
        """Handles the conversion between the degrees and degree, minutes, seconds format.

        Returns new WGSPoint.
        """
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(point.lat_deg)
        return points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)

    def __degree_to_commaminutes(self, point):
        """Handles the conversion between the degrees and degree, decimal minutes format.

        Returns new WGSPoint.
        """
        long_deg, long_min = converter.convert_degree_to_decimal_minutes(point.long_deg)
        lat_deg, lat_min = converter.convert_degree_to_decimal_minutes(point.lat_deg)
        return points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)

    def __dms_to_degree(self, point):
        """Handles the conversion between the degree, minutes, seconds and degrees format.

        Returns new WGSPoint.
        """
        long_temp = converter.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_temp = converter.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        return points.WGSPoint(long_temp, 0, 0, lat_temp, 0, 0)

    def __commaminutes_to_degree(self, point):
        """Handles the conversion between the degree, decimal minutes and degrees format.

        Returns new WGSPoint.
        """
        long_deg = converter.convert_decimal_minutes_to_degree(point.long_deg, point.long_min)
        lat_deg = converter.convert_decimal_minutes_to_degree(point.lat_deg, point.lat_min)
        return points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)

    def __dms_to_commaminutes(self, point):
        """Handles the conversion between the degree, minutes, seconds and degrees, decimal minutes format.

        Returns new WGSPoint.
        """
        long_deg, long_min = converter.convert_dms_to_decimal_minutes(point.long_deg, point.long_min, point.long_sec)
        lat_deg, lat_min = converter.convert_dms_to_decimal_minutes(point.lat_deg, point.lat_min, point.lat_sec)
        return points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)

    def __load_epsg_codes(self):
        """Loads EPSG code from file in data directory to a dictionary."""
        file_path = self.plugin_dir + '/data/epsg_codes.txt'
        f = open(file_path)
        _dict = {}
        for line in f:
            code, description = line.split('\t')
            _dict[code] = description
        self.epsg_code_description = collections.OrderedDict(sorted(_dict.items()))

    def __load_epsg_codes_to_boxes(self):
        """Loads EPSG code from the dictionary to the comboboxes."""
        keys = self.epsg_code_description.keys()
        for key in keys:
            self.dlg.comboBox_from.addItem(key)
            self.dlg.comboBox_to.addItem(key)

    def __show_description_from(self, i):
        """Shows description of the selected EPSG code as tooltip."""
        self.dlg.comboBox_from.setToolTip(self.epsg_code_description.get(self.dlg.comboBox_from.itemText(i)))

    def __show_description_to(self, i):
        """Shows description of the selected EPSG code as tooltip."""
        self.dlg.comboBox_to.setToolTip(self.epsg_code_description.get(self.dlg.comboBox_to.itemText(i)))

    def __change_format(self, i):
        """Event triggered method which creates the selected coordinate system template in the GUI."""
        self.selected_format = i
        self.dlg.label_input_convert.setText('')
        self.dlg.clear_coordinate_fields()
        self.dlg.clear_format_layout()
        if i == 0:
            self.dlg.create_degrees_input()
        if i == 1:
            self.dlg.create_commaminutes_input()
        if i == 2:
            self.dlg.create_dms_input()
        if i == 3:
            self.dlg.create_utm_input()
        if i == 4:
            self.dlg.create_mgrs_input()

    def __change_hemisphere(self, i):
        """Event triggered method which changes the hemisphere according to user selection."""
        self.selected_hemisphere = i
        if i == 0:
            self.hemisphere = Hemisphere.NORTH
        if i == 1:
            self.hemisphere = Hemisphere.SOUTH
        self.__validate_utm_hemisphere()

    def __validate_WGS(self):
        """Event triggered method which delegates to validation methods based on the selected geographic coordinate system."""
        self.dlg.label_input_convert.setText('')
        if self.selected_format == 0:
            self.__validate_long_deg_value()
            self.__validate_lat_deg_value()
        if self.selected_format == 1:
            self.__validate_long_deg_comma_value()
            self.__validate_long_min_comma_value()
            self.__validate_lat_deg_comma_value()
            self.__validate_lat_min_comma_value()
        if self.selected_format == 2:
            self.__validate_long_deg_dms_value()
            self.__validate_long_min_dms_value()
            self.__validate_long_sec_dms_value()
            self.__validate_lat_deg_dms_value()
            self.__validate_lat_min_dms_value()
            self.__validate_lat_sec_dms_value()

    def __validate_UTM(self):
        """Event triggered method which delegates to validation methods based on the selected UTM system."""
        self.dlg.label_input_convert.setText('')
        if self.selected_format == 3:
            self.__validate_utm_zone()
            self.__validate_utm_hemisphere()
            self.__validate_utm_easting()
            self.__validate_utm_northing()

    """Validates entered value for the degree value of the latitude in the degrees format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_lat_deg_value(self):
            try:
                lat_deg_corrected = self.ensurer.ensure_it_is_a_number(self.dlg.lat_deg_input.text())
                self.ensurer.ensure_latitude_in_range(float(lat_deg_corrected))
                self.lat_deg = lat_deg_corrected
                point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                        self.lat_sec)
                self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_Degrees)
            except exceptions.ParseException, e:
                self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the degree value of the longitude in the degrees format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_long_deg_value(self):
            try:
                long_deg_corrected = self.ensurer.ensure_it_is_a_number(self.dlg.long_deg_input.text())
                self.ensurer.ensure_longitude_in_range(float(long_deg_corrected))
                self.long_deg = float(long_deg_corrected)
                point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                        self.lat_sec)
                self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_Degrees)
            except exceptions.ParseException, e:
                self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the degree value of the longitude in the degrees, decimal minutes format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_long_deg_comma_value(self):
        try:
            long_deg_corrected = self.ensurer.ensure_it_is_an_integer(self.dlg.long_deg_input.text())
            self.ensurer.ensure_longitude_in_range(float(long_deg_corrected))
            self.long_deg = long_deg_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_CommaMinutes)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the minutes value of the longitude in the degrees, decimal minutes format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_long_min_comma_value(self):
        try:
            long_min_corrected = self.ensurer.ensure_it_is_a_positive_number(self.dlg.long_min_input.text())
            self.ensurer.ensure_minutes_in_range(float(long_min_corrected))
            self.long_min = long_min_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_CommaMinutes)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the degree value of the latitude in the degrees, decimal minutes format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_lat_deg_comma_value(self):
        try:
            lat_deg_corrected = self.ensurer.ensure_it_is_an_integer(self.dlg.lat_deg_input.text())
            self.ensurer.ensure_latitude_in_range(float(lat_deg_corrected))
            self.lat_deg = lat_deg_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_CommaMinutes)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the minutes value of the latitude in the degrees, decimal minutes format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_lat_min_comma_value(self):
        try:
            lat_min_corrected = self.ensurer.ensure_it_is_a_positive_number(self.dlg.lat_min_input.text())
            self.ensurer.ensure_minutes_in_range(float(lat_min_corrected))
            self.lat_min = lat_min_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_CommaMinutes)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the degree value of the longitude in the DMS format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_long_deg_dms_value(self):
        try:
            long_deg_corrected = self.ensurer.ensure_it_is_an_integer(self.dlg.long_deg_input.text())
            self.ensurer.ensure_longitude_in_range(float(long_deg_corrected))
            self.long_deg = long_deg_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_DMS)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates minutes value for the degree value of the longitude in the DMS format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_long_min_dms_value(self):
        try:
            long_min_corrected = self.ensurer.ensure_it_is_a_positive_integer(self.dlg.long_min_input.text())
            self.ensurer.ensure_minutes_in_range(float(long_min_corrected))
            self.long_min = long_min_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_DMS)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the seconds value of the longitude in the DMS format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_long_sec_dms_value(self):
        try:
            long_sec_corrected = self.ensurer.ensure_it_is_a_positive_number(self.dlg.long_sec_input.text())
            self.ensurer.ensure_seconds_in_range(float(long_sec_corrected))
            self.long_sec = long_sec_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_DMS)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the degrees value of the latitude in the DMS format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_lat_deg_dms_value(self):
        try:
            lat_deg_corrected = self.ensurer.ensure_it_is_an_integer(self.dlg.lat_deg_input.text())
            self.ensurer.ensure_latitude_in_range(float(lat_deg_corrected))
            self.lat_deg = lat_deg_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_DMS)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the minutes value of the latitude in the DMS format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_lat_min_dms_value(self):
        try:
            lat_min_corrected = self.ensurer.ensure_it_is_a_positive_integer(self.dlg.lat_min_input.text())
            self.ensurer.ensure_minutes_in_range(float(lat_min_corrected))
            self.lat_min = lat_min_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_DMS)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the seconds value of the latitude in the DMS format.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_lat_sec_dms_value(self):
        try:
            lat_sec_corrected = self.ensurer.ensure_it_is_a_positive_number(self.dlg.lat_sec_input.text())
            self.ensurer.ensure_seconds_in_range(float(lat_sec_corrected))
            self.lat_sec = lat_sec_corrected
            point = points.WGSPoint(self.long_deg, self.long_min, self.long_sec, self.lat_deg, self.lat_min,
                                    self.lat_sec)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.WGS84_DMS)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the UTM zone.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_utm_zone(self):
        try:
            zone_corrected = self.ensurer.ensure_it_is_a_positive_integer(self.dlg.zone_input.text())
            self.ensurer.ensure_utm_zone_in_range(int(zone_corrected))
            self.utm_zone_number = zone_corrected
            point = points.UTMPoint(self.utm_easting, self.utm_northing, self.utm_zone_number,
                                    self.utm_zone_letter, self.hemisphere)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.UTM)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the UTM hemisphere.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_utm_hemisphere(self):
        point = points.UTMPoint(self.utm_easting, self.utm_northing, self.utm_zone_number,
                                self.utm_zone_letter, self.hemisphere)
        self.__calculate_based_on_new_values(point, CoordinateSystemString.UTM)

    """Validates entered value for the UTM easting.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_utm_easting(self):
        try:
            easting_corrected = self.ensurer.ensure_it_is_a_positive_integer(self.dlg.easting_input.text())
            self.ensurer.ensure_utm_easting_in_range(int(easting_corrected))
            self.utm_easting = easting_corrected
            point = points.UTMPoint(self.utm_easting, self.utm_northing, self.utm_zone_number,
                                    self.utm_zone_letter, self.hemisphere)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.UTM)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    """Validates entered value for the UTM northing.

    As long as the value is valid, the created point is simultaneously converted to other coordinate systems.
    """
    def __validate_utm_northing(self):
        try:
            northing_corrected = self.ensurer.ensure_it_is_a_positive_integer(self.dlg.northing_input.text())
            self.ensurer.ensure_utm_northing_in_range(int(northing_corrected))
            self.utm_northing = northing_corrected
            point = points.UTMPoint(self.utm_easting, self.utm_northing, self.utm_zone_number,
                                    self.utm_zone_letter, self.hemisphere)
            self.__calculate_based_on_new_values(point, CoordinateSystemString.UTM)
        except exceptions.ParseException, e:
            self.dlg.label_input_convert.setText(e.message)

    def __calculate_based_on_new_values(self, point, coordinate_system):
        """For reducing of duplicate code."""
        self.coordinates = {coordinate_system.value: point}
        self.convert_entered_coordinates(point, coordinate_system)
        self.__update_coordinate_fields()