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
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QLabel, QDockWidget, QProgressBar, QAction, QMessageBox, QDialog, QVBoxLayout,QComboBox, QRadioButton,QHBoxLayout,QScrollArea,QCheckBox,QDialogButtonBox

from qgis.PyQt.QtCore import Qt, QSettings

from qgis.core import *
import qgis.utils

from qgis.utils import iface

#from qgis.core import Qgis
from qgis.PyQt.QtGui import QIcon
import processing
#from .provider import SGVProvider
import time
from datetime import date
from datetime import datetime
import getpass
import math
import subprocess
from sys import platform

from .adr_osm import OSMGeocode
# Plugin-Update
from .pdat_update import pd_upd as pd_up

#Eigeene Module laden
from .schreib import schreib
from .ver import ver as v

from .ed_aw import ed_aw as ed_aw

from .snap_st import snap_st as sn
from .atlas import atl_druck as atld
from .gpx import gpx_aus as gpxa
#gpxa.gpx_exp(self)

#atld.druck_st(self)
#from .pg_load import pg_load as pl

#sn.snap(self,'an')
#sn.snap(self,'aus')

from .pg_service_anl import pg_service_an as pg_s_anl
#Pannel importieren
from .pannel import EifelPannel as ep

from .eingabe import eingabe
import subprocess
import shutil
import psycopg2 as p
from psycopg2 import Error

