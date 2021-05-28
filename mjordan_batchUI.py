'''
READ ME 

Author - Micah Jordan 
Date - 02/09/2021

Functional code - have this file and the mjordan_batch_anim_tool file saved in your Maya scripts folder (Documents/Maya/<Maya_Version>)

This tool will create a UI in Maya which will allow the user to bake multiple animations onto one character rig. 
The user will choose one rig file, one directory with animation files, and one directory to save the baked animations to.  

Use the following code:

import mjordan_batchUI

try:
    
    ui_obj.close()
    ui_obj.deleteLater()
    
except:
    
    pass
    
ui_obj = BatchDialogue()
ui_obj.show()

'''

# Import statements

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI
import pymel.core
import os
import mjordan_batch_anim_tool

# For creating a Maya UI
def get_maya_window():
    
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)

# Class for the batchUI tool 
class BatchDialogue (QtWidgets.QDialog):

    # Initial function which will run all necessary functions
    def __init__ (self): 

        maya_main = get_maya_window()
        
        super(BatchDialogue, self).__init__(maya_main)
        
        self.setWindowTitle("Batch Animation")
        
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)

        self.anim_dir = ""
        self.rig_file = ""
        self.save_dir = ""

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    # Creates all button and texts widgets for UI
    def create_widgets(self):
        
        self.anim_dir_text = QtWidgets.QLabel()
        self.rig_file_text = QtWidgets.QLabel()
        self.save_dir_text = QtWidgets.QLabel()

        self.anim_dir_btn = QtWidgets.QPushButton("Animation Directory")
        self.rig_dir_btn = QtWidgets.QPushButton("Rig Directory")
        self.save_dir_btn = QtWidgets.QPushButton("Save Directory")

        self.run_btn = QtWidgets.QPushButton("Run")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
        self.anim_dir_text.setAlignment(QtCore.Qt.AlignVCenter)
        self.rig_file_text.setAlignment(QtCore.Qt.AlignVCenter)
        self.save_dir_text.setAlignment(QtCore.Qt.AlignVCenter)

    # Creates the layout for each of the widgets
    def create_layouts(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        btn_layout = QtWidgets.QHBoxLayout (self)

        main_layout.addWidget(self.anim_dir_btn)
        main_layout.addWidget(self.anim_dir_text)
    
        main_layout.addWidget(self.rig_dir_btn)
        main_layout.addWidget(self.rig_file_text)
       
        main_layout.addWidget(self.save_dir_btn)
        main_layout.addWidget(self.save_dir_text)
        
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

    # Creates the connection between buttons and their functionality 
    def create_connections(self):

        self.anim_dir_btn.clicked.connect(self.get_anim_directory)
        self.rig_dir_btn.clicked.connect(self.get_file)
        self.save_dir_btn.clicked.connect(self.get_save_directory)

        self.run_btn.clicked.connect(self.run_batch)
        self.cancel_btn.clicked.connect(self.close)

    # For selecting an animation directory 
    def get_anim_directory(self):

        dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.anim_dir_text.setText(dir)

        BatchDialogue.anim_dir = dir

    # For selecting a rig file 
    def get_file(self):

        file_path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.rig_file_text.setText(file_path)

        BatchDialogue.rig_file = file_path
  
    
    # For selecting a save directory 
    def get_save_directory(self):

        dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.save_dir_text.setText(dir)

        BatchDialogue.save_dir = dir

    # Runs the batch tool from mjordan_batch_anim_tool
    def run_batch (self):

        if not os.path.exists(self.rig_file):

         pymel.core.error("File does not exist: {0}".format(BatchDialogue.rig_file))

         return

        if not os.path.exists(self.anim_dir):

         pymel.core.error("File does not exist: {0}".format(BatchDialogue.anim_dir))

         return

        if not os.path.exists(self.save_dir):

         pymel.core.error("File does not exist: {0}".format(BatchDialogue.save_dir))

         return

        mjordan_batch_anim_tool.batch(BatchDialogue.rig_file, BatchDialogue.anim_dir, BatchDialogue.save_dir)