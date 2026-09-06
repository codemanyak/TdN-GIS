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


##############################################
#Sanpping einstellen
######################################################

class snap_st:

    def snap(self,schalt):
        # Daten schreiben Funktion
        ### So ließe sich das handhaben
        #Wege definieren
        skizzen = QgsProject.instance().mapLayersByName("SkizzenStrecke")[0]
        trassen = QgsProject.instance().mapLayersByName("StreckenPlan")[0]
        punkte = QgsProject.instance().mapLayersByName("Punkte")[0]
        osm_wege = QgsProject.instance().mapLayersByName("osm_wege")[0]
        #waben = QgsProject.instance().mapLayersByName("waben")[0]
        #waben_zone = QgsProject.instance().mapLayersByName("waben_zone")[0]
        
        # Configuration setzen
        ms = QgsMapSettings()
        u = QgsSnappingUtils()
        u.setMapSettings(ms)
        cfg = u.config()
        cfg.setEnabled(True)
        cfg.setIntersectionSnapping(False)
        cfg.setSelfSnapping(False)
        #cfg.intersectionSnapping()
        cfg.setMode(QgsSnappingConfig.AdvancedConfiguration)

        cfg.setIndividualLayerSettings(trassen,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 12, QgsTolerance.Pixels))
        cfg.setIndividualLayerSettings(punkte,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 10, QgsTolerance.Pixels))
        cfg.setIndividualLayerSettings(skizzen,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 10, QgsTolerance.Pixels))
        cfg.setIndividualLayerSettings(osm_wege,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.VertexAndSegment, 10, QgsTolerance.Pixels))
        
        #cfg.setIndividualLayerSettings(waben,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 6, QgsTolerance.Pixels))
        #cfg.setIndividualLayerSettings(waben_zone,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 6, QgsTolerance.Pixels))
        
        if schalt == 'an':
            cfg.setEnabled(True)
            iface.mainWindow().findChildren(QAction, "EnableTracingAction")[0].setChecked(True)
        elif schalt == 'aus':
            cfg.setEnabled(False)
            iface.mainWindow().findChildren(QAction, "EnableTracingAction")[0].setChecked(False)
            
        QgsProject.instance().setSnappingConfig(cfg)

            

            
