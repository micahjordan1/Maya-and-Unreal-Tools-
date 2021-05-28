'''
READ ME

Author - Micah Jordan 
Date - 03/09/2021

Functional code - have this file along with the corresponding userSetup file saved in your Maya scripts folder (Documents/Maya/<Maya_Version>)

This tool will create a UI in Maya (called by the menu item created in userSetup) which will allow the user to export a selected camera as an FBX file.
'''

# Import statements 
import pymel.core
from PySide2 import QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI

# For creating a Maya UI
def get_maya_window():
    
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)

# Exports a new FBX file
def export_fbx_cam_anim(filename):
   
    pymel.core.loadPlugin("fbxmaya.mll", quiet = True)
    pymel.core.mel.FBXResetExport()
    pymel.core.mel.FBXExportInAscii(v = True)
    pymel.core.mel.FBXExportUpAxis("y")
    pymel.core.mel.FBXExportAnimationOnly(v = False)
    pymel.core.mel.FBXExportCameras(v = True)
    pymel.core.mel.FBXExport(s = True, f = filename)

# Selects chosen camera to be exported
def export_selected_cam_anim(camera, filename):
    
    pymel.core.select(camera, r = True)
    try:
        export_fbx_cam_anim(filename)
    except:
        pass

# Class for the ExportFBXCamera tool 
class ExportFBXCameraDialog(QtWidgets.QDialog):

    dlg_instance = None 

    @classmethod

    # Function for calling the UI
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = ExportFBXCameraDialog()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()
    
    # Initial function which will run all necessary functions
    def __init__(self):
        
        maya_main = get_maya_window()
        super(ExportFBXCameraDialog, self).__init__(maya_main)
        self.setWindowTitle("Export Camera to FBX")
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.setFixedWidth(400)
        self.setFixedHeight(100)

        self.selected_cam = pymel.core.selected()
    
    # Creates all button and texts widgets for UI
    def create_widgets(self):
        
        self.cam_text = QtWidgets.QLabel("Camera")
        self.cam_line_edit = QtWidgets.QLineEdit()
        self.cam_browse_btn = QtWidgets.QPushButton("<<")
        self.exported_file_text = QtWidgets.QLabel("Save Filename")
        self.exported_file_line_edit = QtWidgets.QLineEdit()
        self.exported_file_browse_btn = QtWidgets.QPushButton()
        self.exported_file_browse_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.run_btn = QtWidgets.QPushButton("Run")
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cam_line_edit.setReadOnly(True)
        self.exported_file_line_edit.setReadOnly(True)
        self.cam_browse_btn.setMaximumWidth(30)
        self.cam_line_edit.setMaximumWidth(260)
    
    # Creates the layout for each of the widgets
    def create_layouts(self):
        
        main_layout = QtWidgets.QVBoxLayout(self)
        cam_layout = QtWidgets.QHBoxLayout(self)
        save_layout = QtWidgets.QHBoxLayout(self)
        btn_layout = QtWidgets.QHBoxLayout(self)
        cam_layout.addWidget(self.cam_text)
        cam_layout.addWidget(self.cam_line_edit)
        cam_layout.addWidget(self.cam_browse_btn)
        save_layout.addWidget(self.exported_file_text)
        save_layout.addWidget(self.exported_file_line_edit)
        save_layout.addWidget(self.exported_file_browse_btn)
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(cam_layout)
        main_layout.addLayout(save_layout)
        main_layout.addLayout(btn_layout)
    
    # Creates the connection between buttons and their functionality 
    def create_connections(self):
        
        self.cam_browse_btn.clicked.connect(self.get_selected_object)
        self.exported_file_browse_btn.clicked.connect(self.exported_file_browse)
        self.run_btn.clicked.connect(self.export_camera)
        self.reset_btn.clicked.connect(self.clear_text)
        self.cancel_btn.clicked.connect(self.close)
    
    # Clears the text boxes
    def clear_text(self):
       
       self.cam_line_edit.setText("")
       self.exported_file_line_edit.setText("")
    
    # Allows user to choose file directory and name
    def exported_file_browse(self):
        
        exported_file = QtWidgets.QFileDialog.getSaveFileName(self, "Save as...", None, "FBX Files (*.fbx)")
        try:
            self.exported_file_line_edit.setText(exported_file[0])
        except:
            QtWidgets.QMessageBox.critical(get_maya_window(), "File error", "Path input was invalid, select a valid filepath")
    
    # Closes the UI
    def close(self):

        self.clear_text()
        super(ExportFBXCameraDialog, self).close()
    
    # Checks if correct object is selected
    def get_selected_object(self):
        
        selected = pymel.core.selected()
       
        if not selected:
            QtWidgets.QMessageBox.critical(get_maya_window(), "Selection Error", "Nothing was selected")
            return
        
        elif pymel.core.objectType (selected) == "camera":
            self.selected_cam = selected
            selected = pymel.core.selected()
            cam_parent =  pymel.core.listRelatives (selected[0], p = True)
            cam_name = "{0}".format(cam_parent[0])

            self.cam_line_edit.setText(cam_name)

        elif type(selected[0].getShape()) == pymel.core.nt.Camera:
            self.selected_cam = selected
            cam_name =  self.selected_cam[0].name()
            self.cam_line_edit.setText(cam_name)
       
        else:
            QtWidgets.QMessageBox.critical(get_maya_window(), "Node Type Error", "Selected Item was neither a camera or a transform with a camera shape.")  
    
    # Passes camera and filename to proper function for exporting
    def export_camera(self):
        
        exported_file = self.exported_file_line_edit.text()

        export_selected_cam_anim(self.selected_cam, exported_file)

        self.close()