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

from datetime import date
from datetime import datetime
import getpass

import os   # Module für den zugriff aus Dateisystem laden
import sys

from qgis.PyQt.QtWidgets import QApplication, QWidget, QAction, QMessageBox, QInputDialog, QLineEdit, QDockWidget


class ver:
    # Daten schreiben Funktion
    def ver(self):
        
        jar = datetime.now().strftime('%Y')
        mon = datetime.now().strftime('%Y_%m')
        dat = datetime.now().strftime('%Y_%m_%d')
        # Nutzerverzeichnis  initiieren
        nutzer = getpass.getuser()
        #nutzer_vz_such = os.path.normcase(QgsProject.instance().readPath("./") + '/Ausgabe/'   + jar + '/' + mon + '/'  + dat + '/')
        nutzer_vz_such = os.path.normcase(QgsProject.instance().homePath() )
        proj_verz =  os.path.normcase(QgsProject.instance().homePath()+ '/')
        
        expv = nutzer_vz_such
        nam = os.path.splitext(os.path.split(QgsProject.instance().absoluteFilePath())[1])[0]
            
        return expv, nam
        
                 
