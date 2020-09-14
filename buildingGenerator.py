from maya import cmds
from Qt import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import sys
import pprint


def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)  # convert to Qt
    return ptr


class BuildingGenerator(QtWidgets.QWidget):

    def __init__(self):

        parent = QtWidgets.QDialog(parent=getMayaMainWindow())
        parent.setObjectName('Building Generator')
        parent.setWindowTitle('Building Generator')
        parent.resize(265, 300)
        parent.show()

        super(BuildingGenerator, self).__init__(parent=parent)

        self.buildUI()
        self.populate()

    def populate(self):
        pass

    def buildUI(self):

        # Layout
        layout = QtWidgets.QGridLayout(self)
        buildingWidget = QtWidgets.QWidget()
        layout.addWidget(buildingWidget)

        # Label - Title
        titleLabel = QtWidgets.QLabel("BUILDING GENERATOR")
        layout.addWidget(titleLabel, 0, 0, 1, 2)

        # Line Break
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line, 1, 0, 1, 3)

        # Label - Number of Walls
        numOfWallsLabel = QtWidgets.QLabel("Set Number of Walls")
        layout.addWidget(numOfWallsLabel, 2, 0, 1, 2)

        # LENGTH WIDGETS
        # Label - Length
        lengthLabel = QtWidgets.QLabel("Length")
        layout.addWidget(lengthLabel, 3, 0)

        # NameField - Length
        self.lengthNameField = QtWidgets.QSpinBox()
        self.lengthNameField.setValue(1)
        self.lengthNameField.valueChanged.connect(lambda val: self.lengthSlider.setValue(val))
        layout.addWidget(self.lengthNameField, 3, 1)

        # Slider - Length
        self.lengthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        self.lengthSlider.setMinimum(1)
        self.lengthSlider.setMaximum(100)
        self.lengthSlider.setValue(1)
        self.lengthSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.lengthSlider.setTickInterval(10)
        self.lengthSlider.valueChanged.connect(lambda val: self.lengthNameField.setValue(val))
        layout.addWidget(self.lengthSlider, 3, 2)

        # WIDTH WIDGETS
        # Label - Width
        widthLabel = QtWidgets.QLabel("Width")
        layout.addWidget(widthLabel, 4, 0)

        # NameField - Width
        self.widthNameField = QtWidgets.QSpinBox()
        self.widthNameField.setValue(1)
        self.widthNameField.valueChanged.connect(lambda val: self.widthSlider.setValue(val))
        layout.addWidget(self.widthNameField, 4, 1)

        # Slider - Width
        self.widthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        self.widthSlider.setMinimum(1)
        self.widthSlider.setMaximum(100)
        self.widthSlider.setValue(1)
        self.widthSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.widthSlider.setTickInterval(10)
        self.widthSlider.valueChanged.connect(lambda val: self.widthNameField.setValue(val))
        layout.addWidget(self.widthSlider, 4, 2)

        # FLOORS WIDGETS
        # Label - Floors
        floorLabel = QtWidgets.QLabel("Floors")
        layout.addWidget(floorLabel, 5, 0)

        # NameField - Floors
        self.floorNameField = QtWidgets.QSpinBox()
        self.floorNameField.setValue(1)
        self.floorNameField.valueChanged.connect(lambda val: self.floorSlider.setValue(val))
        layout.addWidget(self.floorNameField, 5, 1)

        # Slider - Floors
        self.floorSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        self.floorSlider.setMinimum(1)
        self.floorSlider.setMaximum(100)
        self.floorSlider.setValue(1)
        self.floorSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.floorSlider.setTickInterval(10)
        self.floorSlider.valueChanged.connect(lambda val: self.floorNameField.setValue(val))
        layout.addWidget(self.floorSlider, 5, 2)

        # Line Break
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line, 6, 0, 1, 3)

        # Label - Gap
        gapLabel = QtWidgets.QLabel("Adjust Gap")
        layout.addWidget(gapLabel, 7, 0, 1, 2)

        # LENGTH GAP WIDGETS
        # Label - Length Gap
        lengthGapLabel = QtWidgets.QLabel("Length")
        layout.addWidget(lengthGapLabel, 8, 0)

        # NameField - Length Gap
        self.lengthGapNameField = QtWidgets.QDoubleSpinBox()
        self.lengthGapNameField.setMinimum(-1000)
        self.lengthGapNameField.setMaximum(1000)
        self.lengthGapNameField.setValue(0)
        self.lengthGapNameField.valueChanged.connect(lambda val: self.lengthGapSlider.setValue(val))
        layout.addWidget(self.lengthGapNameField, 8, 1)

        # Slider - Length Gap
        self.lengthGapSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        self.lengthGapSlider.setMinimum(-1000)
        self.lengthGapSlider.setMaximum(1000)
        self.lengthGapSlider.setValue(0)
        self.lengthGapSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.lengthGapSlider.setTickInterval(10)
        self.lengthGapSlider.valueChanged.connect(lambda val: self.lengthGapNameField.setValue(val))
        layout.addWidget(self.lengthGapSlider, 8, 2)

        # HEIGHT GAP WIDGETS
        # Label - Height
        heightGapLabel = QtWidgets.QLabel("Height")
        layout.addWidget(heightGapLabel, 9, 0)

        # NameField - Floors
        self.heightGapNameField = QtWidgets.QDoubleSpinBox()
        self.heightGapNameField.setMinimum(-1000)
        self.heightGapNameField.setMaximum(1000)
        self.heightGapNameField.setValue(0)
        self.heightGapNameField.valueChanged.connect(lambda val: self.heightGapSlider.setValue(val))
        layout.addWidget(self.heightGapNameField, 9, 1)

        # Slider - Floors
        self.heightGapSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        self.heightGapSlider.setMinimum(-1000)
        self.heightGapSlider.setMaximum(1000)
        self.heightGapSlider.setValue(0)
        self.heightGapSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.heightGapSlider.setTickInterval(10)
        self.heightGapSlider.valueChanged.connect(lambda val: self.heightGapNameField.setValue(val))
        layout.addWidget(self.heightGapSlider, 9, 2)

        # Line Break
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line, 10, 0, 1, 3)

        # reverse button
        self.reverseBtn = QtWidgets.QPushButton('Undo')
        self.reverseBtn.clicked.connect(self.reverseBuilding)
        layout.addWidget(self.reverseBtn, 11, 0)

        # create button
        self.createBtn = QtWidgets.QPushButton('Create')
        self.createBtn.clicked.connect(self.createBuilding)
        layout.addWidget(self.createBtn, 11, 1, 1, 2)

    def createBuilding(self):
        # Raise error if not selected
        if not cmds.ls(selection=True):
            raise Exception("Cannot find a mesh to generate building. Please select a mesh.")

        # get Mesh selection
        selectedMeshes = cmds.ls(selection=True)
        self.selectedMesh = selectedMeshes.pop(0)

        # Variable - Mesh Scale
        cmds.makeIdentity(self.selectedMesh, apply=True, t=1, r=1, s=1, n=0)
        bbox = cmds.exactWorldBoundingBox(self.selectedMesh, calculateExactly=True, ignoreInvisible=True)
        bboxTranslate = cmds.xform(self.selectedMesh, q=1, ws=1, rp=1)

        bboxScale = [abs(abs(bbox[3]) - abs(bbox[0])), abs(abs(bbox[4]) - abs(bbox[1])),
                     abs(abs(bbox[5]) - abs(bbox[2]))]

        # Variables - floors, length, width
        floorCount = self.floorNameField.value()
        lengthCount = self.lengthNameField.value()
        widthCount = self.widthNameField.value()
        lengthGap = self.lengthGapNameField.value()
        heightGap = self.heightGapNameField.value()

        instance = True
        self.buildingMeshes = []

        # Populate Wall Width
        for i in range(2):
            scale = -1 if i == 0 else 1
            for y in range(widthCount):
                for z in range(floorCount):
                    self.buildingMeshes.append(cmds.duplicate(name=self.selectedMesh))
                    cmds.xform(absolute=True,
                               translation=[(i * lengthCount * bboxScale[1]) + (i * lengthGap * lengthCount),
                                            (y * -bboxScale[1]) - (lengthGap * (y - 1)) - (lengthGap + lengthGap / 2),
                                            z * bboxScale[2] + heightGap * z],
                               scale=[scale, 1, 1])

        # Populate Wall Length
        for i in range(2):
            scale = -1 if i == 1 else 1
            for x in range(lengthCount):
                for z in range(floorCount):
                    self.buildingMeshes.append(cmds.duplicate(name=self.selectedMesh))
                    cmds.xform(absolute=True,
                               translation=[(x * bboxScale[1]) + (lengthGap * (x - 1)) + (lengthGap + lengthGap / 2),
                                            (i * widthCount * -bboxScale[1]) - (i * lengthGap * widthCount),
                                            z * bboxScale[2] + heightGap * z],
                               rotation=[0, 0, 90],
                               scale=[scale, 1, 1])

        # Populate Floors
        cmds.polyPlane(subdivisionsX=1, subdivisionsY=1)
        for i in range(floorCount + 1):
            self.buildingMeshes.append(cmds.duplicate())
            cmds.xform(absolute=True,
                       translation=[bboxTranslate[0] + (lengthCount * bboxScale[1]) / 2 + (lengthGap * lengthCount) / 2,
                                    bboxTranslate[1] - (widthCount * bboxScale[1]) / 2 - (lengthGap * widthCount) / 2,
                                    bboxTranslate[2] + i * bboxScale[2] + heightGap * i],
                       rotation=[90, 0, 0],
                       scale=[(lengthCount * bboxScale[1] + (lengthGap * lengthCount)), 1,
                              (widthCount * bboxScale[1]) + (lengthGap * widthCount)])
            print(bboxTranslate[2] + i * bboxScale[2] + heightGap * i)

        # move original mesh to the side
        cmds.xform(self.selectedMesh,
                   absolute=True,
                   translation=[0, 2 * bboxScale[1],
                                0])

    def reverseBuilding(self):

        for i in self.buildingMeshes:
            cmds.delete(i)

        self.buildingMeshes = []

        cmds.move(0, 0, 0, self.selectedMesh)
        cmds.select(self.selectedMesh)
