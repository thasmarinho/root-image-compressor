from root.controller import TransformationController
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5. QtGui import *
import imageio
import numpy as np
import sys
sys.path.insert(0, sys.path[0] + '\\..\\controller')
print(sys.path)


class ImageView(QWidget):
    def __init__(self, img):
        super().__init__()
        self.setStyleSheet(" border:2px solid rgb(150,150, 150); ")

        self.label = QLabel(self)
        self.loadImage(img)

        self.label.setGeometry(0, 0, self.image.width(), self.image.height())
        self.label.setAlignment(Qt.AlignCenter)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.label)
        self.setLayout(mainLayout)

    def loadImage(self, im):
        transformController = TransformationController()
        if type(im) is str:
            im = transformController.openImage(im)

        im = im.astype(np.uint8)

        qimage = self.toQImage(im)

        self.image = QPixmap.fromImage(qimage)
        self.label.setPixmap(self.image)

    def scale(self, width, height):
        if width > height:
            self.image = self.image.scaledToWidth(width)
        else:
            self.image = self.image.scaledToHeight(height)
        self.label.setPixmap(self.image)

    def _cmap2rgb(cmap, step):
        from matplotlib import cm
        return getattr(cm, cmap)(step)

    def toQImage(self, im, copy=False):
        if im is None:
            return QImage()

        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(
                    im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                for i in range(0, 256):
                    qim.setColor(i, qRgb(i, i, i))
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(
                        im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(
                        im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGBA8888)
                    return qim.copy() if copy else qim
