from maya import cmds
import warnings
import os  # operating system
import json  # write data
import pprint  # easier to read code

# find maya directory
USERAPPDIR = cmds.internalVar(userAppDir=True)
# os specific setting
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')

def createDirectory(directory = DIRECTORY):
    """
    Creates the given directory if it doesn't exist already
    Args:
        directory (str): The directory to create

        """
    # check path existence
    if not os.path.exists(directory):
        os.mkdir(directory)


class ControllerLibrary(dict):
    """
    This is a class to find, save, and load controllers. It stores its' data in a dictionary
    """
    #info = automatically store other inputs
    def save(self, name, directory = DIRECTORY, screenshot = True, **info):
        """
        Save out a controller to a location on a disk
        Args:
            name(str): the name to save the controller as
            directory(str): the directory to save the controller to. defaults to user directory
            screenshot(bool): whether to save a screenshot or not
            **info: any arbitrary info that needs to be saved with the controller

        Returns:
            str: The path to the file that was saved out

        """
        createDirectory(directory)

        # path to save the file
        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        cmds.file(rename = path)

        if cmds.ls(selection = True):
            cmds.file(force = True, type = 'mayaAscii', exportSelected = True)
        else:
            cmds.file(save = True, type = 'mayaAscii', force = True)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory = directory)

        # with open file in write mode in a temporary variable f.
        with open(infoFile, 'w') as f:
            json.dump(info, f, indent = 4)

        #update everytime
        self[name] = info

    def find(self, directory = DIRECTORY):
        """
        Finds controllers on disk
        Args:
            directory: The directory to search in

        """
        self.clear()
        #check if path exists, if not, donot play
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        """
        mayaFiles = []
        for f in files:
            if f.endswith('.ma'):
                mayaFiles.append(f)
        """
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            infoFile = '%s.json' % name

            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)

            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, name)
            else:
                screenshot = 'defaultImage.jpg'
                info['screenshot'] = os.path.join(directory, 'defaultImage')

            info['name'] = name
            info['path'] = path

            # put path and item together
            self[name] = info


    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i = True, usingNamespaces = False)

    def saveScreenshot(self, name, directory = DIRECTORY):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename = path, forceOverwrite = True, format = 'image', width = 200, height = 200, showOrnaments = False, startTime = 1, endTime = 1, viewer = False)

        return path

    def delete(self, name):
        #Variable for files
        path = self[name]['path']
        infoFile = path.replace('%s.ma' % name , '%s.json' % name)
        imageFile = path.replace('%s.ma' % name , '%s.jpg' % name)

        os.remove(path) if path else None
        os.remove(infoFile) if infoFile else None
        os.remove(imageFile) if imageFile else None