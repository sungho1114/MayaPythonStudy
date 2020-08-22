import pprint
from maya import cmds
import controllerLibrary
from PySide2 import QtWidgets, QtCore, QtGui
reload(controllerLibrary)



class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The ControllerLibraryUI is a dialogue that lets us save and import controllers
    """

    def __init__(self):
        # super finds all function even though the class change
        # QtWidgets.QDialog.__init__(self) looks better, but hard to change
        super(ControllerLibraryUI, self).__init__()

        # The library variable points to an instance of our controller library
        self.setWindowTitle('Controller Library UI')
        self.library = controllerLibrary.ControllerLibrary()

        # Everytime we create a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """
        This method builds out the UI
        """
        # This is the master layout
        layout = QtWidgets.QVBoxLayout(self)

        # This is the child horizontal widgets
        # add horizontal line
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        # top Layout
        # Name Field
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        # Save Button
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # These are the parameters for our thumbnail size
        # add mesh box (view in icon mode)
        size = 80
        buffer = 12

        # This will create a grid list widget to display our controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)     #icon mode
        self.listWidget.setIconSize(QtCore.QSize(size, size))       # icon size
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)     # make the window size adjustable
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))     # give a gab between icons
        layout.addWidget(self.listWidget)

        # This is our child widget that holds all the buttons
        # bottom layout
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        # import button
        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        #delete button
        deleteBtn = QtWidgets.QPushButton('Delete')
        deleteBtn.clicked.connect(self.delete)
        btnLayout.addWidget(deleteBtn)

        # refresh button
        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)       # connect to populate function
        btnLayout.addWidget(refreshBtn)

        # close button
        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)        # connect to close (QDialogue)
        btnLayout.addWidget(closeBtn)



    def populate(self):
        """ This clears the listWidget and then repopulates it with the contents of our library """
        self.listWidget.clear()     # clear all the contents
        self.library.find()

        # list items on the box
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            # show screenshot
            screenshot = info.get('screenshot')
            #print(screenshot)
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)


            # formating text
            item.setToolTip(pprint.pformat(info))


    def load(self):
        """ This loads the currently selected controller"""
        #give current selected Item
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)


    def save(self):
        """ This saves the controller with the given file name """
        name = self.saveNameField.text()

        # after strip the name and it doesn't exist
        if not name.strip():
            cmds.warning("You must give a name.")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')


    def delete(self):
        """ This deletes the controller with the given file name """
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            cmds.warning("You must choose a file.")
            return

        name = currentItem.text()
        self.library.delete(name)
        self.populate()


def showUI():
    """
    This shows and returns a handle to the ui
    Returns:
        QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui

