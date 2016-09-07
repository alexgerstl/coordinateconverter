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
from coordinate_parser import Parser, CoordinateSystemString
from converter import Converter
import os.path
import points
import exceptions
import collections


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
        self.menu = self.tr(u'&Koordinatenkonvertierer')
        self.toolbar = self.iface.addToolBar(u'CoordinatesConverter')
        self.toolbar.setObjectName(u'CoordinatesConverter')

        self.coordinates = {}
        self.epsg_code_description = {}
        self.converter = Converter()
        self.__load_epsg_codes()
        self.__load_epsg_codes_to_boxes()
        self.dlg.lineEdit_input.textChanged.connect(self.parse)
        self.dlg.comboBox_from.currentIndexChanged.connect(self.__show_description_from)
        self.dlg.comboBox_to.currentIndexChanged.connect(self.__show_description_to)
        self.dlg.lineEdit_input_epsg.textChanged.connect(self.parse_epsg)

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
            text=self.tr(u'Koordinatenkonvertierer'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Koordinatenkonvertierer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        self.dlg.reset()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def parse(self):
        try:
            parser = Parser()
            point = parser.parse(self.dlg.lineEdit_input.text())
            self.dlg.statusBar.showMessage('Valid ' + str(parser.guessed_system.value))
            self.coordinates = {parser.guessed_system.value: point}
            self.convert_entered_coordinates(point, parser.guessed_system)
            self.__update_coordinate_fields()
        except exceptions.ParseException, e:
            self.dlg.statusBar.showMessage(e.message)
            self.coordinates.clear()
            self.dlg.clear_coordinate_fields()
        except exceptions.ConversionException, c:
            self.dlg.statusBar.showMessage(c.message)
            self.coordinates.clear()
            self.dlg.clear_coordinate_fields()

    def convert_entered_coordinates(self, point, guessed_system):
        if isinstance(point, points.WGSPoint):
            if guessed_system == CoordinateSystemString.WGS84_Degrees:
                dms_point = self.__degree_to_DMS(point)
                self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
                comma_point = self.__degree_to_Commaminutes(point)
                self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
                utm_point = self.converter.convert_degree_to_UTM(point)
                self.coordinates[CoordinateSystemString.UTM.value] = utm_point
                mgrs_point = self.converter.convert_UTM_to_MGRS(utm_point)
                self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point
            if guessed_system == CoordinateSystemString.WGS84_DMS:
                degree_point = self.__DMS_to_degree(point)
                self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
                comma_point = self.__degree_to_Commaminutes(degree_point)
                self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
                utm_point = self.converter.convert_degree_to_UTM(degree_point)
                self.coordinates[CoordinateSystemString.UTM.value] = utm_point
                mgrs_point = self.converter.convert_UTM_to_MGRS(utm_point)
                self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point
            if guessed_system == CoordinateSystemString.WGS84_CommaMinutes:
                degree_point = self.__commaminutes_to_degree(point)
                self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
                dms_point = self.__degree_to_DMS(degree_point)
                self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
                utm_point = self.converter.convert_degree_to_UTM(degree_point)
                self.coordinates[CoordinateSystemString.UTM.value] = utm_point
                mgrs_point = self.converter.convert_UTM_to_MGRS(utm_point)
                self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point
        elif isinstance(point, points.MGRSPoint):
            utm_point = self.converter.convert_MGRS_to_UTM(point)
            self.coordinates[CoordinateSystemString.UTM.value] = utm_point
            degree_point = self.converter.convert_UTM_to_degree(utm_point)
            self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
            dms_point = self.__degree_to_DMS(degree_point)
            self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
            comma_point = self.__degree_to_Commaminutes(degree_point)
            self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
        elif isinstance(point, points.UTMPoint):
            degree_point = self.converter.convert_UTM_to_degree(point)
            self.coordinates[CoordinateSystemString.WGS84_Degrees.value] = degree_point
            dms_point = self.__degree_to_DMS(degree_point)
            self.coordinates[CoordinateSystemString.WGS84_DMS.value] = dms_point
            comma_point = self.__degree_to_Commaminutes(degree_point)
            self.coordinates[CoordinateSystemString.WGS84_CommaMinutes.value] = comma_point
            mgrs_point = self.converter.convert_UTM_to_MGRS(point)
            self.coordinates[CoordinateSystemString.MGRS.value] = mgrs_point

    def parse_epsg(self):
        try:
            parser = Parser()
            point = parser.parse(self.dlg.lineEdit_input_epsg.text())
            self.dlg.statusBar.showMessage('Valid ' + str(parser.guessed_system.value))
            if not isinstance(point, points.WGSPoint) and not parser.guessed_system == CoordinateSystemString.WGS84_Degrees:
                self.dlg.statusBar.showMessage('Degree format necessary')
            else:
                x, y = Converter.convert_based_on_epsg(point, str(self.dlg.comboBox_from.currentText()),
                                                       str(self.dlg.comboBox_to.currentText()))
                self.dlg.lineEdit_epsg_result.setText(str(x) + ' ' + str(y))
        except exceptions.ParseException, e:
            self.dlg.statusBar.showMessage(e.message)
        except exceptions.ConversionException, c:
            self.dlg.statusBar.showMessage(c.message)
        except RuntimeError:
            self.dlg.statusBar.showMessage('Conversion not possible')

    def __update_coordinate_fields(self):
        for field in self.dlg.coordinate_fields:
            name = field.objectName()
            for key in self.coordinates:
                if key.lower() in name:
                    if 'WGS' not in key:
                        field.setText(self.coordinates[key].to_string())
                    else:
                        field.setText(self.coordinates[key].to_string(key))

    def __degree_to_DMS(self, point):
        long_deg, long_min, long_sec = self.converter.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = self.converter.convert_degree_to_DMS(point.lat_deg)
        return points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)

    def __degree_to_Commaminutes(self, point):
        long_deg, long_min = self.converter.convert_degree_to_decimal_minutes(point.long_deg)
        lat_deg, lat_min = self.converter.convert_degree_to_decimal_minutes(point.lat_deg)
        return points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)

    def __DMS_to_degree(self, point):
        long_temp = self.converter.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_temp = self.converter.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        return points.WGSPoint(long_temp, 0, 0, lat_temp, 0, 0)

    def __commaminutes_to_degree(self, point):
        long_deg = self.converter.convert_decimal_minutes_to_degree(point.long_deg, point.long_min)
        lat_deg = self.converter.convert_decimal_minutes_to_degree(point.lat_deg, point.lat_min)
        return points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)

    def __load_epsg_codes(self):
        file_path = self.plugin_dir + '/data/epsg_codes.txt'
        f = open(file_path)
        _dict = {}
        for line in f:
            code, description = line.split('\t')
            _dict[code] = description
        self.epsg_code_description = collections.OrderedDict(sorted(_dict.items()))

    def __load_epsg_codes_to_boxes(self):
        keys = self.epsg_code_description.keys()
        for key in keys:
            self.dlg.comboBox_from.addItem(key)
            self.dlg.comboBox_to.addItem(key)

    def __show_description_from(self, i):
        self.dlg.comboBox_from.setToolTip(self.epsg_code_description.get(self.dlg.comboBox_from.itemText(i)))

    def __show_description_to(self, i):
        self.dlg.comboBox_to.setToolTip(self.epsg_code_description.get(self.dlg.comboBox_to.itemText(i)))
