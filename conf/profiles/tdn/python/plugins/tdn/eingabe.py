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
from PyQt5 import QtWidgets
from qgis.PyQt.QtWidgets import QApplication, QWidget, QAction, QMessageBox, QInputDialog, QLineEdit, QDockWidget


class eingabe:
        
    def ein(self):
        qid = QInputDialog()
        title = "Route eingeben"
        label = "Gesuchte Route oder wabe"
        mode = QLineEdit.Normal
        default = ""
        inp, ok = QInputDialog.getText(qid, title, label, mode, default) # Eingebenen Verzeichnispfad mit O.K in die Variable inp
        
        if ok:
            bezeichner = inp 
            return bezeichner
        else:
            bezeichner = '' 
            return bezeichner
