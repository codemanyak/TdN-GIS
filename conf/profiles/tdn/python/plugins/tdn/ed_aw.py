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

import os   # Module für den zugriff aus Dateisystem laden
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QDockWidget, QProgressBar, QAction, QMessageBox, QDialog, QVBoxLayout,QComboBox, QRadioButton,QHBoxLayout, QPushButton


class ed_aw:
    def ed_aw(self):
        dialog = QDialog()
        dialog.setWindowTitle("Welche Ebene bearbeiten?")
        
        layout = QVBoxLayout()
        label = QLabel("Welche Ebene bearbeiten?")
        layout.addWidget(label)

        # Radio-Buttons hinzufügen
        radio_button1 = QRadioButton("Skizze")
        radio_button2 = QRadioButton("StreckenPlan")

        # Standardmäßig den ersten Radio-Button auswählen
        radio_button1.setChecked(True)

        layout.addWidget(radio_button1)
        layout.addWidget(radio_button2)

        #button = QPushButton("OK")
        #layout.addWidget(button)
            
        # OK- und Abbrechen-Buttons hinzufügen
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Abbrechen")
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)    

        def on_ok_button_clicked():
            dialog.accept()
                
        def on_cancel_button_clicked():
            dialog.reject()

        #button.clicked.connect(on_button_clicked)
        ok_button.clicked.connect(on_ok_button_clicked)
        cancel_button.clicked.connect(on_cancel_button_clicked)

        dialog.setLayout(layout)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            if radio_button1.isChecked():
                wahl = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
            elif radio_button2.isChecked():
                wahl = QgsProject.instance().mapLayersByName("StreckenPlan")[0]
            else:
                wahl = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
        else:
            wahl = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
                
        return wahl

