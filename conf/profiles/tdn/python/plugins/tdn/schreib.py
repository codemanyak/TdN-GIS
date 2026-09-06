# encoding: utf-8
#-----------------------------------------------------------
# Autor
# Claas Leiner GKG
#
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
from qgis.core import *
from qgis.gui import *
import qgis.utils

from qgis.PyQt.QtWidgets import QApplication, QWidget, QAction, QMessageBox, QInputDialog, QLineEdit, QDockWidget


class schreib:
    # Daten schreiben Funktion
    def schreib(self):
        vlayer = qgis.utils.iface.activeLayer()
        buff = vlayer.editBuffer()
        if vlayer.isEditable() == False  or vlayer.isModified() == False:
            if vlayer.isModified() == False:
                qgis.utils.iface.vectorLayerTools().stopEditing(vlayer)
                qgis.utils.iface.messageBar().pushInfo('Info','Nichts zu ändern')
            else:
                qgis.utils.iface.vectorLayerTools().stopEditing(vlayer)
                qgis.utils.iface.messageBar().pushInfo('Info','Nichts zu ändern')
        
        else:        
            mb = QMessageBox()
            mb.setText('Änderungen speichern?')
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            return_value = mb.exec()
            if return_value == QMessageBox.Ok:
                #Änderungen schreiben
                buff = vlayer.editBuffer()
                
                if vlayer.isModified() == False: #buff == None:
                    qgis.utils.iface.vectorLayerTools().stopEditing(vlayer)
                    qgis.utils.iface.messageBar().pushInfo('Info','Nichts zu ändern')
                    
                else:            
                    #aend = buff.changedGeometries()
                    #hinzu = buff.addedFeatures()
                
                    #ae_list = list(aend.keys())
                    #hinzu_list = list(hinzu.keys())
                
                    #objekte = vlayer.getFeatures() 
                    
                    vlayer.commitChanges()
                    qgis.utils.iface.vectorLayerTools().stopEditing(vlayer)
                    qgis.utils.iface.messageBar().pushInfo('Info','Änderungen geschrieben')
                
            elif return_value == QMessageBox.Cancel:
                buff = vlayer.editBuffer()
                if buff == None:
                    qgis.utils.iface.messageBar().pushInfo('Info','Nichts zu ändern')
                    #vlayer.commitChanges()
                    qgis.utils.iface.vectorLayerTools().stopEditing(vlayer)
                
                else:
                    qgis.utils.iface.actionRollbackEdits().trigger()
                    #vlayer.commitChanges()
                    qgis.utils.iface.vectorLayerTools().stopEditing(vlayer)
                    qgis.utils.iface.messageBar().pushInfo('Info','Änderungen aufgehoben')

            
