from maya import cmds
import pprint


class BuildingGenerator():

    def __init__(self):
        pass

    def createBuilding(self):
        # Raise error if not selected
        if not cmds.ls(selection=True):
            raise Exception("Cannot find a mesh to generate building. Please select a mesh.")

        # get Mesh selection
        selectedMeshes = cmds.ls(selection=True)
        selectedMesh = selectedMeshes.pop(0)

        # Variables - mesh scale
        bbox = cmds.exactWorldBoundingBox(selectedMesh)
        bboxScale = [abs(bbox[0] - bbox[3]), abs(bbox[1] - bbox[4]), abs(bbox[2] - bbox[5])]

        # Variables - floors, length, width
        floorCount = 2
        lengthCount = 4
        widthCount = 3

        self.addWalls(lengthCount, widthCount, floorCount, bboxScale)

        return lengthCount, widthCount, floorCount, bboxScale

    def addWalls(self, lengthCount, widthCount, floorCount, bboxScale):

        for y in range(widthCount):
            for z in range(floorCount):
                cmds.duplicate(instanceLeaf=True)
                cmds.xform(absolute=True, translation=[0, y * -bboxScale[1], z * bboxScale[2]])

