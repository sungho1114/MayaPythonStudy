#object Renamer
from maya import cmds

#dictionary
SUFFIXES = {
    "mesh" : "geo",
    "joint" : "jnt",
    "camera" : None,
    "ambientLight" : "lgt"
}

DEFAULT_SUFFIX = "grp"

def rename(selection = False):
    """

    This function will rename any objects to have the correct suffix
    Args:
        selection:  Whether or not we use the current selection

    Return:
        A list of all the objects we operated on

    """
            
    objects = cmds.ls(selection = selection, dag = True, long = True)    # ls return object name?
    
    # This fuction runs if selection is true, but object is false
    if selection and not objects:
        raise RuntimeError("You have not select anything")

    objects.sort(key = len, reverse = True)

    # This function prints all separate and print the last one
    for obj in objects:
        shortName = obj.split("|")[-1]
    
        # get list, but get empty list if it is none
        children = cmds.listRelatives(obj, children = True, fullPath = True) or []

        # find the type of elements
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)
    
        #find all suffixes through dictionary
        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)
        
        #camera exception
        if not suffix:
            continue

        # if suffix exists already, skip renaming
        if obj.endswith("_" + suffix):
            continue

        
        newName = "%s_%s" %(shortName, suffix)
    
        cmds.rename(obj, newName)
        
        index = objects.index(obj)
        objects[index] = obj.replace(shortName, new)

    return objects