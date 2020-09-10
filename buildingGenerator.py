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
        parent.resize(250, 300)
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
        numOfWallsLabel = QtWidgets.QLabel("Number of Walls")
        layout.addWidget(numOfWallsLabel, 2, 0, 1, 2)

        # LENGTH WIDGETS
        # Label - Length
        lengthLabel = QtWidgets.QLabel("Length")
        layout.addWidget(lengthLabel, 3, 0)

        # NameField - Length
        lengthNameField = QtWidgets.QLineEdit()
        layout.addWidget(lengthNameField, 3, 1)

        # Slider - Length
        lengthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        lengthSlider.setMinimum(1)
        lengthSlider.setMaximum(100)
        layout.addWidget(lengthSlider, 3, 2)

        # WIDTH WIDGETS
        # Label - Width
        widthLabel = QtWidgets.QLabel("Width")
        layout.addWidget(widthLabel, 4, 0)

        # NameField - Width
        widthNameField = QtWidgets.QLineEdit()
        layout.addWidget(widthNameField, 4, 1)

        # Slider - Width
        widthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        widthSlider.setMinimum(1)
        widthSlider.setMaximum(100)
        layout.addWidget(widthSlider, 4, 2)

        # FLOORS WIDGETS
        # Label - Floors
        floorLabel = QtWidgets.QLabel("Floors")
        layout.addWidget(floorLabel, 5, 0)

        # NameField - Floors
        floorNameField = QtWidgets.QLineEdit()
        layout.addWidget(floorNameField, 5, 1)

        # Slider - Floors
        floorSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        floorSlider.setMinimum(1)
        floorSlider.setMaximum(100)
        layout.addWidget(floorSlider, 5, 2)

        # Line Break
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line, 6, 0, 1, 3)

        # Label - Gap
        gapLabel = QtWidgets.QLabel("Gap")
        layout.addWidget(gapLabel, 7, 0, 1, 2)

        # LENGTH GAP WIDGETS
        # Label - Length Gap
        lengthGapLabel = QtWidgets.QLabel("Length")
        layout.addWidget(lengthGapLabel, 8, 0)

        # NameField - Length Gap
        lengthGapNameField = QtWidgets.QLineEdit()
        layout.addWidget(lengthGapNameField, 8, 1)

        # Slider - Length Gap
        lengthGapSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        lengthGapSlider.setMinimum(1)
        lengthGapSlider.setMaximum(100)
        layout.addWidget(lengthGapSlider, 8, 2)

        # HEIGHT GAP WIDGETS
        # Label - Height
        heightGapLabel = QtWidgets.QLabel("Height")
        layout.addWidget(heightGapLabel, 9, 0)

        # NameField - Floors
        heightGapNameField = QtWidgets.QLineEdit()
        layout.addWidget(heightGapNameField, 9, 1)

        # Slider - Floors
        heightGapSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # left to right slider
        heightGapSlider.setMinimum(1)
        heightGapSlider.setMaximum(100)
        layout.addWidget(heightGapSlider, 9, 2)

        # Line Break
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line, 10, 0, 1, 3)

        # import button
        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createBuilding)
        layout.addWidget(createBtn, 11, 0, 1, 3)

    def createBuilding(self):
        # Raise error if not selected
        if not cmds.ls(selection=True):
            raise Exception("Cannot find a mesh to generate building. Please select a mesh.")

        # get Mesh selection
        selectedMeshes = cmds.ls(selection=True)
        selectedMesh = selectedMeshes.pop(0)

        # Variable - Mesh Scale
        bbox = cmds.exactWorldBoundingBox(selectedMesh)
        cmds.makeIdentity(selectedMesh, apply=True, t=True, r=True, s=True, n=1)
        bboxTranslate = cmds.xform(selectedMesh, q=1, ws=1, rp=1)

        bboxScale = [abs(abs(bbox[3]) - abs(bbox[0])), abs(abs(bbox[4]) - abs(bbox[1])),
                     abs(abs(bbox[5]) - abs(bbox[2]))]

        # Variables - floors, length, width
        floorCount = 4
        lengthCount = 2
        widthCount = 3
        instance = True
        buildingMeshes = []

        # Populate Wall Width
        for i in range(2):
            scale = -1 if i == 0 else 1
            for y in range(widthCount):
                for z in range(floorCount):
                    buildingMeshes.append(cmds.duplicate(name=selectedMesh, instanceLeaf=instance))
                    cmds.xform(absolute=True,
                               translation=[i * lengthCount * bboxScale[1], y * -bboxScale[1] - 5.5, z * bboxScale[2]],
                               scale=[scale, 1, 1])

        # Populate Wall Length
        for i in range(2):
            scale = -1 if i == 1 else 1
            for x in range(lengthCount):
                for z in range(floorCount):
                    buildingMeshes.append(cmds.duplicate(name=selectedMesh, instanceLeaf=instance))
                    cmds.xform(absolute=True,
                               translation=[x * bboxScale[1], i * widthCount * -bboxScale[1] - 5.5, z * bboxScale[2]],
                               rotation=[0, 0, 90],
                               scale=[scale, 1, 1])

        # Populate Floors
        cmds.polyPlane(subdivisionsX=1, subdivisionsY=1)
        for i in range(floorCount + 1):
            cmds.duplicate(instanceLeaf=instance)
            cmds.xform(absolute=True,
                       translation=[bboxTranslate[0] + (lengthCount * bboxScale[1]) / 2,
                                    bboxTranslate[1] + -(widthCount * bboxScale[1]) / 2,
                                    bboxTranslate[2] + i * bboxScale[2]],
                       rotation=[90, 0, 0],
                       scale=[lengthCount * bboxScale[1], 1, widthCount * bboxScale[1]])

        self.buildingMeshes = buildingMeshes

        # Delete mesh
        cmds.delete(selectedMesh)

        var = lambda val: cmds.delete(self.buildingMeshes)

    # def deleteWalls(self, *args):
    #    cmds.delete(self.buildingMeshes)