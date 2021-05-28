'''
Author - Micah Jordan 
Date - 03/09/2021

Functional code - have this file along with the mjordan_fbx_export_camera_animation saved in your Maya scripts folder (Documents/Maya/<Maya_Version>)

This tool will call the UI from the corresponding file in Maya by using a customized menu item. This will allow the user to export a selected camera as an FBX file.
'''

# Import statements 
import os, inspect, sys
import maya.cmds, maya.mel
import maya.OpenMaya

# Creates a menu item in Maya for the ExportFBXCamera UI
def create_custom_menu(): 

    menu_name = "export_cam"
    maya.cmds.menu(menu_name, label = "Export Cam", parent = "MayaWindow", tearOff = True)
    maya.cmds.menuItem(parent = menu_name, divider = True)
    maya.cmds.menuItem(parent = menu_name, 
                        label = "Export Camera Animation",
                        command = call_export_cam_animation, 
                        annotation = "Exports selected camera to FBX file")

# Function that imports UI file and calls the function to show it   
def call_export_cam_animation(*args):

    import mjordan_fbx_export_camera_animation
    mjordan_fbx_export_camera_animation.ExportFBXCameraDialog.show_dialog()

maya.cmds.evalDeferred("create_custom_menu()")