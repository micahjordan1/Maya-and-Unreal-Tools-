'''
READ ME 

Author - Micah Jordan 
Date - 02/02/2021

Functional code - have this file and the mjordan_batchUI file saved in your Maya scripts folder (Documents/Maya/<Maya_Version>)

This tool will reference one rig file and multiple animaiton files then attach each animation to the rig. 
Each animation that is baked onto the rig will be saved as a new file. 

Import this module, and run the batch() method:

'''

# Import statement 

import pymel.core
import os

# Creating reference for file in Maya
def create_reference (file_path): 

    # Checks if given file path exists 
    if not os.path.exists(file_path): 
       
         pymel.core.error("File does not exists: {0}".format(file_path))
         return

    try:
        
        file_path = file_path.replace("\\", "/")
        
    except:
        
        pass
    
    # References in the given file 
    file_path_dir, file_path_name = os.path.split(file_path)

    file_path_filename, file_path_ext = os.path.splitext(file_path_name)

    return  pymel.core.createReference (file_path, ns = file_path_filename)

# Creating a namespace for the file 
def create_file_namespace(file_path):

    # Gets the actual file name and returns it 
    file_dir, file_full_name = os.path.split(file_path)

    file_name, file_ext = os.path.splitext(file_full_name)

    return file_name

# Create list of extra joints to avoid duplicates
def get_namespace_diff_list(src_list, dst_list):

    src_list = [item.split(":")[-1] for item in src_list]
    dst_list = [item.split(":")[-1] for item in dst_list]


    diff_list = list(set(dst_list) - set(src_list))

    return diff_list

# Connect the animation from the source to the destination 
def connect_anim (src, dst, src_ns, dst_ns): 

    diff_list = get_namespace_diff_list (src, dst)

    for src_joint in src: 

        #skipping duplicates 
        if src_joint.split(":")[-1] in diff_list:

            continue
        
        dst_joint = src_joint.replace(src_ns, dst_ns)

        # skipping joints that don't exist in rig
        if not pymel.core.objExists(dst_joint):

            continue

        pymel.core.parentConstraint(src_joint, dst_joint, mo = True)

# Bake animation to the rig
def bake_anim (objs): 
    
    
    start_time = pymel.core.playbackOptions (q = True, min = True)
    end_time = pymel.core.playbackOptions (q = True, max = True)
    
    pymel.core.select (cl = True)
    
    pymel.core.select (objs)
 
    pymel.core.bakeResults (
                        simulation = True,
                        time = (start_time, end_time),
                        sampleBy = 1,
                        oversamplingRate = 1,
                        disableImplicitControl = True,
                        preserveOutsideKeys = True,
                        sparseAnimCurveBake = False,
                        removeBakedAnimFromLayer = False,
                        bakeOnOverrideLayer = False,
                        minimizeRotation = True,
                        controlPoints = False,
                        shape = True
                       )

# Set the start and end time of the skeleton to that of the animation 
def set_to_anim_time (given_skel): 
    
    for joint in given_skel:
        
        keyframes = pymel.core.keyframe(joint, q = True)

        if keyframes:

            break

    pymel.core.playbackOptions(min = keyframes[0], e = True)
    
    pymel.core.playbackOptions(max = keyframes[-1], e = True)
   
    pymel.core.currentTime(keyframes[0])

# Given an animaton file and a rig file, animation is attached to rig and saved to given save directory
def connect_rig_to_anim(rig_path, anim_path, save_path):

    # Create a new scene
    pymel.core.newFile ( f = True)

    # Reference in character  
    rig_ref = create_reference(rig_path)

    # Reference in animation 
    anim_ref = create_reference(anim_path)

    # Get list of anim joints 
    rig_skel = pymel.core.ls(rig_ref.nodes(), type = "joint")
    anim_skel = pymel.core.ls(anim_ref.nodes(), type = "joint")

    # Set scene time to anim time 
    set_to_anim_time (anim_skel)

    # Get character file namespace 
    rig_ns = create_file_namespace(rig_path)

    # Get anim file namespace 
    anim_ns = create_file_namespace(anim_path)
    
    # Attach 1 animation to character 
    connect_anim (anim_skel, rig_skel, anim_ns, rig_ns) 

    # Bake animation on char rig
    bake_anim (rig_skel)

    # Remove animation reference 
    anim_ref.remove()

    # Save file 
    pymel.core.renameFile (save_path)
    pymel.core.saveFile (f = True)

# Takes a given list of animaiton files, attaches each one to a given rig, and saves them all to the save directory 
def batch(rig_path, anim_dir, save_dir): 

    # Error check each path 
    if not os.path.exists(rig_path):

        pymel.core.error("File does not exist: {0}".format(char_path))

        return
    
    if not os.path.exists(anim_dir):
    
        pymel.core.error("Directory does not exist: {0}".format(anim_dir))

        full_anim_path = os.path.join(anim_dir,anim_file)

        return

    if not os.path.exists(save_dir):

        print("Creating directory: {0}".format(save_dir))
        os.makedirs(save_dir)
   
    # Loop through all files and connect animation 
    for anim_file in os.listdir(anim_dir):

        # Generate a save name
        save_file = os.path.join(save_dir, anim_file.replace(".ma", "_Character.ma"))

        # Get full anim file path 
        full_anim_path = os.path.join (anim_dir,anim_file)

        # Connect the rig to the animation
        connect_rig_to_anim(rig_path, full_anim_path , save_file)
       




