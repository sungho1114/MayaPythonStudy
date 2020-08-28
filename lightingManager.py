import os
import time
from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial
import Qt
import logging  # python library defining outputs and levels
from maya import OpenMayaUI as omui
import json

logging.basicConfig()
logger = logging.getLogger('LightingManager')  # control logger
logger.setLevel(logging.DEBUG)  # every logger down to debug will be disabled

if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQT'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal


def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()

    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)  # convert to Qt
    return ptr


def getDock(name='LightingManager'):
    deleteDock(name)
    ctrl = pm.workspaceControl(name, dockToMainWindow=('right', 1), label="Lighting Manager")
    qtCtrl = omui.MQtUtil_findControl(ctrl)  # memory address of the control
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr


def deleteDock(name='LightingManager'):
    if pm.workspaceControl(name, query=True, exists=True):
        pm.deleteUI(name)


class LightManager(QtWidgets.QWidget):
    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Directional Light": pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        # call which function to call later as well as which argument to give
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True)
    }

    def __init__(self, dock=True):

        if dock:
            parent = getDock()
        else:
            deleteDock()

            # try this, if there is no ui, continue
            try:
                pm.deleteUI('lightingManager')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('lightingManager')
            parent.setWindowTitle('Lighting Manager')
            layout = QtWidgets.QVBoxLayout(parent)

        # super to LightManager
        super(LightManager, self).__init__(parent=parent)

        self.buildUI()
        self.populate()

        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()

    def populate(self):
        while self.scrollLayout.count():  # while this counts its child
            widget = self.scrollLayout.takeAt(0).widget()  # get the child at position 0 to get its widget
            if widget:
                widget.setVisible(False)
                widget.deleteLater()

        for light in pm.ls(type=["areaLight", "spotLight", "pointLight", "directionalLight", "volumeLight"]):
            self.addLight(light)

    def buildUI(self):
        # build layout and apply to self
        layout = QtWidgets.QGridLayout(self)

        # combo box to put light type
        self.lightTypeCB = QtWidgets.QComboBox()  # add dropbox (combo box)
        # add items in the list
        for lightType in sorted(self.lightTypes):  # sorting by alphabet
            self.lightTypeCB.addItem(lightType)
        layout.addWidget(self.lightTypeCB, 0, 0, 1, 2)  # add widget on row 0, column 0

        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn, 0, 2)  # add widget on row 0, column 1

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        # scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1, 0, 1, 3)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.saveLight)
        layout.addWidget(saveBtn, 2, 0)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.importLight)
        layout.addWidget(importBtn, 2, 1)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        layout.addWidget(refreshBtn, 2, 2)

    def saveLight(self):
        properties = {}

        for lightWidget in self.findChildren(LightWidget):
            light = lightWidget.light
            transform = light.getTransform()

            properties[str(transform)] = {
                'translate': list(transform.translate.get()),
                'rotation': list(transform.rotate.get()),
                'lightType': pm.objectType(light),
                'intensity': light.intensity.get(),
                'color': light.color.get()
            }

        directory = self.getDirectory()

        lightFile = os.path.join(directory, 'lightFile_%s.json' % time.strftime('%m%d'))  # current month and day
        with open(lightFile, 'w') as f:
            json.dump(properties, f, indent=4)

        logger.info('saving file to %s' % lightFile)

    def getDirectory(self):
        directory = os.path.join(pm.internalVar(userAppDir=True), 'lightManager')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def importLight(self):
        directory = self.getDirectory()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Light Browser", directory)  # open import directory
        with open(filename[0], 'r') as f:
            properties = json.load(f)

        for light, info in properties.items():
            lightType = info.get('lightType')
            # for every one of the light type, it will check light type matches, if it matches, break the loop
            for lt in self.lightTypes:
                if ('%sLight' % lt.split()[0].lower()) == lightType:
                    break
            else:
                logger.info('Cannot find a corresponding light type for %s' % light)
                continue

            light = self.createLight(lightType=lt)
            light.intensity.set(info.get('intensity'))

            light.color.set(info.get('color'))

            transform = light.getTransform()
            transform.translate.set(info.get('translate'))
            transform.rotate.set(info.get('rotation'))

        self.populate()

    def createLight(self, lightType=None, add=True):
        if not lightType:
            lightType = self.lightTypeCB.currentText()
        func = self.lightTypes[lightType]

        light = func()
        if add:
            self.addLight(light)

        return light

    def addLight(self, light):
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        widget.onSolo.connect(self.onSolo)
        self.scrollLayout.addWidget(widget)

    def onSolo(self, value):
        lightWidgets = self.findChildren(LightWidget)
        for widget in lightWidgets:
            if widget != self.sender():
                widget.disableLight(value)


class LightWidget(QtWidgets.QWidget):
    onSolo = Signal(bool)  # define the signal

    def __init__(self, light):
        super(LightWidget, self).__init__()

        # check if it is a light from pymel
        if isinstance(light, basestring):
            light = pm.PyNode(light)
        if isinstance(light, pm.nodetypes.Transform):
            light = light.getShape()

        self.light = light
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(
            val))  # toggle button function, lambda : call functions later, take input when it runs
        """
        same as lambda function
        same as lambda function
        def setLightVisibility(val):
            self.light.visibility.set(val)
        """
        layout.addWidget(self.name, 0, 0)

        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)  # pressed and depressed hold
        soloBtn.toggled.connect(lambda val: self.onSolo.emit(val))
        layout.addWidget(soloBtn, 0, 1)

        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 2)

        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        intensity.setMinimum(1)
        intensity.setMaximum(100)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)

        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

    def setButtonColor(self, color=None):
        if not color:
            color = self.light.color.get()

        assert len(
            color) == 3, "You mush provide a list of 3 colors"  # it is gonna give error if there is no 3 color info

        r, g, b = [c * 255 for c in color]  # for each value in color, multiplying 255

        self.colorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0)' % (r, g, b))

    def setColor(self):
        lightColor = self.light.color.get()
        color = pm.colorEditor(rgbValue=lightColor)

        r, g, b, a = [float(c) for c in color.split()]  # split the string in every space

        color = (r, g, b)

        print(color)
        self.light.color.set(color)
        self.setButtonColor(color)

    def disableLight(self, value):
        self.name.setChecked(not value)  # opposite value

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        pm.delete(self.light.getTransform())


"""
# this function shows the UI through LightManager class
def showUI():
    ui = LightManager()
    ui.show()
    return ui
"""
