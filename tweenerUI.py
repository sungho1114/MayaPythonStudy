from maya import cmds


def tween(percentage, obj = None, attrs = None, selection = True):

    # if obj is not given and selection is set to false, alart early to prevent error
    if not obj and not selection:
        raise ValueError("No object given to tween")

    # if no obj is specified, get it from the first selection
    if not obj:
        obj = cmds.ls(selection = True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable = True)

    currentTime = cmds.currentTime(query = True)

    for attr in attrs:

        # construct the full name of the attribute with its object
        attrFull = '%s.%s' % (obj, attr)
        # get the keyframes of the attribute on this project
        keyframes = cmds.keyframe(attrFull, query = True)

        #if there are no keyframes, continue
        if not keyframes:
            continue

        previousKeyframes = []
        for frame in keyframes:
            if frame < currentTime:
                previousKeyframes.append(frame)

        # for frame in keyframes, if statements works, put frame (first frame), same as last chunk but shorter
        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        # check if there frames doesn't exist
        if not previousKeyframes and not laterKeyframes:
            continue

        previousFrame = max(previousKeyframes) if previousKeyframes else None
        # if there are later keyframes, find minimum, else there is none. same as last chunk but shorter
        nextFrame = min(laterKeyframes) if laterKeyframes else None

        if not previousFrame or not nextFrame:
            continue

        #quary the attribute at the given time
        previousValue = cmds.getAttr(attrFull, time = previousFrame)
        nextValue = cmds.getAttr(attrFull, time = nextFrame)

        difference = nextValue - previousValue
        weightedDifference = (difference * percentage) / 100.0
        currentValue = previousValue + weightedDifference

        cmds.setKeyframe(attrFull, time = currentTime, value = currentValue)

class TweenWindow(object):
    
    windowName = "TweenerWindow"
    
    def show(self):

        if cmds.window(self.windowName, query = True, exists = True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        #put ui
        self.buildUI()

        cmds.showWindow()


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

    def close(self, *args):
        cmds.deleteUI(self.windowName)