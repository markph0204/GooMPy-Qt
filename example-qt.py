#!/usr/bin/env python
"""
Example of using GooMPy with QT

Copyright (C) 2015 Alec Singer and Simon D. Levy
Qt version modified by Mark Hurley

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.
This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from goompy import *

WIDTH = 800
HEIGHT = 500

LATITUDE = 37.7913838
LONGITUDE = -79.44398934
ZOOM = 15
MAPTYPE = 'roadmap'


class MyView(QtWidgets.QGraphicsView):
    """
    In QT, QGraphicsView is a Base Windows class which handles a lot of
    """

    def __init__(self, scene):
        QtWidgets.QGraphicsView.__init__(self, scene)
        self.setMaximumSize(WIDTH, HEIGHT)
        self.goompy = GooMPy(WIDTH, HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE)

        self.setCacheMode(QtWidgets.QGraphicsView.CacheNone)
        self.coords = None
        self.is_pan = False
        self.zoomlevel = ZOOM

        # Set image
        self.update_map_background()

    def resizeEvent(self, ev: QtGui.QResizeEvent):
        self.update_map_background()

    # ref: http://stackoverflow.com/a/5156978/23991
    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.LeftButton:
            self.is_pan = True
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self.coords = ev.x(), ev.y()
            ev.accept()
        else:
            ev.ignore()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.LeftButton:
            self.is_pan = False
            self.setCursor(QtCore.Qt.ArrowCursor)
            ev.accept()
        else:
            ev.ignore()

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        if self.is_pan:
            self.goompy.move(self.coords[0] - ev.x(), self.coords[1] - ev.y())
            self.update_map_background()
            self.coords = ev.x(), ev.y()
            ev.accept()
        else:
            ev.ignore()

    def update_map_background(self):
        qimage = self.goompy.getImageQt().copy()
        brush = QtGui.QBrush(qimage)
        self.setBackgroundBrush(brush)

    def zoom_button_call(self, val):
        new_level = self.zoomlevel + val
        if new_level > 0 and new_level < 22:
            self.zoomlevel = new_level
            self.goompy.useZoom(new_level)

    def zoom_button_plus(self):
        self.zoom_button_call(+1)

    def zoom_button_minus(self):
        self.zoom_button_call(-1)

    def reload(self):
        self.coords = None
        self.update_map_background()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    scene = QtWidgets.QGraphicsScene(QtCore.QRectF(0, 0, WIDTH, HEIGHT))
    view = MyView(scene)
    view.setWindowTitle("Move Map")
    view.show()
    sys.exit(app.exec())
