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
from qgis.core import QgsProject,QgsLayoutExporter
import qgis.utils
from .ver import ver as v
import subprocess


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QLabel, QDockWidget, QProgressBar, QAction, QMessageBox, QDialog, QVBoxLayout,QComboBox, QRadioButton,QHBoxLayout,QScrollArea,QCheckBox,QDialogButtonBox


class atl_druck:
    
    # Schnell Druck
    def druck_st(self):
        
        import processing
        
        # Auswahlmenü
        def AuswahlMenue():
            dialog = QDialog()
            dialog.setWindowTitle("Strecken oder Punkte ausgeben?")

            layout = QVBoxLayout()

            label = QLabel("Strecken oder Punkte ausgeben?")
            layout.addWidget(label)

            # Radio-Buttons hinzufügen
            radio_button1 = QRadioButton("Strecken Abschnitte")
            radio_button1a = QRadioButton("Strecken Tage")
            radio_button2 = QRadioButton("Punkte")
            radio_button3 = QRadioButton("Küche")
            radio_button4 = QRadioButton("AuswertungsTabellen")
            radio_button5 = QRadioButton("Bildschirmfoto")
            radio_button6 = QRadioButton("Uebersicht Final")
            radio_button7 = QRadioButton("Vorplanung")

            # Standardmäßig den ersten Radio-Button auswählen
            radio_button1.setChecked(True)

            layout.addWidget(radio_button1)
            layout.addWidget(radio_button1a)
            layout.addWidget(radio_button2)
            layout.addWidget(radio_button3)
            layout.addWidget(radio_button4)
            layout.addWidget(radio_button5)
            layout.addWidget(radio_button6)
            layout.addWidget(radio_button7)

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
                    wahl = "StreckenAbschnitte"
                elif radio_button1a.isChecked():
                    wahl = "StreckenGesamt"
                elif radio_button2.isChecked():
                    wahl = "Punkte"
                elif radio_button3.isChecked():
                    wahl = "Küche"
                elif radio_button4.isChecked():
                    wahl = "AuswertungsTabellen"
                elif radio_button5.isChecked():
                    wahl = "Bildschirmfoto"
                elif radio_button6.isChecked():
                    wahl = "UebersichtFinal"
                elif radio_button7.isChecked():
                    wahl = "Vorplanung"
                else:
                    wahl = 'ohne'
            else:
                wahl = 'ohne'
                
            return wahl

        # Beispiel: Öffnen Sie den Dialog aus einem QGIS-Plugin oder einem Skript

        wahl = AuswahlMenue()  
        
        print(wahl)

        if wahl != 'ohne' and wahl != 'AuswertungsTabellen' and wahl != 'Bildschirmfoto' and wahl != 'UebersichtFinal' and wahl != 'Küche' and wahl !=  'StreckenGesamt' and wahl !=  'Vorplanung':
                
            vlayer = QgsProject.instance().mapLayersByName("Etappen")[0]
            et_list = []
            objekte = vlayer.getFeatures()
            for feature in objekte:
                if feature["fahrt"] == 1:
                    print(feature["bezeichnung"])
                    wert = feature["bezeichnung"]
                    et_list.append(wert)
            et_list.append('0_Saemtliche_Streckenabschnitte')
            et_list.sort()
            print(et_list)
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
                abbr = QPushButton("Abbrechen")
                layout.addWidget(button)
                layout.addWidget(abbr)

                def on_button_clicked():
                    dialog.accept()
                def on_abbr_clicked():
                    dialog.reject()

                button.clicked.connect(on_button_clicked)
                abbr.clicked.connect(on_abbr_clicked)

                dialog.setLayout(layout)

                result = dialog.exec_()

                if result == QDialog.Accepted:
                    selected_value = combo_box.currentText()
                    strecke = selected_value
                    return strecke
                    # Hier können Sie den ausgewählten Wert weiterverarbeiten
                    # Zum Beispiel: Ein Attribut eines Layers setzen, etc.
                else:
                    strecke = 'keine'
                    return strecke

            # Beispiel: Öffnen Sie den Dialog aus einem QGIS-Plugin oder einem Skript
            strecke = AuswahlMenue()
            print(wahl)
            print(strecke)        
        
        if wahl == 'StreckenAbschnitte':
            dlayer = QgsProject.instance().mapLayersByName("Abschnitte")[0]
            druck = 'Atlas_Abschnitte'
        
            
        if wahl == 'StreckenGesamt':
            dlayer = QgsProject.instance().mapLayersByName("Strecken_box")[0]
            druck = 'Atlas_Strecken'
            strecke = 'Tages_Etappen_TDN_2026_'
        
        elif wahl == 'Punkte':
            dlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
            druck = 'PU-Atlas'
            
        elif wahl == 'Küche':
            dlayer = QgsProject.instance().mapLayersByName("kuechen_infra_atlas")[0]
            druck = 'Atlas-Küche'
            strecke = ''
 
 
        elif wahl == 'AuswertungsTabellen':
            tlayer = QgsProject.instance().mapLayersByName("StreckenAuswertung")[0]
            dlayer = tlayer
            druck = 'AuswertungsTabellen' 
            strecke = ''
            
        elif wahl == 'Bildschirmfoto':
            tlayer = QgsProject.instance().mapLayersByName("StreckenAuswertung")[0]
            dlayer = tlayer
            druck = 'Bildschirmfoto' 
            strecke = ''
            
        elif wahl == 'UebersichtFinal':
            tlayer = QgsProject.instance().mapLayersByName("StreckenAuswertung")[0]
            dlayer = tlayer
            druck = 'UebersichtFinal' 
            strecke = ''
            
        elif wahl == 'Vorplanung':
            tlayer = QgsProject.instance().mapLayersByName("StreckenAuswertung")[0]
            dlayer = tlayer
            druck = 'Vorplanung' 
            strecke = ''
            

        elif wahl == 'ohne' or strecke == 'keine':
            dlayer = None
            druck = None
        
        if dlayer != None and wahl != "AuswertungsTabellen" and wahl != 'Bildschirmfoto' and wahl != 'Uebersicht':
            if strecke != '0_Saemtliche_Streckenabschnitte':
                dlayer.selectByExpression("\"etappen_bezeichnung\"= '" + strecke +"'") 
            else:
                dlayer.selectByExpression("\"etappe\"> 0") 
            objekte = dlayer.selectedFeatures()
        
        elif wahl == "AuswertungsTabellen" or wahl == "UebersichtFinal" or wahl == "Bildschirmfoto" or wahl == "Vorplanung":
            tlayer = dlayer
            objekte = tlayer
            
        else:
            objekte = None
        print(objekte)
        
        if objekte != None:              
            #pdfv = self.expv_such
            pdfv = v.ver(self)[0]
            if not os.path.exists(pdfv + '/PDF_Atlas_Ausgabe'):
                os.makedirs(pdfv + '/PDF_Atlas_Ausgabe')
            pdv = pdfv + '/PDF_Atlas_Ausgabe'
            
            if wahl == 'StreckenAbschnitte':
                ausgabe = pdv + '/S_' + strecke
                
            if wahl == 'StreckenGesamt':
                ausgabe = pdv + '/' + strecke
            
            elif wahl == 'Punkte':
                ausgabe = pdv + '/P_' + strecke
                
            elif wahl == 'Küche':
                ausgabe = pdv + '/Kueche_' + strecke
                
            elif wahl == 'UebersichtFinal':
                ausgabe = pdv + '_UebersichtFinal'
                
            elif wahl == 'Vorplanung':
                ausgabe = pdv + 'Vorplanung'
            
            elif wahl == 'Bildschirmfoto':
                qid = QInputDialog()
                title = "Name des PDF"
                label = "Name des PDF"
                mode = QLineEdit.Normal
                default = 'Detail'
                inp, ok = QInputDialog.getText(qid, title, label, mode, default) # Eingebenen Verzeichnispfad mit O.K in die Variable inp
                na_z = inp
                ausgabe = pdv + '/Detail_' + na_z
                
            elif wahl == 'AuswertungsTabellen':
                auswertung = pdv + '/AuswertungsTabellen'
                ausgabe = auswertung
                
            elif wahl == 'ohne':
                ausgabe = ''
         
            ausgabe = ausgabe.replace(":","_")
            ausgabe = ausgabe.replace("-","_")
            ausgabe = ausgabe.replace(".","_")
            ausgabe = ausgabe.replace(" ","_")
            ausgabe = ausgabe.replace("%","_")
            ausgabe = ausgabe.replace("//","/")
            ausgabe = ausgabe.replace("\\\\","\\")
            #ausgabe = QtWidgets.QFileDialog.getSaveFileName(filter = "PDF (*.pdf)" ,directory = pdfv)[0]
            qgis.utils.iface.messageBar().pushInfo('Info',ausgabe + 'wird gedruckt')
                
            if ausgabe != '' :
                if len(ausgabe.lower()) - ausgabe.lower().rfind('pdf') != 3:
                    ausgabe = os.path.normcase(ausgabe + '.pdf')
                else:
                    ausgabe = os.path.normcase(ausgabe)
                
                if  wahl == 'AuswertungsTabellen':
                    manager = QgsProject.instance().layoutManager()
                    Layout = manager.layoutByName('AuswertungsTabellen')
                    exporter = QgsLayoutExporter(Layout)
                    exporter.exportToPdf(ausgabe, QgsLayoutExporter.PdfExportSettings())                   
                    qgis.utils.iface.messageBar().clearWidgets()
                    qgis.utils.iface.messageBar().pushInfo('Info','Gedruckt')
                    
                elif  wahl == 'Bildschirmfoto':
                    manager = QgsProject.instance().layoutManager()
                    Layout = manager.layoutByName('Bildschirmfoto')
                    
                    try:
                        Hauptkarte = Layout.referenceMap()
                        canvas = qgis.utils.iface.mapCanvas()
                        Hauptkarte.setExtent(canvas.extent())
                        #Hauptkarte.setScale(5000)
                        qid = QInputDialog()
                        title = "Maßstab?"
                        label = "Welcher Maßstab"
                        mode = QLineEdit.Normal
                        default = str(int(round(Hauptkarte.scale(),-1)))
                        inp, ok = QInputDialog.getText(qid, title, label, mode, default) # Eingebenen Verzeichnispfad mit O.K in die Variable inp
                        
                        Hauptkarte.setScale(int(inp))
                    except:
                        pass                    
                        
                    
                    exporter = QgsLayoutExporter(Layout)
                    exporter.exportToPdf(ausgabe, QgsLayoutExporter.PdfExportSettings())                   
                    qgis.utils.iface.messageBar().clearWidgets()
                    qgis.utils.iface.messageBar().pushInfo('Info','Gedruckt')
                    
                elif  wahl == 'UebersichtFinal':
                    manager = QgsProject.instance().layoutManager()
                    Layout = manager.layoutByName('UebersichtFinal')
                    exporter = QgsLayoutExporter(Layout)
                    exporter.exportToPdf(ausgabe, QgsLayoutExporter.PdfExportSettings())                   
                    qgis.utils.iface.messageBar().clearWidgets()
                    qgis.utils.iface.messageBar().pushInfo('Info','Gedruckt')
                    
                elif  wahl == 'Vorplanung':
                    manager = QgsProject.instance().layoutManager()
                    Layout = manager.layoutByName('Vorplanung')
                    exporter = QgsLayoutExporter(Layout)
                    exporter.exportToPdf(ausgabe, QgsLayoutExporter.PdfExportSettings())                   
                    qgis.utils.iface.messageBar().clearWidgets()
                    qgis.utils.iface.messageBar().pushInfo('Info','Gedruckt')
                
                else:
                    # Atlas-Layout als PDF exportieren
                    '''
                    manager = QgsProject.instance().layoutManager()
                    layout = manager.layoutByName(druck)
                    printer = layout.atlas()
                    for i in range(0, printer.count()):   
                        exporter = QgsLayoutExporter(printer.layout())
                        exporter.exportToPdf(ausgabe, QgsLayoutExporter.PdfExportSettings())
                        printer.next()
                    '''
                    
                    params = {
                        'COVERAGE_LAYER': None,
                        'DISABLE_TILED': False,
                        'DPI': None,
                        'FILTER_EXPRESSION': '',
                        'FORCE_VECTOR': False,
                        'GEOREFERENCE': False,
                        'INCLUDE_METADATA': False,
                        'LAYERS': None,
                        'LAYOUT': druck,
                        'SIMPLIFY': True,
                        'SORTBY_EXPRESSION': '',
                        'SORTBY_REVERSE': False,
                        'TEXT_FORMAT': 0,  # Texte immer als Pfade exportieren (empfohlen)
                        'OUTPUT': ausgabe
                        }
                    processing.run('native:atlaslayouttopdf', params) # => für progressbarfeedback=f) 
                    print(params)
                    print('Pfad :', ausgabe)
                    
                    canvas = qgis.utils.iface.mapCanvas()
                    canvas.zoomToSelected(dlayer)
                    dlayer.removeSelection()
                    
                    vlayer = QgsProject.instance().mapLayersByName("StreckenPlan")[0]  
                    qgis.utils.iface.setActiveLayer(vlayer)
                    
                # Clear th  e message bar when done
                qgis.utils.iface.messageBar().pushInfo('Info','Gedruckt')
                #os.popen('okular ' +  ausgabe + '')
                #subprocess.call(["xdg-open", ausgabe])
                if platform == "linux":
                    subprocess.call(["xdg-open", ausgabe])
                elif platform == "darwin":
                    subprocess.call(["open", ausgabe])
                elif platform == "win32":
                    #os.system("start "+ Druck)
                    #os.system("start "+ '"'  + Druck + '"')
                    os.startfile(ausgabe)
                #Anderes Werkzeug auswählen info
                
            else:
                qgis.utils.iface.messageBar().pushInfo('Info','Nichts zu drucken')
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Nichts zu drucken')
        #vlayer.selectAll()

        
        
        #qgis.utils.iface.actionZoomToLayer().trigger()
        
        #extent = vlayer.extent()
        #canvas.setExtent(extent)
        #canvas.refresh()
