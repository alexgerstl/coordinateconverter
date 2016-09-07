# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordinatesConverter
                                 A QGIS plugin
 konvertiert Koordinaten
                             -------------------
        begin                : 2016-08-23
        copyright            : (C) 2016 by Alexander Gerstl
        email                : alex.gerstl@gmx.at
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CoordinatesConverter class from file CoordinatesConverter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .coordinates_converter import CoordinatesConverter
    return CoordinatesConverter(iface)
