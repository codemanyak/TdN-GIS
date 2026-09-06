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


class verz:
    # Daten schreiben Funktion
    def verz(self,met):
        jar = datetime.now().strftime('%Y')
        mon = datetime.now().strftime('%Y_%m')
        dat = datetime.now().strftime('%Y_%m_%d')
        # Nutzerverzeichnis  initiieren
        nutzer = getpass.getuser()
        nutzer_vz_such = os.path.normcase(QgsProject.instance().readPath("./") + '/Ausgabe/'   + jar + '/' + mon + '/'  + dat + '/')
        #nutzer_vz_ar = os.path.normcase(QgsProject.instance().readPath("./") + '/Ausgabe/' + jar + '/' + mon + '/'  + dat + '/')
        expv_such = nutzer_vz_such
        #expv_ar = nutzer_vz_ar

        
        if met == such:
            if not os.path.exists(expv_such):
                os.makedirs(expv_ar)
            expv = expv_such
        
        #elif met == arb:
            #if not os.path.exists(expv_ar):
                #os.makedirs(expv_ar)
            #expv = expv_ar
            
        return expv
            

            
