from maya import cmds


#main UI function
def main():
    
    #delete exist window
    if cmds.window('myWin', exists = True):
        cmds.deleteUI('myWin', window = True)
    if (cmds.windowPref('myWin', exists = True)):
        cmds.windowPref('myWin', remove = True)
        
    #window Size Variable
    winWid = 500
    winHei = 270  
    myWin = cmds.window('myWin', title = 'Sung\'s Easy Rotator', widthHeight = [winWid,winHei], s = False)
        
    #window first Column
    cmds.columnLayout( adj = True )
    cmds.separator( h = 10 )
    cmds.text( label = 'Welcome to Rotator.', fn = 'boldLabelFont', ww = True )
    cmds.separator( h = 10 )
    cmds.text( label = 'X Axis', fn = 'boldLabelFont', ww = True )
    cmds.setParent('..')
    
    #XAxis
    tmpRowWidth = [winWid*0.1, winWid*0.75, winWid*0.15]
    cmds.rowLayout( nc = 3, cw3 = tmpRowWidth )
    cmds.text(label = 'Rotate', w = tmpRowWidth[0])
    cmds.intSliderGrp('XSlide', min = -180, max = 180, field = True, w = tmpRowWidth[1] )
    cmds.button('Rotate', w = tmpRowWidth[2], c = 'rotate(cmds.intSliderGrp(\'XSlide\', q=True, v=True),0,0)')
    cmds.setParent('..')
    
    tmpRowWidth = [winWid*0.25, winWid*0.25, winWid*0.25, winWid*0.25]
    cmds.rowLayout( nc = 4, cw4 = tmpRowWidth )
    cmds.button('rotateX-180', label = '-180', al = 'center', w = tmpRowWidth[0], c = 'rotate(-180,0,0)')
    cmds.button('rotateX-90', label = '-90', al = 'center', w = tmpRowWidth[1], c = 'rotate(-90,0,0)')
    cmds.button('rotateX90', label = '90', al = 'center', w = tmpRowWidth[2], c = 'rotate(90,0,0)')
    cmds.button('rotateX180', label = '180', al = 'center', w = tmpRowWidth[3], c = 'rotate(180,0,0)')
    cmds.setParent('..')
    
    cmds.columnLayout( adj = True )
    cmds.separator( h = 10 )
    cmds.text( label = 'Y Axis', fn = 'boldLabelFont', ww = True )
    cmds.setParent('..')
    
    #YAxis
    tmpRowWidth = [winWid*0.1, winWid*0.75, winWid*0.15]
    cmds.rowLayout( nc = 3, cw3 = tmpRowWidth )
    cmds.text(label = 'Rotate', w = tmpRowWidth[0])
    cmds.intSliderGrp('YSlide', min = -180, max = 180, field = True, w = tmpRowWidth[1] )
    cmds.button('Rotate', w = tmpRowWidth[2], c = 'rotate(0,cmds.intSliderGrp(\'YSlide\', q=True, v=True),0)')
    cmds.setParent('..')
    
    tmpRowWidth = [winWid*0.25, winWid*0.25, winWid*0.25, winWid*0.25]
    cmds.rowLayout( nc = 4, cw4 = tmpRowWidth )
    cmds.button('rotateY-180', label = '-180', al = 'center', w = tmpRowWidth[0], c = 'rotate(0,-180,0)')
    cmds.button('rotateY-90', label = '-90', al = 'center', w = tmpRowWidth[1], c = 'rotate(0,-90,0)')
    cmds.button('rotateY90', label = '90', al = 'center', w = tmpRowWidth[2], c = 'rotate(0,90,0)')
    cmds.button('rotateY180', label = '180', al = 'center', w = tmpRowWidth[3], c = 'rotate(0,180,0)')
    cmds.setParent('..')
    
    cmds.columnLayout( adj = True )
    cmds.separator( h = 10 )
    cmds.text( label = 'Z Axis', fn = 'boldLabelFont', ww = True )
    cmds.setParent('..')
    
    #ZAxis
    tmpRowWidth = [winWid*0.1, winWid*0.75, winWid*0.15]
    cmds.rowLayout( nc = 3, cw3 = tmpRowWidth )
    cmds.text(label = 'Rotate', w = tmpRowWidth[0])
    cmds.intSliderGrp('ZSlide', min = -180, max = 180, field = True, w = tmpRowWidth[1] )
    cmds.button('Rotate', w = tmpRowWidth[2], c = 'rotate(0,0,cmds.intSliderGrp(\'ZSlide\', q=True, v=True))')
    cmds.setParent('..')
    
    tmpRowWidth = [winWid*0.25, winWid*0.25, winWid*0.25, winWid*0.25]
    cmds.rowLayout( nc = 4, cw4 = tmpRowWidth )
    cmds.button('rotateZ-180', label = '-180', al = 'center', w = tmpRowWidth[0], c = 'rotate(0,0,-180)')
    cmds.button('rotateZ-90', label = '-90', al = 'center', w = tmpRowWidth[1], c = 'rotate(0,0,-90)')
    cmds.button('rotateZ90', label = '90', al = 'center', w = tmpRowWidth[2], c = 'rotate(0,0,90)')
    cmds.button('rotateZ180', label = '180', al = 'center', w = tmpRowWidth[3], c = 'rotate(0,0,180)')
    cmds.setParent('..')
    
    cmds.columnLayout( adj = True )
    cmds.separator( h = 10 )
    cmds.setParent('..')

    
    cmds.showWindow(myWin)



#---------------------------------------------------------------------------------------------------------------------------------------------------



#button
def rotate(Xnum,Ynum,Znum):
    OldTrans = cmds.xform(cmds.ls(selection = True),q=1,ra=1)
    NewTrans = [Xnum,Ynum,Znum]
    cmds.rotate( OldTrans[0] + NewTrans[0], OldTrans[1] + NewTrans[1], OldTrans[2] + NewTrans[2], cmds.ls( selection = True ), relative = True)




#---------------------------------------------------------------------------------------------------------------------------------------------------



#Execution
if __name__ == '__main__':
    main()