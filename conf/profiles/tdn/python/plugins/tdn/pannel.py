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
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QWidget, QComboBox, QDateEdit, QSpinBox, QLineEdit, QCompleter, QInputDialog, QMessageBox, QAction,QDialog,QRadioButton,QScrollArea,QDialogButtonBox
from qgis.PyQt.QtCore import Qt, QSettings
from PyQt5.QtCore import QDate
import qgis.utils
from qgis.utils import iface

from qgis.gui import QgsAttributeDialog, QgsAttributeEditorContext 

from qgis.core import QgsProject, QgsFeature, Qgis, QgsLayerDefinition, QgsTask, QgsMessageLog, QgsApplication, QgsVectorLayer, QgsDataSourceUri, QgsRelation, QgsMapSettings, QgsSnappingUtils,QgsSnappingConfig,QgsTolerance,QgsVectorFileWriter,QgsFeatureRequest
        
import psycopg2 as p
from psycopg2 import Error
import os
from sys import platform

import urllib.request, json
#from .adr_osm import OSMGeocode
from .schreib import schreib
from .ver import ver as v

import requests

import re
import fileinput
import shutil

import time
from datetime import date
from datetime import datetime

from .pg_service_anl import pg_service_an as ps
import subprocess
from .atlas import atl_druck as atld
from .gpx import gpx_aus as gpxa

#atld.druck_st(self)
#gpxa.gpx_exp(self)

#from .ALKIS_Update import ALKIS_Update as AU


#import qgis.core
#from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsApplication, Qgis, QgsProject

# Globale Variable für das Panel
#custom_panel = None


