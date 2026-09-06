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
import os   # Module für den zugriff aus Dateisystem laden
import sys
from sys import platform
from qgis.core import QgsProject
import qgis.utils
from .ver import ver as v
import subprocess


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QLabel, QDockWidget, QProgressBar, QAction, QMessageBox, QDialog, QVBoxLayout,QComboBox, QRadioButton,QHBoxLayout,QScrollArea,QCheckBox,QDialogButtonBox


class weg_folge:
    
    def wege_waehlen(self,items):
        """
        Erzeugt einen scrollbaren Checkbox-Dialog aus einer Liste.

        :param items: Liste von Strings
        :param title: Fenstertitel
        :param parent: Parent-Widget (z.B. iface.mainWindow())
        :param prechecked: optionale Liste vorausgewählter Einträge
        :return: Liste ausgewählter Einträge oder None bei Abbruch
        """
        #dialog = QDialog(parent)
        dialog = QDialog()
        dialog.setWindowTitle('Etappenabschnitte  wählen')
        dialog.resize(350, 510)

        main_layout = QVBoxLayout(dialog)

        # ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        checkboxes = []

        for item in items:
            cb = QCheckBox(str(item))
            cb.setProperty("filter_text", str(item).lower())
            scroll_layout.addWidget(cb)
            checkboxes.append(cb)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        # OK / Cancel Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        main_layout.addWidget(button_box)
            
        # Alle wählen
        select_all = QCheckBox("Alle auswählen")
        select_all.stateChanged.connect(
            lambda state: [
                cb.setChecked(state)
                for cb in checkboxes
            ]
        )
        main_layout.insertWidget(0, select_all)
            
        # Filerung
        # Filterfunktion
        # Suchfeld
        search_box = QLineEdit()
        search_box.setPlaceholderText("Suchen …")
        main_layout.addWidget(search_box)

        def filter_checkboxes(text):
            text = text.lower()
            for cb in checkboxes:
                filter_text = cb.property("filter_text") or ""
                cb.setVisible(text in filter_text)

        search_box.textChanged.connect(
            lambda text: filter_checkboxes(text)
        )

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            return [
                cb.text()
                for cb in checkboxes
                if cb.isChecked()
            ]
        else:
            return None
        
    def show_message(self,message):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(message)
            msg_box.setWindowTitle("Info")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
    
    def wfl(self):
        import re
        # Laxer definieren
        #tabelle =  QgsProject.instance().mapLayersByName("richtungs_folge")[0] # tabelle mit sämtlicne Layernamen
        etap =   QgsProject.instance().mapLayersByName("richtungs_folge")[0]    # Der Layer mit sämtlichen Routen  
        etap_name = etap.name()

        wegeliste = []
        for feat in etap.getFeatures():
            wegeliste.append(feat['etappe'])
        
        wegeliste = list(set(wegeliste))
       
        wegeliste.sort()
        
        wegnamen = []
        
        # Export-Pfade festlegen
        pdfv = v.ver(self)[0]
        print(pdfv)
        if not os.path.exists(pdfv + '/Wegbeschreibungen'):
            os.makedirs(pdfv + '/Wegbeschreibungen')
        pad = os.path.normpath(pdfv + '/Wegbeschreibungen')
        print(pad)
        
        
        
        def exkwr(pad,lay,lay_name,dat_name):  # sel 0 True or False für die Verarbeitung nur gewählter Layer
            layer = lay
            #path = pad + "/" + name + '.xlsx'
            path = pad + '/' + dat_name + '.xlsx'
            
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.layerName = lay_name
            options.driverName = 'XLSX'
            options.fileEncoding = 'utf-8'
            options.onlySelectedFeatures = True
            options.attributes = [3,2,14,18,15,16,17,13,12,10,5,6] 
            print(options)
            writer = QgsVectorFileWriter.writeAsVectorFormatV3(layer,path,QgsProject.instance().transformContext(),options)       
            return writer, path
        
        wegenamen = self.wege_waehlen(wegeliste)
     
        try:
            #exkwr(pad,lay,lay_name,dat_name)
            
            weg_namen = [''] # Die List der Wegnamen, die aus der Auswajl in der Tabelle erzeugt wird
            weg_features = []
            
            for ele in wegenamen:
                etap.selectByExpression('"etappe" = ' + "'" + ele + "'" +'')
                print('"etappe" = ' + "'" + ele + "'" +'')
                exkwr(pad,etap,etap_name,'tdn2026_richtfolge_' + ele)
            
            print(etap)
            print(pad)
            print(wegenamen[0] )
            
            if platform == "linux":
                subprocess.call(["xdg-open", pad])
                #subprocess.call(["xdg-open", pfad])
            elif platform == "darwin":
                subprocess.call(["open", pad])
            elif platform == "win32":
                try:
                    os.system("start "+ pad)
                    #os.system("start "+ pfad)
                except:
                    pass
            self.show_message('Tabellen erstellt')
            
        except:
            self.show_message('Keine Eingabe')
        
        
