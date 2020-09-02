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

        # Freeze Transform
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

        # Variables - mesh scale
        bbox = cmds.exactWorldBoundingBox(selectedMesh)
        bboxScale = [abs(bbox[0] - bbox[3]), abs(bbox[1] - bbox[4]), abs(bbox[2] - bbox[5])]

        # Variables - floors, length, width
        floorCount = 4
        lengthCount = 2
        widthCount = 3
        instance = True
        buildingMeshes = []

        # Create Wall in Width
        for i in range(2):
            scale = -1 if i == 0 else 1
            for y in range(widthCount):
                for z in range(floorCount):
                    buildingMeshes.append(cmds.duplicate(name=selectedMesh, instanceLeaf=instance))
                    cmds.xform(absolute=True,
                               translation=[i * lengthCount * bboxScale[1], y * -bboxScale[1] - 5.5, z * bboxScale[2]],
                               scale=[scale, 1, 1])

        # Create Wall in Length
        for i in range(2):
            scale = -1 if i == 1 else 1
            for x in range(lengthCount):
                for z in range(floorCount):
                    buildingMeshes.append(cmds.duplicate(name=selectedMesh, instanceLeaf=instance))
                    cmds.xform(absolute=True,
                               translation=[x * bboxScale[1], i * widthCount * -bboxScale[1] - 5.5, z * bboxScale[2]],
                               rotation=[0, 0, 90],
                               scale=[scale, 1, 1])

        # Floors
        cmds.polyPlane(subdivisionsX=1, subdivisionsY=1)
        for i in range(floorCount + 1):
            cmds.duplicate(instanceLeaf=instance)
            cmds.xform(absolute=True,
                       translation=[(lengthCount * bboxScale[1]) / 2, -(widthCount * bboxScale[1]) / 2, i * bboxScale[2]],
                       rotation=[90, 0, 0],
                       scale=[lengthCount * bboxScale[1], 1, widthCount * bboxScale[1]])

        self.buildingMeshes = buildingMeshes
        var = lambda val: cmds.delete(self.buildingMeshes)

    def deleteWalls(self, *args):
        cmds.delete(self.buildingMeshes)