class tdn:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.propfad = os.path.dirname(QgsApplication.qgisSettingsDirPath())
        self.plugin_dir = os.path.dirname(__file__)
        self.provider = None
        
        def show_message(message):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(message)
            msg_box.setWindowTitle("Info")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
        
        def pg_service_anlegen():
            dialog = pg_s_anl()     # Aufruf von imprtoerter Klasse aus pannel_pi.py
            if dialog.exec_() == QDialog.Accepted:
                print('pg_service.conf anlegen')

        project = QgsProject.instance()
        
        #TDN-Verz ermitteln
        projekt = os.path.normpath(project.absoluteFilePath()) #
        # verzeichnis und dateinamen des Projektes trennen
        verz = os.path.split(projekt)[0]
        #TDN-Verz ermitteln #Ein Verzeichnis oberhalb
        tdn_verz = os.path.dirname(verz)
        
        #projekt_verz = os.path.normpath(project.homePath())
        nam = os.path.splitext(os.path.split(project.absoluteFilePath())[1])[0]
        
        skript = os.path.dirname(os.path.normpath(os.path.realpath(__file__)))
        projekt_verz = os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(os.path.dirname(os.path.dirname(skript))))))) + '/daten'
        conf_verz = os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(os.path.dirname(os.path.dirname(skript))))))) + '/conf'
        
        batchpfad = os.path.normpath(skript + '/TDN_GIS.bat')
        bpneu = os.path.normpath(tdn_verz + '/TDN_GIS.bat')
        
        if platform == "win32":
            alt_pg_dat = os.path.normpath(skript + "/pg_service.conf")
            pg_dat = os.path.normpath(tdn_verz + "/conf/pg_service.conf")
            print('Conf-pfade')
            print(pg_dat)
            print(alt_pg_dat)
            batchpfad = os.path.normpath(skript + '/TDN_GIS.bat')
            bpneu = os.path.normpath(tdn_verz + '/TDN_GIS.bat')
            
            try:
                if not os.path.exists(pg_dat):
                    if os.path.exists(alt_pg_dat):
                        shutil.copy2(alt_pg_dat,pg_dat)
                        os.remove(alt_pg_dat)
                    
                if os.path.exists(batchpfad):
                    os.remove(bpneu)
                    shutil.copy2(batchpfad,bpneu)
                    os.remove(batchpfad)
            except:
                print('Pfade')
                print(pg_dat)
                print(alt_pg_dat)
                print(batchpfad)
                print(bpneu)
            
        
        if nam == "TDN_2026" or nam == "TDN_2027":
            print('TDN-Projekt geladen')        

        else:
            try:   # Wenn das anlegen der Verbindung oder die folgenden SQL Abfragen fehl schlagen wird eine  Ausname ausgelöst
                conn = p.connect(service="tdn_gis",sslmode="require")
                cur = conn.cursor()
                sql = """insert into tdn.plugin_user
                        (plugin_version)
                        select 'Vers:_2026_08_25' as eintrag where not exists
                        (select nutzer||plugin_version as eintrag from tdn.plugin_user 
                            where nutzer||plugin_version = CURRENT_USER||'Vers:_2026_08_25')
    ;
                        """
                cur.execute(sql)            
                cur.close()        
                conn.commit()
                print('PluginVersion getestet')
                
                #projekt_verz = os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(os.path.dirname(os.path.dirname(skript))))))) + '/daten'
                #show_message(os.path.normcase(projekt_verz + '/TDN_2026.qgz'))
                #project.read(os.path.normcase(projekt_verz + '/TDN_2026.qgz'))
                
            except:
                if platform == "win32":
                    pg_dat = os.path.normpath(conf_verz + "/pg_service.conf")   
                    
                    if not os.path.exists(pg_dat):
                        # Wenn nicht, wird der Dialog (siehe pannel_pi.py) zu Anlgen der Service-Datei geöffnet
                        pg_service_anlegen()                        
                        #os.system("setx PGSYSCONFDIR" + " " + os.path.normcase(os.path.join(skript)))                        
                        #show_message('Schließen Sie QGIS und starten sie neu um auf die angemeldete Datenbank zuzugreifen.')
                else:
                    # Unter Linux und Mac hat die .pg_service.conf einen festen Platz
                    pg_dat = os.path.expanduser("~/.pg_service.conf")
                    if not os.path.exists(pg_dat):
                        # Wenn nicht, wird der Dialog (siehe pannel_pi.py) zu Anlgen der Service-Datei geöffnet
                        pg_service_anlegen() 
                    else:
                        tdns = 0
                        with open(pg_dat, "r") as file:
                            for line in file:
                                lis = line.rstrip()
                                if ('tdn_gis' in lis) == True:
                                    tdns = tdns + 1
                                else:
                                    tdns = tdns + 0
                        if tdns == 0:
                            pg_service_anlegen()
                        else:
                            print('PG-Service vorhanden')
                            show_message('PG-Service avorhanden')
                    
        
        def snapt(self):
            if QgsSnappingConfig().enabled() == True:
                sna = 1
            elif QgsSnappingConfig().enabled() == False:
                sna = 0
            print(sna)
            return sna
        self.snapt = snapt
        
        #Süurverfolgung einschalten
        iface.mainWindow().findChildren(QAction, "EnableTracingAction")[0].setChecked(True)

        try:
            global pannell            

            pannell = ep()
            iface.addDockWidget(Qt.RightDockWidgetArea, pannell)
                
        except:
            show_message('TDN-GIS öffnen um das Pannell zu nutzen')
        
        #project.read(os.path.normcase(projekt_verz + '/TDN_2026.qgz'))
        #QSettings().setValue('/qgis/identifyAutoFeatureForm', 'true')
        QSettings().setValue('/UI/recentProjects/1/path', projekt_verz + '/TDN_2026.qgz')
        QSettings().setValue('/UI/recentProjects/1/pin','true')
        QSettings().setValue('/UI/recentProjects/1/title','TDN-Gis 2026')
        QSettings().setValue('/UI/recentProjects/2/path', projekt_verz + '/TDN_2027.qgz')
        QSettings().setValue('/UI/recentProjects/2/pin','true')
        QSettings().setValue('/UI/recentProjects/2/title','TDN-GIS 2027')
        QSettings().setValue('/browser/favourites',projekt_verz + '|||TDN_GIS')            
        
        
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
            
            
    def initGui(self):  
        #. Add toolbar        
        #self.toolBar = self.iface.addToolBar("TDN")
        #self.initProcessing()
        
        #. Add toolbar        
        self.toolBar = self.iface.addToolBar("TDN")
        iface.mainWindow().addToolBar(Qt.LeftToolBarArea,self.toolBar)
        self.toolBar.setVisible(True)
        #self.toolBar.setAllowedAreas(Qt.LeftToolBarArea | Qt.RightToolBarArea)
        #self.initProcessing()
   
        # Aktion Kartenthema Standard
        self.te_standard =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"te_standard.svg"))),"Thema Standard", self.iface.mainWindow())
        self.te_standard.triggered.connect(self.te_sta)        
        self.te_standard_button = self.toolBar.addAction(self.te_standard)       

        
        # Aktion Kartenthema DOP
        self.te_lub =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"ortho.png"))),"Thema Luftbild", self.iface.mainWindow())
        self.te_lub.triggered.connect(self.te_dop)        
        self.te_lub_button = self.toolBar.addAction(self.te_lub)
        
        
        # Aktion Kartenthema Kizze
        #self.te_Skizz =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"hoehe.svg"))),"Thema Standard", self.iface.mainWindow())
        #self.te_Skizz.triggered.connect(self.te_Skizze)        
        #self.te_Skizz = self.toolBar.addAction(self.te_Skizz)

        
        # Aktion Kartenthema Küche
        self.te_kuech =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir  ,"kueche.png"))),"Thema Küche", self.iface.mainWindow())
        self.te_kuech.triggered.connect(self.te_kueche)        
        self.te_kuech_button = self.toolBar.addAction(self.te_kuech)
        
        # Aktion Kartenthema Höhe
        self.te_hoeh =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir   ,"hoehe.png"))),"Thema Höhen", self.iface.mainWindow())
        self.te_hoeh.triggered.connect(self.te_hoehe)        
        self.te_hoeh_button = self.toolBar.addAction(self.te_hoeh)



        # leerer Button
        self.mas_leer0 =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"leer.svg")))," ", self.iface.mainWindow())
        self.mas_leer0_button = self.toolBar.addAction(self.mas_leer0)
        
        
        # Pannel öffnen
        self.panell_left =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"suche.svg"))),"Panell öffnen", self.iface.mainWindow())
        self.panell_left.setEnabled(True)
        self.panell_left.setCheckable(True) 
        self.panell_left.triggered.connect(self.pan_left)        
        self.panell_left_button = self.toolBar.addAction(self.panell_left)
        
        # leerer Button
        self.mas_leer0 =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"leer.svg")))," ", self.iface.mainWindow())
        self.mas_leer0_button = self.toolBar.addAction(self.mas_leer0)
        
        # Skizzen-Element schreiben
        self.edit_skiz =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"edit2.png"))),"Neue WegeSkizze hinzufügen", self.iface.mainWindow())
        self.edit_skiz.setEnabled(True)
        self.edit_skiz.setCheckable(True) 
        self.edit_skiz.triggered.connect(self.edit_ski)        
        self.edit_skiz_button = self.toolBar.addAction(self.edit_skiz)
        
        # leerer Button
        self.mas_leer0 =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"leer.svg")))," ", self.iface.mainWindow())
        self.mas_leer0_button = self.toolBar.addAction(self.mas_leer0)
        
        # Trassen-Segment hnzufügen
        self.edit_schnell =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"lin_edit.png"))),"Neues Trassensegment hinzufügen", self.iface.mainWindow())
        self.edit_schnell.setEnabled(True)
        self.edit_schnell.setCheckable(True) 
        self.edit_schnell.triggered.connect(self.edit_st)        
        self.edit_schnell_button = self.toolBar.addAction(self.edit_schnell)
        
        # leerer Button
        self.mas_leer0 =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"leer.svg")))," ", self.iface.mainWindow())
        self.mas_leer0_button = self.toolBar.addAction(self.mas_leer0)        
        
        # Trassen-Eigenschaften
        self.edit_trasse =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"hervorheben.svg"))),"Trassen-Eigenschaften bearbeiten", self.iface.mainWindow())
        self.edit_trasse.setEnabled(True)
        self.edit_trasse.setCheckable(True) 
        self.edit_trasse.triggered.connect(self.edit_tr)        
        self.edit_trasse_button = self.toolBar.addAction(self.edit_trasse)
        
        # Editieren
        self.edit_schnellp =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"ed_knoten_li.png"))),"Linien-Knoten bearbeiten", self.iface.mainWindow())
        self.edit_schnellp.setEnabled(True)
        self.edit_schnellp.setCheckable(True) 
        self.edit_schnellp.triggered.connect(self.edit_pu)        
        self.edit_schnellp_button = self.toolBar.addAction(self.edit_schnellp)
        
        '''
        # Trassen-Segmente teilen
        self.edit_schnitt =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"ed_schneiden.png"))),"Trassesegmente teilen", self.iface.mainWindow())
        self.edit_schnitt.setEnabled(True)
        self.edit_schnitt.setCheckable(True) 
        self.edit_schnitt.triggered.connect(self.edit_sch)        
        self.edit_schnitt_button = self.toolBar.addAction(self.edit_schnitt)      

        
        # Teil hinzufühen
        self.edit_neuteil =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"teil.png"))),"Trassenteil hinzufügen", self.iface.mainWindow())
        self.edit_neuteil.setEnabled(True)
        self.edit_neuteil.setCheckable(True) 
        self.edit_neuteil.triggered.connect(self.edit_teil)        
        self.edit_neuteil_button = self.toolBar.addAction(self.edit_neuteil)  
        '''
 
        
        # Loeschen
        self.edit_loesch =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"ed_loesch.png"))),"Linien wählen und löschen", self.iface.mainWindow())
        self.edit_loesch.setEnabled(True)
        self.edit_loesch.setCheckable(True) 
        self.edit_loesch.triggered.connect(self.edit_loe)        
        self.edit_loesch_button = self.toolBar.addAction(self.edit_loesch)
        
        
        # leerer Button
        self.mas_leer0 =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"leer.svg")))," ", self.iface.mainWindow())
        self.mas_leer0_button = self.toolBar.addAction(self.mas_leer0)        
        
        
        
        # knoten verschieben
        self.edit_knot =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"Such.png"))),"Neuer Punkt", self.iface.mainWindow())
        self.edit_knot.setEnabled(True)
        self.edit_knot.setCheckable(True) 
        self.edit_knot.triggered.connect(self.edit_kn)        
        self.edit_knot_button = self.toolBar.addAction(self.edit_knot)  
        
        # Punkt-Eigenschaften
        self.pu_eigensch =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"export.svg"))),"Punkt-Eigenschaften bearbeiten", self.iface.mainWindow())
        self.pu_eigensch.setEnabled(True)
        self.pu_eigensch.setCheckable(True) 
        self.pu_eigensch.triggered.connect(self.pu_eigen)        
        self.pu_eigensch_button = self.toolBar.addAction(self.pu_eigensch)
        
        # knoten verschieben
        self.edit_pu_knot =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"ed_knoten.png"))),"Punkte verschieben", self.iface.mainWindow())
        self.edit_pu_knot.setEnabled(True)
        self.edit_pu_knot.setCheckable(True) 
        self.edit_pu_knot.triggered.connect(self.edit_pukn)        
        self.edit_pu_knot_button = self.toolBar.addAction(self.edit_pu_knot)  
        
        # Punkt Loeschen
        self.edit_loeschp =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"ed_loeschp.png"))),"Punkte wählen und löschen", self.iface.mainWindow())
        self.edit_loeschp.setEnabled(True)
        self.edit_loeschp.setCheckable(True) 
        self.edit_loeschp.triggered.connect(self.edit_loep)        
        self.edit_loeschp_button = self.toolBar.addAction(self.edit_loeschp)      

        
    
        # leerer Button
        self.mas_leer0 =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"leer.svg")))," ", self.iface.mainWindow())
        self.mas_leer0_button = self.toolBar.addAction(self.mas_leer0)        
        


        
        # Browser öffnen
        self.bro_ed =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic"  ,"layer_laden.png"))),"DateiBrowser ", self.iface.mainWindow())
        self.bro_ed.setEnabled(True)
        self.bro_ed.setChecked(True)
        self.bro_ed.setCheckable(True) 
        self.bro_ed.triggered.connect(self.Browser_e)        
        self.bro_ed_button = self.toolBar.addAction(self.bro_ed)
        


        
        # Auswahl drucken
        self.druck_schnell =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"druck.png"))),"PDF-Atlas drucken", self.iface.mainWindow())
        #self.druck_schnell.setEnabled(True)
        #self.druck_schnell.setCheckable(True) 
        self.druck_schnell.triggered.connect(self.druck_st)        
        self.druck_schnell_button = self.toolBar.addAction(self.druck_schnell)

        # GPX ausgeben
        self.gpx_ausgeben =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"gpx.svg"))),"GPX-Tracks ausgeben", self.iface.mainWindow())
        #self.gpx_ausgeben.setEnabled(True)
        #self.gpx_ausgeben.setCheckable(True) 
        self.gpx_ausgeben.triggered.connect(self.gpx_aus)        
        self.gpx_ausgeben_button = self.toolBar.addAction(self.gpx_ausgeben)
        
        # Richtungsexcel ausgeben
        self.export_richt =  QAction(QIcon(os.path.normcase(os.path.join(self.plugin_dir + "/pic" ,"Such2.png"))),"Wegbeschreibung / Richtungstabelle ausgeben", self.iface.mainWindow())
        self.export_richt.triggered.connect(self.export_layer)        
        self.export_richt_button = self.toolBar.addAction(self.export_richt)
        

        
        #Update der Plugins
        self.pro_update =  QAction(QIcon(os.path.normpath(os.path.join(self.plugin_dir + "/pic" ,"upload.svg"))),"Plugin und Projekt aktualisieren", self.iface.mainWindow())
        self.pro_update.setEnabled(True)
        self.pro_update.triggered.connect(self.Plugin_update)        
        self.pro_update_button = self.toolBar.addAction(self.pro_update)
        
        # Richtungsfolge als Excel
        #self.richt_liste =  QAction(QIcon(os.path.normpath(os.path.join(self.plugin_dir + "/pic" ,"xweg.svg"))),"Richtungsfolge als Excel", self.iface.mainWindow())
        #self.richt_liste.setEnabled(True)
        #self.richt_liste.triggered.connect(self.RichtListe)        
        #self.richt_liste_button = self.toolBar.addAction(self.pro_update)
        
    def show_message(self,message):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(message)
            msg_box.setWindowTitle("Info")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()


    def unload(self):
        #QgsApplication.processingRegistry().removeProvider(self.provider)
        #del self.vek_lad_button
        #del self.panell_left_button
        #print(dir(self.toolBar))
        #self.iface.removeToolBarIcon(self.fo_ein)
        self.toolBar.setVisible(False)
        if self.toolBar is not None:
            del self.toolBar
            
        for dw in  qgis.utils.iface.mainWindow().findChildren(QDockWidget):
            if dw.objectName() == "":
            #if type(dw).__name__ == "EifelPannel":
                qgis.utils.iface.removeDockWidget(dw)

    
    # Projektupdate    
    def Plugin_update(self):
        Info = pd_up.pd_upd(self)
        self.show_message(Info)
            
        
        # Browse öffnen
    def Browser_e(self, checked):
        if checked:
            qgis.utils.iface.messageBar().pushInfo('Info','DateiBrowser öffnen')
            for x in qgis.utils.iface.mainWindow().findChildren(QDockWidget):
                if x.objectName() == 'Browser' or x.objectName() == 'bookmarkManager'or x.objectName() == 'ProcessingToolbox':
                    x.setVisible(True)
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','DateiBrowser schließen')
            for x in qgis.utils.iface.mainWindow().findChildren(QDockWidget):
                if x.objectName() == 'Browser' or x.objectName() == 'bookmarkManager'or x.objectName() == 'ProcessingToolbox':
                    x.setVisible(False)
    
    # Themenwahl
    def te_sta(self):  # Thema Standard
        vlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
        qgis.utils.iface.setActiveLayer(vlayer)
        project = QgsProject.instance() 
        root = project.layerTreeRoot()
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Standard'
        mtc.applyTheme(name, root, model)
        #sn.snap(self,'an')
            
        
    def te_dop(self):  # Thema Orthop
        vlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
        qgis.utils.iface.setActiveLayer(vlayer)
        project = QgsProject.instance() 
        root = project.layerTreeRoot()
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Luftbild'
        mtc.applyTheme(name, root, model)
        #sn.snap(self,'an')
        
    def te_kueche(self):  # Thema Orthop
        vlayer = QgsProject.instance().mapLayersByName("Infrastruktur")[0]
        qgis.utils.iface.setActiveLayer(vlayer)
        project = QgsProject.instance() 
        root = project.layerTreeRoot()
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Küche'
        mtc.applyTheme(name, root, model)
        #sn.snap(self,'an')
        
    def te_hoehe(self):  # Thema Orthop
        vlayer = QgsProject.instance().mapLayersByName("SteigungenStrecke")[0]
        qgis.utils.iface.setActiveLayer(vlayer)
        project = QgsProject.instance() 
        root = project.layerTreeRoot()
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Höhen'
        mtc.applyTheme(name, root, model)
        #sn.snap(self,'an')
        
    def te_Skizze(self):  # Thema Orthop
        vlayer = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
        qgis.utils.iface.setActiveLayer(vlayer)
        project = QgsProject.instance() 
        root = project.layerTreeRoot()
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Skizze'
        mtc.applyTheme(name, root, model)
        #sn.snap(self,'an')
    
    # Schnell digit
    def edit_st(self, checked):
        
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("StreckenPlan")[0]
        root = project.layerTreeRoot()
        
        #model = qgis.utils.iface.layerTreeView().layerTreeModel()
        #mtc = QgsProject.instance().mapThemeCollection()
        #name = 'Edit'
        #mtc.applyTheme(name, root, model) 
        
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:
                
            vlayer.startEditing()
            qgis.utils.iface.actionAddFeature().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
                
                
    # Schnell Skizze
    def edit_ski(self, checked):
        
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
        root = project.layerTreeRoot()
        
        #model = qgis.utils.iface.layerTreeView().layerTreeModel()
        #mtc = QgsProject.instance().mapThemeCollection()
        #name = 'Edit'
        #mtc.applyTheme(name, root, model) 
        
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:
                
            vlayer.startEditing()
            qgis.utils.iface.actionAddFeature().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
                
                
                
        # Schnell digit
    def edit_tr(self, checked):
        
        project = QgsProject.instance()
            
        root = project.layerTreeRoot()
        
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Standard'
        mtc.applyTheme(name, root, model)         
        
        if checked:
            vlayer = ed_aw.ed_aw(self)
            qgis.utils.iface.setActiveLayer(vlayer)
            vlayer.startEditing()
            qgis.utils.iface.actionIdentify().trigger()
        
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            vlayer = qgis.utils.iface.activeLayer()
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
    
    
    def pu_eigen(self, checked):
        
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
        root = project.layerTreeRoot()
        
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Standard'
        mtc.applyTheme(name, root, model) 
        
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:                
            vlayer.startEditing()
            qgis.utils.iface.actionIdentify().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
    
    

        # Schnell digit edit_likn
    def edit_kn(self, checked):
        
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
        root = project.layerTreeRoot()
        
        #model = qgis.utils.iface.layerTreeView().layerTreeModel()
        #mtc = QgsProject.instance().mapThemeCollection()
        #name = 'Edit'
        #mtc.applyTheme(name, root, model) 
        
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:
                
            vlayer.startEditing()
            qgis.utils.iface.actionAddFeature().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
            
            #sn.snap(self,'aus')
                
        # Schnell digit
            
        # Knoten verschieben edit_likn
    def edit_pu(self, checked):
        
        project = QgsProject.instance() 
        
        # Thema ändern
        #root = project.layerTreeRoot()
        #model = qgis.utils.iface.layerTreeView().layerTreeModel()
        #mtc = QgsProject.instance().mapThemeCollection()
        #name = 'Knoten'
        # mtc.applyTheme(name, root, model)        
        
        if checked:
            vlayer = ed_aw.ed_aw(self)
            qgis.utils.iface.setActiveLayer(vlayer)
            vlayer.startEditing()
            qgis.utils.iface.actionVertexToolActiveLayer().trigger()
            #qgis.utils.iface.actionIdentify().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            vlayer = qgis.utils.iface.activeLayer()
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)              
    
    
    def edit_pukn(self, checked):
        
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("Punkte")[0]
        
        # Thema ändern
        #root = project.layerTreeRoot()
        #model = qgis.utils.iface.layerTreeView().layerTreeModel()
        #mtc = QgsProject.instance().mapThemeCollection()
        #name = 'Knoten'
        # mtc.applyTheme(name, root, model)        
        
        
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:                
            vlayer.startEditing()
            qgis.utils.iface.actionVertexToolActiveLayer().trigger()
            #qgis.utils.iface.actionIdentify().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
            
    # Schneiden
    def edit_sch(self, checked):
            
        project = QgsProject.instance() 
        
        if checked:
            vlayer = ed_aw.ed_aw(self)
            qgis.utils.iface.setActiveLayer(vlayer)
            vlayer.startEditing()
            qgis.utils.iface.actionSplitFeatures().trigger()
            #actionSplitFeatures
            #qgis.utils.iface.actionIdentify().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
            vlayer = qgis.utils.iface.activeLayer()
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
                
        # Teilhinzufügen
    def edit_teil(self, checked):
            
        project = QgsProject.instance() 


        vlayer = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
        if vlayer.selectedFeatures() != []:
        
            if checked:
                vlayer.startEditing()
                qgis.utils.iface.actionAddPart().trigger()
                #actionSplitFeatures
                #qgis.utils.iface.actionIdentify().trigger()
            else:
                qgis.utils.iface.actionAddPart().trigger()
                qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
                schreib.schreib(self)
                
                style_name = 'Standard'
                stylemanager = vlayer.styleManager()
                current_style = stylemanager.currentStyle()
                if style_name != current_style:
                    stylemanager.setCurrentStyle(style_name)
        else:
            qgis.utils.iface.actionSelect().trigger()
            mb = QMessageBox()
            mb.setText('Segment markieren')
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            return_va = mb.exec()
            if return_va == QMessageBox.Ok:
                pass
            if checked:
                qgis.utils.iface.setActiveLayer(vlayer)
                qgis.utils.iface.actionSelect().trigger()
            else:
                mb = QMessageBox()
                mb.setText('Ein weiteres mal Schaltfläche Klicken und Linien digitalisieren')
                mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                return_val = mb.exec()
                if return_val == QMessageBox.Ok:
                    pass
            
            
    '''        
    # Vereinigen
    def edit_ver(self, checked):
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("sgv_trassen")[0]
        root = project.layerTreeRoot()
        model = qgis.utils.iface.layerTreeView().layerTreeModel()
        mtc = QgsProject.instance().mapThemeCollection()
        name = 'Edit'
        mtc.applyTheme(name, root, model)        
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:
            qgis.utils.iface.actionSelect().trigger()
            vlayer.startEditing()   
            #vlayer.startEditing()
            #actionSelect
            #qgis.utils.iface.actionCutFeatures().trigger()
            #qgis.utils.iface.actionIdentify().trigger()
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            schreib.schreib(self)
    '''
            
        # Objekte loeschen
    def edit_loe(self, checked):
            
        project = QgsProject.instance() 

        if checked:            
            vlayer = ed_aw.ed_aw(self)
            qgis.utils.iface.setActiveLayer(vlayer)
            qgis.utils.iface.actionSelect().trigger()
            vlayer.startEditing()            
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            #loeschen
            vlayer = qgis.utils.iface.activeLayer()
            qgis.utils.iface.actionDeleteSelected().trigger()
            schreib.schreib(self)
            
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
            
            #vlayer.removeSelection()
            qgis.utils.iface.actionIdentify().trigger()
            
    # PunktObjekte loeschen
    def edit_loep(self, checked):
            
        project = QgsProject.instance() 
        vlayer = QgsProject.instance().mapLayersByName("Punkte")[0]   
        qgis.utils.iface.setActiveLayer(vlayer)
        if checked:            
            
            qgis.utils.iface.actionSelect().trigger()
            vlayer.startEditing()            
        else:
            qgis.utils.iface.messageBar().pushInfo('Info','Editiermodus beenden')
            #loeschen
            qgis.utils.iface.actionDeleteSelected().trigger()
            schreib.schreib(self)
            
            style_name = 'Standard'
            stylemanager = vlayer.styleManager()
            current_style = stylemanager.currentStyle()
            if style_name != current_style:
                stylemanager.setCurrentStyle(style_name)
            
            #vlayer.removeSelection()
            qgis.utils.iface.actionIdentify().trigger()
            
            

    # Schnell Druck
    def druck_st(self, checked):
        atld.druck_st(self)
        
        
    # Schnell Druck
    def gpx_aus(self):
        gpxa.gpx_exp(self)
        
    def export_layer(self):
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
        
        
    def pan_left(self, checked):
        
        #pannell = None
        
        if checked:    
            try:
                global pannell            

                pannell = ep()
                iface.addDockWidget(Qt.RightDockWidgetArea, pannell)
                
            except:
                self.show_message('TDN-GIS öffnen um das Pannell zu nutzen')
            
        
        else:
            
            #if pannell is not None:   
            try:
                iface.removeDockWidget(pannell)
            except:
                pass
            #pannell.deleteLater()
                #rem_kc_pannell()
            #pannell = None
                    

