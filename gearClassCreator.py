from maya import cmds

class Gear(object):
    """
    This is a gear object that lets us create and modify a gear
    """
    def __init__(self):
        
        #the __init__ method lets us set default values
        self.transform = None
        self.extrude = None
        self.constructor = None
    
    def createGear(self, teeth = 10, length = 1):
        
        """
        This function will create a gear with the given parameters
        Args:
            teeth: the number of teeth to create
            length: the length of the teeth
                
        Returns:
            A tuple of the transform, constructor, and extrude node
        """
        
        spans = teeth * 2
        
        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis = spans)
        
        sideFaces = range(spans*2, spans*3, 2)
        
        cmds.select(clear = True)
        
        for face in sideFaces:
            cmds.select("%s.f[%s]" % (self.transform, face), add = True)
            
        self.extrude = cmds.polyExtrudeFacet(localTranslateZ = length)[0]
        #return transform, constructor, extrude
    
        
    def changeTeeth(self, teeth = 10, length = 1):
        spans = teeth * 2
        
        cmds.polyPipe(self.constructor, edit = True, subdivisionsAxis = spans)
        
        sideFaces = range(spans * 2, spans * 3, 2)
        faceNames = []
        
        for face in sideFaces:
            faceName = 'f[%s]' %(face)
            faceNames.append(faceName)
        #expend list instead of give list,
        cmds.setAttr('%s.inputComponents' %(self.extrude), len(faceNames), *faceNames, type = "componentList")
        
        cmds.polyExtrudeFacet(self.extrude, edit = True, localTranslateZ = length)
        
        cmds.select(clear = True)
        