
# move selected mesh into the middle, export as fbx or obj, and bring it back to original location
from maya import cmds
import pymel.core as pm

pm.loadPlugin("fbxmaya") # LOAD PLUGIN

#UI Function
def main():
    
    #before adding window
    if (cmds.window('EasySave', exists = True)):    #delete window if exist
        cmds.deleteUI('EasySave', window = True)
    
    if (cmds.windowPref('EasySave', exists = True)):
        cmds.windowPref('EasySave', remove = True)    #delete previous setting
    
    #Add window
    windowwidth = 400    #width variable
    window = cmds.window('EasySave', title ='Sung\'s EasySave', iconName='ES', widthHeight=(windowwidth, 90), sizeable = False)    #window variable
    cmds.columnLayout( adjustableColumn = True )
    
    #First column ( text)
    cmds.text('Put the file path for the selected mesh', align = 'center', font = 'boldLabelFont')
    
    #Second column
    tmpRowWidth = [ windowwidth * 0.1 , windowwidth * 0.7 , windowwidth * 0.2 ]
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = tmpRowWidth, adjustableColumn = True)
    cmds.text('path')    #add text
    filepath = cmds.textFieldGrp('filepath', width = tmpRowWidth[1], editable = True)        #textfield
    cmds.button('browse', label = 'browse', width = tmpRowWidth[2], command = "browseFunction()")        #button
    cmds.setParent('..')
    
    
    #Third column
    tmpRowWidth = [ windowwidth*0.5 , windowwidth*0.5 ]
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = tmpRowWidth, adjustableColumn = True)
    cmds.button('exportFBX', label = 'Export FBX', width = tmpRowWidth[0], align = 'center' , command = 'exportFBXFunction()')
    cmds.button('exportOBJ', label = 'Export OBJ', width = tmpRowWidth[1], align = 'center' , command = 'exportOBJFunction()')
    cmds.setParent('..')
    
    #fourth column
    cmds.columnLayout( adj = True )
    alarmMessage = cmds.text('alarmMessage', label = '')
    
    #Show window
    cmds.showWindow(window)

    

#browse Function
def browseFunction():
       
    multipleFilters = 'FBX export (*.fbx) ;; OBJ export (*.obj) ;; Maya Files (*.ma, *mb) ;; Maya ASCII (*.ma) ;; All Files (*.*)'    #file filter
    chooseFile = cmds.fileDialog2(caption = 'filepath', fileMode = 0, fileFilter = multipleFilters)        # add filepath info
    filepath = cmds.textFieldGrp('filepath', edit = True , text = chooseFile[0])        #return chooseFile string
    cmds.fileInfo('filepath', filepath)



#export Function
def exportFBXFunction():

    #get FBX export save
    finalpath = cmds.textFieldGrp('filepath', q = True, text = True)        #query = question, text = answer or value
    
    #delete exist column
    if (cmds.columnLayout('messageColumn', exists = True)):    #delete column if exist
        cmds.deleteUI('messageColumn', control = True)
        
    if(cmds.text('message', exists = True)):
        cmds.deleteUI('message', control = True)
    
    
    #save files
    if finalpath != '' and cmds.ls( selection = True ):
        original = cmds.xform(cmds.ls( selection = True ),q=1,ws=1,rp=1)
        myneglist = [ -x for x in original]
        cmds.move( myneglist[0], myneglist[1], myneglist[2], cmds.ls( selection = True ), relative = True)
        new = cmds.xform(cmds.ls( selection = True ),q=1,ws=1,rp=1)
        pm.mel.FBXExport( f = finalpath, s = True )
        cmds.move( original[0], original[1], original[2], cmds.ls( selection = True ), relative = True)
        alarmMessage = cmds.text('alarmMessage', label = 'Save Completed.', backgroundColor = [0,0,1], edit = True)
        
    else:
        alarmMessage = cmds.text('alarmMessage', label = 'Save Failed. Please check if the mesh is selected and the filepath is correct.', backgroundColor = [1,0,0], edit = True)
        
        
#export Function
def exportOBJFunction():

    #get FBX export save
    finalpath = cmds.textFieldGrp('filepath', q = True, text = True)        #query = question, text = answer or value
    
    #delete exist column
    if (cmds.columnLayout('messageColumn', exists = True)):    #delete column if exist
        cmds.deleteUI('messageColumn', control = True)
        
    if(cmds.text('message', exists = True)):
        cmds.deleteUI('message', control = True)
        
    
    #save file
    if finalpath != '' and cmds.ls( selection = True ):
        original = cmds.xform(cmds.ls( selection = True ),q=1,ws=1,rp=1)
        myneglist = [ -x for x in original]
        cmds.move( myneglist[0], myneglist[1], myneglist[2], cmds.ls( selection = True ), relative = True)
        new = cmds.xform(cmds.ls( selection = True ),q=1,ws=1,rp=1)
        cmds.file(finalpath , preserveReferences = False, force = True , type = 'OBJexport' , exportSelected = True)
        cmds.move( original[0], original[1], original[2], cmds.ls( selection = True ), relative = True)
        alarmMessage = cmds.text('alarmMessage', label = 'Save Completed.', align = 'center', backgroundColor = [0,0,1], edit = True)
    
    else:
        alarmMessage = cmds.text('alarmMessage', label = 'Save Failed. Please check if the mesh is selected and the filepath is correct.', align = 'center', backgroundColor = [1,0,0], edit = True)
    
#Execution
if __name__ == '__main__':
    main()