class EifelPannel(QDockWidget):    

    def __init__(self, parent=None):
        super().__init__(parent)
    
        # Überschrift des panel
        #self.setWindowTitle("TDN-GIS")
        #self.setWindowTitle("<b><span style='color:#2E86C1; font-size:14pt;'>TDN-GIS</span></b>")
        #self.setStyleSheet("QLabel { padding: 6px; background-color: #ffffff; border-bottom: 1px solid #ffffff; }")  
        header = QLabel("<b><span style='color:#870319; font-size:16pt;'>TDN-GIS</span></b>")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("QLabel { padding: 3px; background-color: #cecece; border-bottom: 4.1px solid #8d8e90; }")        


        # Haupt-Widget erstellen
        main_widget = QWidget()
        #layout = QVBoxLayout(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(header)

        #label = QLabel("Steuerung")
        #main_layout.addWidget(label)
        
        ############################################
        # teil 1: Aufbau der Benutzeroberfläche
        #############################################
        #######################################
        # Layer Definitionen
        ##########################        
        
        project = QgsProject.instance()
        
        #layerlist  = [layer.name() for layer in project.mapLayers().values() if 'postgres' in str(layer) ]
        #layerlist.sort()
        #QSettings().setValue('/qgis/attributeTableView', 1)
        #QSettings().setValue('/map/identifyAutoFeatureForm', 'true')
        #QSettings().setValue('/Map/identifyAutoFeatureForm', 'true')
        #QSettings().setValue('/qgis/identifyAutoFeatureForm', 'true')
        #QSettings().setValue('/qgis/identifyAutoFeatureForm', 'true')
        
        def setlay():
            layerlist  = [layer.name() for layer in project.mapLayers().values() if 'postgres' in str(layer) ]
            layerlist.sort()
            
            if "Punkte" in layerlist:
                PuOb = project.mapLayersByName("Punkte")[0]
            else:
                PuOb = ''
            
            if "SkizzenStrecke" in layerlist:
                skizze = project.mapLayersByName("SkizzenStrecke")[0]
            else:
                skizze = ''
            
            if "StreckenPlan" in layerlist:
                strecke = project.mapLayersByName("StreckenPlan")[0]
            else:
                strecke = ''
                
            if "Orte" in layerlist:
                pl_orte = project.mapLayersByName("Orte")[0]
            else:
                pl_orte = ''
                
            if "Infrastruktur" in layerlist:
                kuech_punkte = project.mapLayersByName("Infrastruktur")[0]
            else:
                kuech_punkte = ''
                
            if "StandortKüche" in layerlist:
                kuech_fl = project.mapLayersByName("StandortKüche")[0]
            else:
                kuech_fl = ''
            
            return PuOb, skizze, strecke, pl_orte, kuech_punkte, kuech_fl
        
        PuOb,skizze,strecke,pl_orte,kuech_punkte,kuech_fl = setlay()

    
        pad = v.ver(self)[0]
        ##############################################
        
        
    


        ###############################
        # Funktionen erstellen         #
        ###############################
        
        def pgv_a():
            skriptv = __file__
            inverz, indat = os.path.split(skriptv)
                
            pg_serv_verz = os.path.normpath(inverz)
            
            wahl = ps.pg_service_anlegen() # Funktion mit Dropdownmenü zur gemeindewahl aufreufen
            if platform == "win32":                    
                qgis.utils.iface.messageBar().pushInfo('Info: ','Service nicht gefunden')
                QgsProject.instance().write()
                    #pg_path = os.path.normcase(os.path.join(self.plugin_dir))
                pg_path = os.path.normcase(os.path.join(pg_serv_verz))                 
                    
                os.system("setx PGSYSCONFDIR" + " " + pg_path)
                    
                show_message('Schließen Sie QGIS und starten sie neu um auf die angemeldete Datenbank zuzugreifen.')

        
        # Nachricht anzeigen
        def show_message(message):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(message)
            msg_box.setWindowTitle("Info")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            
        def info(Nachricht):
            qgis.utils.iface.messageBar().pushInfo('Info',Nachricht)
        
        # Verbindung zur datenbank und schema, ausgelesen aus Verbindung im Projekt
        def pg_verb():       
            conn_info = s_eg.dataProvider().uri().connectionInfo()  # QGIS-eigene Verbindung
            conn = p.connect(conn_info)
            pg_schema = s_eg.dataProvider().uri().schema()
            cur = conn.cursor()
            return conn,pg_schema
        
        def folge_akt():
            conn = p.connect(service="tdn_gis",sslmode="require")
            cur = conn.cursor()
            sql = """select t_2026.richtung_folge();"""
            cur.execute(sql)            
            cur.close()        
            conn.commit()
        

        def snap(self,schalt,Layer):

            osm_wege = QgsProject.instance().mapLayersByName("osm_wege")[0]
            
            # Configuration setzen
            ms = QgsMapSettings()
            u = QgsSnappingUtils()
            u.setMapSettings(ms)
            cfg = u.config()
            cfg.setEnabled(True)
            cfg.setIntersectionSnapping(False)
            cfg.setSelfSnapping(False)
            #cfg.setTracingEnabled(True)
            cfg.setMode(QgsSnappingConfig.AdvancedConfiguration)
            if Layer == strecke:
                cfg.setIndividualLayerSettings(Layer,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 12, QgsTolerance.Pixels))
            if Layer == skizze:
                cfg.setIndividualLayerSettings(Layer,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 10, QgsTolerance.Pixels))
            
            cfg.setIndividualLayerSettings(PuOb,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 10, QgsTolerance.Pixels))
            cfg.setIndividualLayerSettings(osm_wege,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.VertexAndSegment, 10, QgsTolerance.Pixels))
            
            
            if schalt == 'an':
                cfg.setEnabled(True)
                iface.mainWindow().findChildren(QAction, "EnableTracingAction")[0].setChecked(True)
            elif schalt == 'aus':
                cfg.setEnabled(False)
                iface.mainWindow().findChildren(QAction, "EnableTracingAction")[0].setChecked(False)
            
            
            QgsProject.instance().setSnappingConfig(cfg)
        
        
        
        # zu layer springen
        def spring_layer(m_layer):
            root = project.layerTreeRoot()
            vlayer = project.mapLayersByName(m_layer)[0]
            root.findLayer(vlayer.id()).setItemVisibilityCheckedParentRecursive(True)            
            iface.setActiveLayer(vlayer)
            return vlayer
        
        # Funktion zum Editiren
        def setz_klick(layer):           
            vlayer = spring_layer(layer)
            vlayer.startEditing()
            iface.actionAddFeature().trigger()
        
        # Funktion zum Speichern
        def speicher_klick(layer): 
            vlayer = spring_layer(layer)            
            if vlayer.isEditable() == False:
                info('Nichts zu ändern')    
            elif vlayer.isEditable() == True and vlayer.isModified() == False:
                iface.vectorLayerTools().stopEditing(vlayer)            
            else:
                vlayer.commitChanges()
                iface.vectorLayerTools().stopEditing(vlayer)
                snap(self,'aus','keine')
                info('Änderungen gespeichert')
                
        # objekte löschen
        def loesch(layer):      
            qgis.utils.iface.setActiveLayer(layer)
            
            wahl = layer.selectedFeatureIds()
            if not wahl:
                show_message('Keine gewählten Objekte!- Bitte auswählen')
                qgis.utils.iface.actionSelect().trigger()
            
            else:
                mb = QMessageBox()
                mb.setText('Gewählte Objekte löschen?')
                mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                return_value = mb.exec()
                
                if return_value == QMessageBox.Ok:
                    layer.startEditing() 
                    layer.deleteFeatures(wahl)
                    layer.commitChanges()
                    show_message('Gewählte Objekte glöscht')
                else:
                    info('Nichts gelöscht')
        
        # Knoten verschieben
        def knoten_versch():
            vlayer = gebiet
            qgis.utils.iface.setActiveLayer(vlayer)                
            vlayer.startEditing()
            qgis.utils.iface.actionVertexToolActiveLayer().trigger()
            #qgis.utils.iface.actionIdentify().trigger()
            
        # Attribute editieren
        def attr_edit():
            vlayer = gebiet
            qgis.utils.iface.setActiveLayer(vlayer) 
            QSettings().setValue('/map/identifyAutoFeatureForm', 'true')
            QSettings().setValue('/Map/identifyAutoFeatureForm', 'true')
            QSettings().setValue('/qgis/identifyAutoFeatureForm', 'true')
            #vlayer.startEditing()
            qgis.utils.iface.actionIdentify().trigger()
            
        # Thema auswählen
        def akt_thema(thema):
            root = project.layerTreeRoot()
            model = qgis.utils.iface.layerTreeView().layerTreeModel()
            mtc = project.mapThemeCollection()
            mtc.applyTheme(thema, root, model)

        # Gruppe öffnen
        def spring_gruppe(gruppe):
            root = project.layerTreeRoot()
            Gruppe = root.findGroup(gruppe)
            Gruppe.setItemVisibilityChecked(True)
        

        # Attributt-tabelle in Formularansicht öffen
        def TagFormOpen(layer):
            QSettings().setValue('/qgis/attributeTableView', 1)
            qgis.utils.iface.setActiveLayer(layer)
            zeig_form = iface.showAttributeTable(layer)
            return zeig_form
            #QSettings().setValue('/qgis/attributeTableView', 0)

        #Objekte auf layer wählen
        def auswahl_layer(layer):
            spring_layer(layer)
            qgis.utils.iface.actionSelect().trigger()
         
        # Eingabe der Schlagbezeichnung 
        def schlagbezeichnung():
            qid = QInputDialog()
            title = "Schlagname"
            label = "Schlagname eingeben"
            mode = QLineEdit.Normal
            default = ""
            inp, ok = QInputDialog.getText(qid, title, label, mode, default) # Eingebenen Verzeichnispfad mit O.K in die Variable inp
            if ok:
                schlagbez = inp
            else:
                schlagbez = ""
            return  schlagbez
        
        def LayWahl():
            PuOb,skizze,strecke,pl_orte,kuech_punkte,kuech_fl = setlay()
            dialog = QDialog()
            dialog.setWindowTitle("Objekte Eintragen in")

            layout = QVBoxLayout()

            label = QLabel("Layer zum Editieren wählen")
            layout.addWidget(label)

            # Radio-Buttons hinzufügen
            radio_button1 = QRadioButton("Orte Vorplanung")
            radio_button2 = QRadioButton("StreckenSkizze")
            radio_button3 = QRadioButton("KüchenInfra-Punkte")
            radio_button4 = QRadioButton("Fläche-Standort-Küche")
            radio_button5 = QRadioButton("Punkte -Quartier etc.")
            radio_button6 = QRadioButton("Streckenplanung")
            #radio_button5 = QRadioButton("Flächen-Verinb.-Aufgabe")
                        
            #radio_button3 = QRadioButton("Dummy")

            # Standardmäßig den ersten Radio-Button auswählen
            radio_button2.setChecked(True)

            layout.addWidget(radio_button1)
            layout.addWidget(radio_button2)
            layout.addWidget(radio_button3)
            layout.addWidget(radio_button4)
            layout.addWidget(radio_button5)
            layout.addWidget(radio_button6)
                        

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
                    lay = pl_orte
                elif radio_button2.isChecked():
                    lay = skizze
                elif radio_button3.isChecked():
                    lay = kuech_punkte
                elif radio_button4.isChecked():
                    lay = kuech_fl
                elif radio_button5.isChecked():
                    lay = PuOb
                elif radio_button6.isChecked():
                    lay = strecke
                else:
                    lay = 'ohne'
            else:
                lay = 'ohne'
            
            if lay != 'ohne':
                if lay == pl_orte:
                    akt_thema('Vorplanung')
                elif lay == skizze:
                    akt_thema('Skizze')                    
                elif lay == kuech_punkte:
                    akt_thema('Küche')                    
                elif lay == kuech_punkte or lay == kuech_fl:
                    akt_thema('Küche')                    
                else:
                    akt_thema('Standard')
                    
            else:
                show_message('Keine Auswahl')
                            
            return lay
        
        # Funktion Punktobjekte setzen
        def puobj_setz():            
            
            lay = LayWahl()
            
            if lay != 'ohne':                    
                spring_layer(lay.name())
                setz_klick(lay.name())
                if lay == skizze:
                    snap(self,'an',skizze)
                elif lay == strecke:
                    snap(self,'an',strecke)
                else:
                    snap(self,'an','keine')
                
                    
            else:
                show_message('Keine Auswahl')
                snap(self,'aus','keine')
                
        # Funktion Punktobjekte bearbeiten
        def puobj_edit():          
            lay = LayWahl()
            
            if lay != 'ohne': 
                
                spring_layer(lay.name())
                lay.startEditing()
                qgis.utils.iface.actionIdentify().trigger()
            else:
                show_message('Keine Auswahl')
        
        def obj_loesch():
            lay = LayWahl()
            
            if lay != 'ohne':
                loesch(lay)

            else:
                show_message('Keine Auswahl') 
                
                
        def wege_waehlen(items):
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

        def export_WegFolge():
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
            #pdfv = os.path.normcase(QgsProject.instance().homePath() )
            pdfv = v.ver(self)[0]
            print('PDF-V: ',pdfv)
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
            
            wegenamen = wege_waehlen(wegeliste)
        
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
                    #os.system("start "+ pad)
                    #subprocess.call(["xdg-open", pfad])
                elif platform == "darwin":
                    subprocess.call(["open", pad])
                elif platform == "win32":
                    try:
                        os.system("start "+ pad)
                        #os.system("start "+ pfad)
                    except:
                        pass
                    
                show_message('Tabellen erstellt')
                
            #except(Exception) as error:
                #show_message('Keine Eingabe ',error)
            except:
                show_message('Keine Eingabe ')
                

        def export_StreckeAusw():

            # Laxer definieren
            #tabelle =  QgsProject.instance().mapLayersByName("richtungs_folge")[0] # tabelle mit sämtlicne Layernamen
            Ausw =   QgsProject.instance().mapLayersByName("StreckenAuswertung")[0]    # Der Layer mit sämtlichen Routen  
            Ausw_name = Ausw.name()
            
            
            
            AbPlan =   QgsProject.instance().mapLayersByName("ablauf_plan")[0]    # Der Layer mit sämtlichen Routen  
            AbPlan_name = AbPlan.name()
            
            
            # Export-Pfade festlegen
            #pdfv = os.path.normcase(QgsProject.instance().homePath() )
            pdfv = v.ver(self)[0]
            print('PDF-V: ',pdfv)
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
                options.onlySelectedFeatures = False
                #options.attributes = [3,2,14,18,15,16,17,13,12,10,5,6]
                if os.path.exists(path):
                    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                print(options)
                writer = QgsVectorFileWriter.writeAsVectorFormatV3(layer,path,QgsProject.instance().transformContext(),options)       
                return writer, path
            
            #wegenamen = wege_waehlen(wegeliste)
        
            try:
                #exkwr(pad,lay,lay_name,dat_name)
                exkwr(pad,Ausw,Ausw_name,'tdn2026_streckenauswertung')                
                #path = exkwr(pad,Ausw,Ausw_name,'tdn2026_streckenauswertung')[1] 
                path = exkwr(pad,AbPlan,AbPlan_name,'tdn2026_streckenauswertung')[1]
                
                
                try:
                    ###################################
                    #Excel formatieren
                    from openpyxl import load_workbook
                    from openpyxl.styles import Font, Alignment,PatternFill
                    from openpyxl.utils import get_column_letter
                    
                    hellblau = PatternFill(
                        fill_type="solid",
                        fgColor="9aecf0"      # helles Blau
                    )
                    
                    hellgruen = PatternFill(
                        fill_type="solid",
                        fgColor="7ff683"      # helles Grün
                    )
                    rot = PatternFill(
                        fill_type="solid",
                        fgColor="f294d4"      # helles Grün
                    )
                    
                    braun = PatternFill(
                            fill_type="solid",
                            fgColor="ffb260"      # helles Grün
                    )                   
                    
                    rosa = PatternFill(
                            fill_type="solid",
                            fgColor="fdd6e7"      # helles Grün
                    )   
                    
                    
                    
                        
                    # Arbeitsmappe laden
                    wb = load_workbook(path)

                    # Tabellenblatt auswählen
                    ws = wb["StreckenAuswertung"]
                    ws_ablp = wb["ablauf_plan"]
                    
                    '''
                    # Spaltenbreite steuern
                    for col in ws.iter_cols():
                        max_length = 0
                        column = get_column_letter(col[0].column)

                        for cell in col:
                            try:
                                if cell.value is not None:
                                    max_length = max(max_length, len(str(cell.value)))
                            except Exception:
                                pass

                        # Zuschlag für Arial 11
                        adjusted_width = (max_length + 2) * 1.2
                        ws.column_dimensions[column].width = adjusted_width
                    '''
                    
                    # Generell Zeilenformatierung in Streckenauswertung
                    def form_gen(eing):
                        for row in eing.iter_rows():
                            eing.row_dimensions[row[0].row].height = 20
                            for cell in row:
                                cell.font = Font(name="Arial",size=11)
                                cell.alignment = Alignment(
                                    horizontal=cell.alignment.horizontal,
                                    vertical="center"
                                    )
                    form_gen(ws)
                    form_gen(ws_ablp)

                    # Kopfzeile (erste Zeile) formatieren
                    def form_kopfzeile(eing):
                        for cell in eing[1]:
                            #cell.font = Font(bold=True)
                            cell.font = Font(name="Arial", bold=True, size=13)
                            cell.alignment = Alignment(horizontal="center", vertical="center")
                            cell.fill = rot
                    
                    form_kopfzeile(ws)
                    form_kopfzeile(ws_ablp)
                        
                    # Zellen formatieren 
                    
                    def form_zeilen(eing):
                        for row in eing.iter_rows():
                            if (row[1].value == "1 Segmente"  and row[3].value == 1  ) or (row[4].value == "2 Mittag") :   # 2. Spalte = Index 1
                                for cell in row:
                                    cell.font = Font(
                                        name="Arial",
                                        size=11,
                                        bold=True
                                    )
                                    cell.fill = hellblau
                                    
                            if (row[1].value == "3 Toursumme") or (row[4].value == "1 Quartier" and row[7].value == 2):   # 2. Spalte = Index 1
                                for cell in row:
                                    cell.font = Font(
                                        name="Arial",
                                        size=11,
                                        bold=True
                                    )
                                    cell.fill = hellgruen
                                    
                            if row[4].value == "1 Quartier" and row[7].value == 1  :   # 2. Spalte = Index 1
                                for cell in row:
                                    cell.font = Font(
                                        name="Arial",
                                        size=11,
                                        bold=True
                                    )
                                    cell.fill = braun
                                    
                            if row[1].value == "2 EtappenSumme"  :   # 2. Spalte = Index 1
                                for cell in row:
                                    cell.font = Font(
                                        name="Arial",
                                        size=11,
                                        bold=True
                                    )
                                    cell.fill = rosa
                    form_zeilen(ws)
                    form_zeilen(ws_ablp)

                    # Arbeitsmappe speichern
                    wb.save(path)
                    #######
                    ############
                except:
                   info('Kein OpenPyxl installiert, Excel wird unformatiert erstellt')
                        
                print(Ausw)
                print(pad)
                
                if platform == "linux":
                    subprocess.call(["xdg-open", path])
                    #os.system("start "+ pad)
                    #subprocess.call(["xdg-open", pfad])
                elif platform == "darwin":
                    subprocess.call(["open", path])
                elif platform == "win32":
                    try:
                        os.system("start "+ path)
                        #os.system("start "+ pfad)
                    except:
                        pass
                    
                show_message('Tabellen erstellt')
                
            #except(Exception) as error:
                #show_message('Keine Eingabe ',error)
            except:
                show_message('Keine Eingabe ')
            

        
        ##########################
        #  Klick für dieFunktionen setzen
        #########################
        
        #PG-Service eintragen
        #def NeueVerbindung_klick():
            #pgv_a()
        
        # Excel Streckenauswertung ausgeben        
        def excel_ausw_klick():
            export_StreckeAusw()
        
        
        #GPX ausgeben
        def gpx_ausgeben_klick():
            gpxa.gpx_exp(self)       
        
        
        #PDF Atlas ausgeben
        def atlas_ausgeben_klick():
            atld.druck_st(self)

        
        # Wegfolge ausgeben
        def export_WegFolge_klick():
            export_WegFolge()        
        
        # Wegfolge aktualisieren
        def folge_akt_klick():
            show_message('Dauert 2 Minuten')
            folge_akt()
            show_message('WegeFolge aktualisiert')

        #Punktobjekte setzen        
        def PunObjSetz_klick():
            puobj_setz()
            
        #Punktobjekte bearbeiten       
        def PunObjEdit_klick():
            puobj_edit()          
            
        def PunObjSpeicher_klick():
            layer = iface.activeLayer()
            speicher_klick(layer.name())
            
        def FeaturesLoeschen_klick():
            obj_loesch()

    
        ###################################################
        
        # stylesets für Oberfläche header.setStyleSheet("QLabel { padding: 3px; background-color: #cecece; border-bottom: 4.1px solid #8d8e90; }")  
        
        def css_ueberschr(LabelN):
            LabelN.setStyleSheet("""
            QLabel {
            color: #000000;
            font-weight: bold;
            font-size: 14pt;
            text-align:center; 
            padding: 4px;
            border-bottom: 4.1px solid #3e4759;
            }
            """)
            LabelN.setAlignment(Qt.AlignCenter)

        def css_Button(PN,farbe,gr):
            PN.setStyleSheet("""
            QPushButton {
            color: """ + farbe + """;
            font-weight: bold;
            font-size: """ + str(gr) +"""pt;
            padding: 4px 6px;
            }
            QPushButton:hover { background-color: #16A085; }
            """)
            
        def css_Button2(PN,farbe,bc,gr):
            PN.setStyleSheet("""
                QPushButton {
                    background-color: """ + bc + """;
                    color: """ + farbe +""";
                    font-size: """ + str(gr) +"""pt;
                    font-weight: bold;
                    border: none;
                    border-radius: 6px;
                    padding: 4px 8px;
                }
                QPushButton:hover {
                    background-color: #a01635;
                }
                QPushButton:pressed {
                    background-color: #d641d7;
                }
            """)
    

     
        # Punktobjekte digitalisieren
        ####################################
        # Titel für Punktobjekte bearbeiten
        ##################################
        self.NeueObjekte = QLabel("Punkte und Linien bearbeiten")
        css_ueberschr(self.NeueObjekte) # CCS formatieren
        main_layout.addWidget(self.NeueObjekte)
    
        ####################################
        # Titel für Punktobjekte bearbeit
        ####################################        
        ########################
        # Art des Layouts
        #######################################
        # Horizontales Layout
        NeueObjekte_layout = QHBoxLayout()
        
        # Buttons setzen
        self.NeuesObjekt = QPushButton('Objekt erfassen')
        self.ObjektEdit = QPushButton('Objekt bearbeiten')
        
        
        #Fornatieren
        css_Button(self.NeuesObjekt,'green',11)
        css_Button(self.ObjektEdit,'green',11)
        
        # Verbindung mit den Funktionen
        self.NeuesObjekt.clicked.connect(PunObjSetz_klick)
        self.ObjektEdit.clicked.connect(PunObjEdit_klick)              
        
        # Zum Layout hinzufügen
        NeueObjekte_layout.addWidget(self.NeuesObjekt)
        NeueObjekte_layout.addWidget(self.ObjektEdit)        
        
        
        # Zum Haupt-Layout hinzufügen
        main_layout.addLayout(NeueObjekte_layout)       
        
        #######################################
        # Horizontales Layout
        LoeschObjekte_layout = QHBoxLayout()
        # Buttons setzen
        self.ObjektSpeichern = QPushButton('Objekt speichern')
        self.LoescheObjekt = QPushButton('Gewählte Objekte loeschen')
        
        #Fornatieren
        css_Button(self.ObjektSpeichern,'red',11)
        css_Button2(self.LoescheObjekt,'white','orange',12)
        
        # Verbindung mit den Funktionen
        self.LoescheObjekt.clicked.connect(FeaturesLoeschen_klick)
        self.ObjektSpeichern.clicked.connect(PunObjSpeicher_klick)
        
        # Zum Layout hinzufügen
        LoeschObjekte_layout.addWidget(self.ObjektSpeichern)
        LoeschObjekte_layout.addWidget(self.LoescheObjekt)
        
        
        # Zum Haupt-Layout hinzufügen
        main_layout.addLayout(LoeschObjekte_layout)   
        
        
        ####################################
        # Titel für Wegefolge bearbeiten
        ##################################
        self.wegbesch = QLabel("Wege-Beschreibung")
        css_ueberschr(self.wegbesch) # CCS formatieren
        main_layout.addWidget(self.wegbesch)
        #####################################
        #Wegefolge aktualisieren
        #######################################
        # Horizontales Layout
        FolgeAkt_layout = QHBoxLayout()
        # Buttons setzen
        self.Wegbeschreibung = QPushButton('Knoten Aktualisieren')
        self.WegExport = QPushButton('Als Excel ausgeben')
        
        #Fornatieren
        css_Button(self.Wegbeschreibung,'green',12)
        css_Button(self.WegExport,'green',11)
        
        
        # Verbindung mit den Funktionen
        self.Wegbeschreibung.clicked.connect(folge_akt_klick)
        self.WegExport.clicked.connect(export_WegFolge_klick)
        
        # Zum Layout hinzufügen
        FolgeAkt_layout.addWidget(self.Wegbeschreibung)
        FolgeAkt_layout.addWidget(self.WegExport)
        
        # Zum Haupt-Layout hinzufügen
        main_layout.addLayout(FolgeAkt_layout)    
        
        
   
        ####################################
        # Titel für Atlas-Ausgabe
        ##################################
        self.atlas_aus = QLabel("Karten und Auswertungen ausgeben")
        css_ueberschr(self.atlas_aus) # CCS formatieren
        main_layout.addWidget(self.atlas_aus)
        #####################################
        #Atlas-Ausgabe
        #######################################
        # Horizontales Layout
        AtlasAus_layout = QHBoxLayout()
        # Buttons setzen
        self.PDFAtlas = QPushButton('PDFs')
        self.EXCAuss = QPushButton('Ablauf als Excel')
        self.GPXAuss = QPushButton('GPX-Tracks')
        
        #Fornatieren
        css_Button(self.PDFAtlas,'green',11)
        css_Button(self.EXCAuss,'green',11)
        css_Button(self.GPXAuss,'green',11)
        
        # Verbindung mit den Funktionen
        self.PDFAtlas.clicked.connect(atlas_ausgeben_klick)
        self.EXCAuss.clicked.connect(excel_ausw_klick)
        self.GPXAuss.clicked.connect(gpx_ausgeben_klick)
        
        # Zum Layout hinzufügen
        AtlasAus_layout.addWidget(self.PDFAtlas)
        AtlasAus_layout.addWidget(self.EXCAuss)
        AtlasAus_layout.addWidget(self.GPXAuss)
        
        # Zum Haupt-Layout hinzufügen
        main_layout.addLayout(AtlasAus_layout)    
        
        
        
        
    
        
        
        
        ##############################################
        ############################################
        # teil 1: Aufbau der Benutzeroberfläche abgeschlossen
        #############################################
        ##############################################################
        
        # Initialisiere die Attribut-Werte-Liste, damit die Auswertung aller Eingaben des panells mit einander in Bezug gesetzt werden können
        self.selected_values = []
        #####################################################
        
        ###########################################################
        #currentText
        # HauptWidget initialisieren
        self.setWidget(main_widget)
        # HauptWidget initialisieren
        
    #########################################
    # Jetzt stattdessen über update_selected_values() und self.process_selected_values() um nachher alles zusammen verwenden zu können):
    #######################################################
    """
    def on_checkbox_state_changed(self, state):
        
        self.update_selected_values()            
            # Logik für die Verarbeitung der ausgewählten Werte
        self.process_selected_values()
    """
    #########################################
    # Jetzt stattdessen über update_selected_values() und self.process_selected_values() um nachher alles zusammen verwenden zu können):
    #######################################################
    """    
    def update_selected_values(self):
        
        # Hier werden die aus dem Panell erfassten Werteänderungen  verarbeitet
        # Es wird eine Liste gebildet, in welche alle über das panell gewählten Werte unter process_selected_values() verfügbar sind
        self.selected_values = []  # Liste definieren
        
        ########################################
        # Verarbeitung der Pannel-Eingaben
        # #####################################  
    """
        
