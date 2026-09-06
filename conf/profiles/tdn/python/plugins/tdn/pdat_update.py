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

from qgis.core import  QgsProject

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QLabel ,QDialog, QVBoxLayout, QDockWidget, QCheckBox, QFormLayout, QRadioButton, QHBoxLayout, QComboBox
from qgis.PyQt.QtWidgets import QAction, QMessageBox

import qgis.utils
from qgis.utils import iface
#from qgis.PyQt.QtCore import Qt, QSettings

import psycopg2 as p
from psycopg2 import Error
import os
import zipfile
import glob

import shutil
import re
import fileinput

import time

from datetime import date
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox

class pd_upd:
    # Daten schreiben Funktion
    def pd_upd(self):
        
        dat = datetime.now().strftime('%Y_%m_%d_um_%H_%M')
        # Verzechnis definieren
        plugin_dir = os.path.dirname(__file__)
        oberhalb = os.path.dirname(plugin_dir)
        
        # Projekt
        project = QgsProject.instance()
        # Dateien im Pluginverzeicnis
        os.chdir(plugin_dir)
        muster = r"*.*"   # Suchmuster fü
        dats = glob.glob(muster) # Eine Liste aller dateien wird erzeugt
        #######################
        
        # Der pfad zur Quell-Projektdatei
        projekt = os.path.normpath(project.absoluteFilePath()) #
        # verzeichnis und dateinamen des Projektes trennen
        verz = os.path.split(projekt)[0]
        qgs_dat = os.path.split(projekt)[1]
        
        if qgs_dat == 'TDN_2026.qgz':
            prdat = 'TDN_2026'
        elif qgs_dat == 'TDN_2027.qgz':
            prdat = 'TDN_2027'
        
        def show_message(message):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(message)
            msg_box.setWindowTitle("Info")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
        
        # schema auslesen
        def pg_auslesen():
            try: 
                project = QgsProject.instance()
                doktab = project.mapLayersByName("Punkte")[0]
                conn_info = doktab.dataProvider().uri().connectionInfo()  # QGIS-eigene Verbindung
                pg_schema = doktab.dataProvider().uri().schema()
            except:
                show_message('Bitte Projekt laden')
                doktab = None
                conn_info = None
                pg_schema = None
                project = None
            
            return conn_info,pg_schema,project
            
        def Vorhaben():
            dialog = QDialog()
            dialog.setWindowTitle("Update Vorlage ")

            layout = QVBoxLayout()

            label = QLabel('Projekt als Vorlage hochladen oder Projekt und Plugin  aus Vorlage aktualisieren?')
            layout.addWidget(label)

            # Radio-Buttons hinzufügen
            radio_button1 = QRadioButton("Projekt und Plugin aktualisieren")
            radio_button2 = QRadioButton("Vorlage und Plugin hochladen")

            # Standardmäßig den ersten Radio-Button auswählen
            radio_button1.setChecked(True)

            layout.addWidget(radio_button1)
            layout.addWidget(radio_button2)
                
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
                    antwort = 'Aktualisieren'
                elif radio_button2.isChecked():
                    antwort = 'Publizieren'
                else:
                    antwort = 'Abbruch'
            else:
                antwort = 'Abbruch'
                    
            return antwort
        
        antwort = Vorhaben()
        conn_info,pg_schema,project = pg_auslesen()
        
        if project != None:
            proj_verz =  os.path.normpath(project.homePath())        
            skriptv = __file__
            inverz, indat = os.path.split(skriptv)                
            vorlagen_verz = proj_verz
        
        if pg_schema == None or project == None:
            antwort = 'Abbruch'
        
        
        if antwort ==  'Publizieren':           
            
            def frage_nutzer(parent=None):
                # Eingabefelder
                dialog = QDialog(parent)
                dialog.setWindowTitle("Projekt als Vorlage für Update speichern")
                admin_input = QLineEdit()
                admin_input.setPlaceholderText("Ich bin TDN-Admin mit Namen:")
                adminpw_input = QLineEdit()
                adminpw_input.setPlaceholderText("Ich bin TDN-Admin mit folgendem Passwort")

                # Layout
                form_layout = QFormLayout()
                form_layout.addRow("Admin-Name:", admin_input)
                form_layout.addRow("Admin-PW:", adminpw_input)
                # OK-Button
                ok_button = QPushButton("OK")
                abr_button = QPushButton("Abbrechen")
                ok_button.clicked.connect(dialog.accept)
                abr_button.clicked.connect(dialog.reject)

                # Gesamt-Layout
                layout = QVBoxLayout()
                layout.addLayout(form_layout)
                layout.addWidget(ok_button)
                layout.addWidget(abr_button)
                dialog.setLayout(layout)

                # Dialog anzeigen
                if dialog.exec_():
                    admin = admin_input.text() #or "test"
                    adpw = adminpw_input.text() #or "test"
                    return admin,adpw
                else:
                    return "niemand","ohne"

                    
            admin,adpw = frage_nutzer()
            ##print(f"nutz: {admin}, Pw: {adpw}")
                
            if admin == 'niemand' or adpw == 'ohne':
                show_message('Keine Eingabe')

            else:            
                try:                                                    # Wenn das anlegen der Verbindung oder die folgenden SQL Abfragen fehl schlagen wird eine  Ausname ausgelöst
                    #conn = p.connect(service="EIFEL",sslmode="require")    # Datenbankverbdindung über das Modul  psycopg2 als p
                    conn = p.connect(host='85.215.48.125', port=51353, dbname='tdn', user=admin, password=adpw ,sslmode="require")
                    #print(conn)
                    
                    curtest = conn.cursor() # Cursor auf der Verbindung anlegen, mit dem Cursor können Abfragen abgesetzt werden
                    
                    # testen ob rechte
                    testabfrage = """ select case when current_user in (select username from tdn.admin_list) then 'ja' else 'nein' end """
                    curtest.execute(testabfrage)
                    berechtigt = curtest.fetchone()
                    
                    berechtigt = berechtigt[0]
                    curtest.close()
                    conn.commit()
                    conn.close()
                    #print(berechtigt)
                    
                    if berechtigt == 'ja':
                        
                        #Projekt schreibneb
                        project.write()
                        os.chdir(verz)                       
                        
                        
                        #Projekt lesen
                        with open(projekt, "rb") as f:
                            pr_data = f.read()
                        ##########################
                        # Plugin-Ordner als zip schreiben ohne projektordner)
                        ##########################
                        
                        # Dateien im Pluginverzeicnis
                        os.chdir(plugin_dir)
                        
                        compression = zipfile.ZIP_DEFLATED
                        zip_plug = oberhalb +'/' 'tdn_plugin_dat' + '.zip'
                        
                        with zipfile.ZipFile(zip_plug, 'w', compression=compression) as zipf:
                            for objs in dats:  # dats ist Liste der Dateien, Erstellung Siehe Anfang
                                zipf.write(objs)
                        
                        # Daten des Zipfiles lesen für den datenbank-import (als Binärer datenstrpm)
                        with open(zip_plug, "rb") as f:
                            plug_data = f.read()
                        #bc    
                        shutil.copy2(zip_plug,oberhalb +'/' 'tdn_plugin_dat' + dat + '.zip')
                        
                        ##########################
                        # Plugin-Ordner als zip geschrieben)
                        ##########################
                        
                        ##############################
                        # Funktion die Datenbank laden
                        #############################
                        def dbload(abf):
                            conn = p.connect(host='85.215.48.125', port=51353, dbname='tdn', user=admin, password=adpw ,sslmode="require")
                            cur = conn.cursor()
                        
                            cur.execute(abf)
                            conn.commit()
                            cur.close()
                            conn.close()
                        
                        ###############################
                        #Upload Plugin in die Datenbank
                        ################################
                        
                        pluginkenn = 'plugin_vorlage'
                        # Abfrage
                        # Datenstrom als p.Binary in die datenbank
                        abfp = """
                        insert into tdn.projekt_datei_update
                        (typ,projekt_name,schema_name,proj_zip,datum)
                        values('plugin','""" + pluginkenn + """','""" + pg_schema +"""',"""  + str(p.Binary(plug_data)) + """,'"""  + dat + """');"""
                        ##print(abf)
                        # p.Binary(data)
                        #In Datenbank laden
                        #print(abfp)
                        dbload(abfp)
                        os.remove(zip_plug)
                        
                        ###############################
                        #Upload der Vorlagen in die Datenbank
                        ################################
                        # Abfrage
                        # Datenstrom als p.Binary in die datenbank
                        abf = """
                        insert into tdn.projekt_datei_update
                        (typ,projekt_name,schema_name,proj_zip,datum)
                        values('""" + prdat +  """','"""+ qgs_dat + """','""" + pg_schema +"""',"""  + str(p.Binary(pr_data)) + """,'"""  + dat + """');"""
                        ##print(abf)
                        # p.Binary(data)
                        #In Datenbank laden
                        dbload(abf)
                        
                        # Daten im Projektverzeichnis löschen
                        os.chdir(verz)
                        #os.remove(zip_dat)
                        #os.remove(projekt)
                        '''
                        if os.path.exists(cfg):
                            os.remove(cfg)
                        
                        if os.path.exists(bild):
                            os.remove(bild)
                        '''
                        
                        show_message('Vorlage auf Datenbank hochgeladen')
                        Info = 'Vorlage auf Datenbank hochgeladen'
                    else:
                        show_message('Keine Berechtigung zum Anlagen einer Vorlage')
                        Info = 'Keine Berechtigung zum Anlagen einer Vorlage'
                        
                except (Exception, p.DatabaseError) as error:
                    #print(str(error))
                    show_message('gescheitert: ' + str(error))
                    Info = 'gescheitert: ' + str(error)
                
        
        elif  antwort ==  'Aktualisieren':
            
            try:
                
                ############################################
                #plugin aktualsiieren
                #########################################
                os.chdir(plugin_dir)
                
                # Backup alte dateienen                
                compression = zipfile.ZIP_DEFLATED
                zip_plug = oberhalb +'/' 'tdn_plugin_dat' + '.zip'
                print(zip_plug)
                print(dats)
                with zipfile.ZipFile(zip_plug, 'w', compression=compression) as zipf:
                    for objs in dats:  # dats ist Liste der Dateien, Erstellung Siehe Anfang
                        zipf.write(objs)
                shutil.copy2(zip_plug,oberhalb +'/' 'tdn_plugin_dat' + dat + '.zip')
                os.remove(zip_plug)
                # Backup erstellt
                
                
                # postgis anbinden
                conn = p.connect(conn_info)
                cur = conn.cursor()
                # Abfrage letzte Zeile der Projektdatei-Datenbank
                abf = """select proj_zip from tdn.projekt_datei_update where projekt_name = 'plugin_vorlage' order by fid desc limit 1"""
                # Daten holen
                cur.execute(abf)
                pdata = cur.fetchone()[0]
                
                pdatpfad = os.path.normpath(plugin_dir + 'tdn_plugin_dat.zip') 
                
                with open(pdatpfad, "wb") as f:
                    f.write(pdata)           
                
                ''' alter version
                with zipfile.ZipFile(pdatpfad, 'r') as zip_ref:
                    zip_ref.extractall(plugin_dir) 
                '''
                    
                with zipfile.ZipFile(pdatpfad, 'r') as zip_ref:
                    for member in zip_ref.infolist():
                        # Extrahieren der einzelnen Datei
                        zip_ref.extract(member, plugin_dir)
                        
                        # Den vollständigen Pfad der extrahierten Datei ermitteln
                        extrahierter_pfad = os.path.join(plugin_dir, member.filename)
                        
                        # Sicherstellen, dass es sich um eine Datei und keinen Ordner handelt
                        if os.path.isfile(extrahierter_pfad):
                            # Den im Archiv gespeicherten Zeitstempel in Sekunden umwandeln
                            zeitstempel = time.mktime(member.date_time + (0, 0, -1))
                            
                            # Zeitstempel der Datei aktualisieren (Zugriffs- und Änderungszeit)
                            os.utime(extrahierter_pfad, (zeitstempel, zeitstempel))
                            
                
                svgpfad = os.path.normpath(plugin_dir + '/pic')
                
                svgmuster = r"*.svg"   # Suchmuster fü
                pngmuster = r"*.png"   # Suchmuster fü
                svgs = glob.glob(svgmuster) # Eine Liste aller dateien wird erzeugt
                pngs = glob.glob(pngmuster) # Eine Liste aller dateien wird erzeugt
                cplist = svgs + pngs
                for objs in cplist:
                    shutil.copy2(objs,svgpfad + '/' + objs)
                    #os.remove(objs)              
                
                os.remove(pdatpfad)
                
                cur.close()
                conn.close()
                
                ############################################
                #plugin aktualsiert
                #########################################              
            
                
                os.chdir(vorlagen_verz)
                # postgis anbinden
                conn = p.connect(conn_info)
                cur = conn.cursor()
                # Abfrage letzte Zeile der Projektdatei-Datenbank
                
                if prdat == 'TDN_2027':
                    abf = """select proj_zip from tdn.projekt_datei_update where projekt_name = 'TDN_2027.qgz' order by fid desc limit 1"""
                    
                elif prdat == 'TDN_2026':
                    abf = """select proj_zip from tdn.projekt_datei_update where projekt_name = 'TDN_2026.qgz' order by fid desc limit 1"""
                    
                # Daten holen
                cur.execute(abf)
                data = cur.fetchone()[0]
                
                #zipfile schreiben
                datpfad = os.path.normpath(vorlagen_verz + '/' + qgs_dat)
                
                
                #Backups der alten Vorlagen
                pro_vorlage = os.path.normpath(vorlagen_verz + '/' + qgs_dat)
                bc_vorlage = os.path.normpath(vorlagen_verz  + '/bc' + '_' + dat + '_' + qgs_dat)
                shutil.copy2(pro_vorlage,bc_vorlage)
                
                #cfg_vorlage = pro_vorlage +'.cfg'
                #cfg_vorlage_bc = bc_vorlage +'.cfg'
                #hutil.copy2(cfg_vorlage,cfg_vorlage_bc)
                
                # Neue vorlage schreiben
                os.remove(datpfad)
                with open(datpfad, "wb") as f:
                    f.write(data)           
                
                #with zipfile.ZipFile(datpfad, 'r') as zip_ref:
                #zip_ref.extractall(vorlagen_verz) 
                
                # dab verbindung schließen
                #os.remove(datpfad)
                cur.close()
                conn.close()
                
                

                project.read(projekt) 
                
                Info = 'Update durchgeführt'
                show_message('Vorlage aktualisiert und Projekt aus Vorlage aktualisiert')
                
                # Plugin neu laden
                qgis.utils.unloadPlugin('tdn')
                qgis.utils.loadPlugin('tdn')
                qgis.utils.startPlugin('tdn')
                
                    
            except (Exception, p.DatabaseError) as error:
                #print(str(error))
                show_message('gescheitert: ' + str(error))
                Info = 'gescheitert: ' + str(error)
        else:
            show_message('Keine Eingabe')
            Info = 'Keine Eingabe'
            
        return Info




        
        
