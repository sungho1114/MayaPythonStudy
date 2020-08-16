from maya import cmds
from tweenerUI import tween
from gearClassCreator import Gear

class BasicWindow(object):
    
    windowName = "BasicWindow"
    
    def show(self):

        if cmds.window(self.windowName, query = True, exists = True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow()


    def buildUI(self):
        pass

    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)

class TweenerUI(BasicWindow):

    windowName = "TweenerWindow"

    def buildUI(self):

        column = cmds.columnLayout()

        cmds.text(label = "Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns = 2)

        self.slider = cmds.floatSlider(min = 0, max = 100, value = 50, step = 1, changeCommand = tween)

        cmds.button(label = "Reset", command = self.reset)

        cmds.setParent(column)
        cmds.button(label = "Close", command = self.close)

    #don't need another argument, but needed for maya requirement, dump variable into argus
    def reset(self, *args):
        #whenever edit works, value changes
        cmds.floatSlider(self.slider, edit = True, value = 50)


class GearUI(BasicWindow):

    windowName = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):

        column = cmds.columnLayout()
        cmds.text(label = "Use the slider to modify the gear")

        cmds.rowLayout(numberOfColumns = 4)

        self.label = cmds.text(label = "10")

        self.slider = cmds.intSlider(min = 5, max = 30, value = 10, step = 1, dragCommand = self.modifyGear)
        cmds.button(label = "Make Gear", command = self.makeGear)
        cmds.button(label = "Reset", command = self.reset)

        cmds.setParent(column)
        cmds.button(label = "Close", command = self.close)  # already made on the top

    def makeGear(self, *argu):
        # query value
        teeth = cmds.intSlider(self.slider, query = True, value = True)

        self.gear = Gear()

        self.gear.createGear(teeth = teeth)

    def modifyGear(self, teeth):
        if self.gear:
            self.gear.changeTeeth(teeth = teeth)

        cmds.text(self.label, edit = True, label = teeth)

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit = True, value = 10)
        cmds.text(self.label, edit = True, label = 10)