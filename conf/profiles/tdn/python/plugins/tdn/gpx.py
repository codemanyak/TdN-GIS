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
from qgis.core import QgsProject,QgsFeatureRequest,QgsVectorFileWriter,QgsCoordinateTransform,QgsCoordinateReferenceSystem
import qgis.utils
from .ver import ver as v
import subprocess


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QLabel, QDockWidget, QProgressBar, QAction, QMessageBox, QDialog, QVBoxLayout,QComboBox, QRadioButton,QHBoxLayout,QScrollArea,QCheckBox,QDialogButtonBox


class gpx_aus:
    
    # Schnell Druck
    def gpx_exp(self):
        
        import processing
        
        # Auswahlmenü
        def AuswahlMenue():
            dialog = QDialog()
            dialog.setWindowTitle("Strecken oder Punkte ausgeben?")

            layout = QVBoxLayout()

            label = QLabel("Strecken oder Punkte ausgeben?")
            layout.addWidget(label)

            # Radio-Buttons hinzufügen
            radio_button1 = QRadioButton("Strecken-Abschnitte")
            radio_button3 = QRadioButton("Strecken-Tage")
            radio_button2 = QRadioButton("Punkte")
            #radio_button3 = QRadioButton("Dummy")

            # Standardmäßig den ersten Radio-Button auswählen
            radio_button1.setChecked(True)

            layout.addWidget(radio_button1)
            layout.addWidget(radio_button3)
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
                    wahl = "Strecken-Abschnitte"
                elif radio_button2.isChecked():
                    wahl = "Punkte"
                elif radio_button3.isChecked():
                    wahl = "Strecken-Tage"
                else:
                    wahl = 'ohne'
            else:
                wahl = 'ohne'
                
            return wahl

        # Beispiel: Öffnen Sie den Dialog aus einem QGIS-Plugin oder einem Skript

        wahl = AuswahlMenue()        

        if wahl != 'ohne':
                
            vlayer = QgsProject.instance().mapLayersByName("Etappen")[0]
            et_list = []
            objekte = vlayer.getFeatures()
            for feature in objekte:
                if feature["fahrt"] == 1:
                    print(feature["bezeichnung"])
                    wert = feature["bezeichnung"]
                    et_list.append(wert)
            et_list.append('01 Sämtliche')
            et_list.sort()
            #Auswahlmenü Routen 
            def AuswahlMenue():
                dialog = QDialog()
                dialog.setWindowTitle("Für welche Etappen?")

                layout = QVBoxLayout()

                label = QLabel("Für welche Etappen?")
                layout.addWidget(label)

                combo_box = QComboBox()
                combo_box.addItems(et_list)
                layout.addWidget(combo_box)

                button = QPushButton("OK")
                layout.addWidget(button)

                def on_button_clicked():
                    dialog.accept()

                button.clicked.connect(on_button_clicked)

                dialog.setLayout(layout)

                result = dialog.exec_()

                if result == QDialog.Accepted:
                    selected_value = combo_box.currentText()
                    strecke = selected_value
                    return strecke
                    # Hier können Sie den ausgewählten Wert weiterverarbeiten
                    # Zum Beispiel: Ein Attribut eines Layers setzen, etc.

            # Beispiel: Öffnen Sie den Dialog aus einem QGIS-Plugin oder einem Skript
            strecke = AuswahlMenue()
            print(wahl)
            print(strecke)        
        
        if wahl == 'Strecken-Abschnitte':
            dlayer = QgsProject.instance().mapLayersByName("StreckenPlan")[0]
            gpx = 'Strecken-Abschnitte'
        elif wahl == 'Strecken-Tage':
            dlayer = QgsProject.instance().mapLayersByName("StreckenPlan")[0]
            gpx = 'Strecken-Tage'
        elif wahl == 'Punkte':
            dlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
            gpx = 'Punkte'
        elif wahl == 'ohne':
            dlayer = None
            gpx = None
        
        if dlayer != None:
            
            if strecke == '01 Sämtliche':
                dlayer = dlayer
            
            else:              
                dlayer.selectByExpression("\"etappen_bezeichnung\"= '" + strecke +"'")
                seiten = dlayer.materialize(QgsFeatureRequest().setFilterFids(dlayer.selectedFeatureIds()))
                seiten.setName('gpxl')
                QgsProject.instance().addMapLayer(seiten)
                dlayer = QgsProject.instance().mapLayersByName("gpxl")[0]
            
                dlayer.startEditing()
                for objekt in dlayer.getFeatures():
                    name = objekt["name"]
                    name = name.replace("(","")
                    name_neu = name.replace(",0)","")
                    
                        
                    nam_sp_id = objekt.fields().indexOf('name')                        
                    dlayer.changeAttributeValue(objekt.id(), nam_sp_id, name_neu)
                            
                dlayer.commitChanges()
             
             
            if wahl == 'Strecken-Tage':
                
                alg_params = {
                               
                                'GROUP_BY':'"etappen_bezeichnung"',
                                'AGGREGATES':[
                                    {'aggregate': 'first_value','delimiter': ',','input': '"etappen_bezeichnung"','length': -1,'name': 'name','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}
                                    ],
                                 'INPUT':dlayer,
                                'OUTPUT':'TEMPORARY_OUTPUT'
                                    }
                n_layer = processing.run('native:aggregate', alg_params)
                dlayer2 = n_layer['OUTPUT']
                
                #megerlines
                alg_params = {
                            'INPUT':dlayer2,
                            'OUTPUT':'memory:'
                                }
                
                n_layer = processing.run("native:mergelines", alg_params)
                dlayer2 = n_layer['OUTPUT']
                
                #reparrieren
                alg_params = {
                            'METHOD':1,
                            'INPUT':dlayer2,
                            'OUTPUT':'memory:'
                                }
                
                n_layer = processing.run("native:fixgeometries", alg_params)
                dlayer2 = n_layer['OUTPUT']
                
            
            else:
                
                #Felder des neuen Weglayers ueberarbeiten
                alg_params = {
                    'FIELDS_MAPPING': 
                                [
                                    {'expression': '"name"','length': -1,'name': 'name','precision': 0,'type': 10}
                                ],
                        'INPUT': dlayer,
                        'OUTPUT': 'memory:'
                        }
                n_layer = processing.run('native:refactorfields', alg_params)
                dlayer2 = n_layer['OUTPUT']
                
                #dlayer.selectByExpression("\"etappen_bezeichnung\"= '" + strecke +"'")      
                #objekte = dlayer.selectedFeatures()
                
            
        else:
            objekte = None
        print(objekte)
        
        def vekwr(form,pad,lay,name,sel):  # sel 0 True or False für die Verarbeitung nur gewählter Layer
            layer = lay
            if form == 'shp':
                path = pad + "/" + name + '.shp'
                writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='ESRI Shapefile', onlySelected=sel,layerOptions= ['SPATIAL_INDEX=YES'])
            elif form == 'gpkg':
                path = pad + "/" + name + '.gpkg'
                writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='GPKG', onlySelected=sel,layerOptions= ['SPATIAL_INDEX=YES'])
            elif form == 'gpx':
                path = pad + "/" + name + '.gpx'
                writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='GPX', onlySelected=sel,datasourceOptions=["GPX_USE_EXTENSIONS=OFF"],layerOptions= ['FORCE_GPX_TRACK=YES'],ct=QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem(4326), QgsProject.instance()) )   
            elif form == 'KML':
                path = pad + "/" + name + '.kml'
                writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='KML', onlySelected=sel,ct=QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem(4326), QgsProject.instance()) )    
            elif form == 'LIBKML':
                path = pad + "/" + name + '_.kml'
                writer = QgsVectorFileWriter.writeAsVectorFormat(layer,path,'utf-8',driverName='LIBKML', onlySelected=sel,ct=QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem(4326), QgsProject.instance()) )    
            return writer
        
        if objekte != None:
            pdv = v.ver(self)[0]
            if not os.path.exists(pdv + '/GPX_Ausgabe'):
                os.makedirs(pdv + '/GPX_Ausgabe')
            pdfv = pdv + '/GPX_Ausgabe'
            if wahl == 'Strecken':
                ausgabe = pdfv + '/S_' + strecke
            elif wahl == 'Punkte':
                ausgabe = pdfv + '/P_' + strecke
            elif wahl == 'ohne':
                ausgabe = ''
         
            strecke = strecke.replace(":","_")
            strecke = strecke.replace("-","_")
            strecke = strecke.replace(".","_")
            strecke = strecke.replace(" ","_")
            strecke = strecke.replace("%","_")
            strecke = strecke.replace("//","/")
            strecke = strecke.replace("\\\\","\\")
            
            
            vekwr('gpx',pdfv,dlayer2,strecke,False)
            vekwr('KML',pdfv,dlayer2,strecke,False)
            vekwr('LIBKML',pdfv,dlayer2,strecke,False)
            vekwr('gpkg',pdfv,dlayer2,strecke,False)
            
            print('Str ' + strecke)
            if strecke != '01 Sämtliche':
                try:                    
                    project = QgsProject.instance()
                    loesch = project.mapLayersByName('gpxl')[0]
                    project.removeMapLayer(loesch.id())
                except:
                    pass
            
            
            if platform == "linux":
                subprocess.call(["xdg-open", pdfv])
                #subprocess.call(["xdg-open", pfad])
            elif platform == "darwin":
                subprocess.call(["open", pdfv])
                #subprocess.call(["open", pfad])
            elif platform == "win32":
                try:
                    os.system("start "+ pdfv)
                    #os.system("start "+ pfad)
                except:
                    pass
