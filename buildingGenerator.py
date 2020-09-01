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
        lengthCount = 2
        widthCount = 2
        instance = True

        self.addWalls(selectedMesh, lengthCount, widthCount, floorCount, bboxScale, instance)

        return selectedMesh, lengthCount, widthCount, floorCount, bboxScale

    def addWalls(self, selectedMesh, lengthCount, widthCount, floorCount, bboxScale, instance):

        for i in range(2):
            scale = -1 if i == 0 else 1
            for y in range(widthCount):
                for z in range(floorCount):
                    cmds.duplicate(name=selectedMesh, instanceLeaf=instance)
                    cmds.xform(absolute=True,
                               translation=[i * lengthCount * bboxScale[1], y * -bboxScale[1], z * bboxScale[2]],
                               scale=[scale, 1, 1])

        for i in range(2):
            scale = -1 if i == 1 else 1
            for x in range(lengthCount):
                for z in range(floorCount):
                    cmds.duplicate(name=selectedMesh, instanceLeaf=instance)
                    cmds.xform(absolute=True,
                               translation=[x * bboxScale[1], i * widthCount * -bboxScale[1], z * bboxScale[2]],
                               rotation=[1, 1, 90],
                               scale=[scale, 1, 1])
