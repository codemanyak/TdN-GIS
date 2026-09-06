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
#Vorpprocessing, Dangles entfernen Geometrie neu strukturieren
######################################################

class snap_st:
    
    def __init__(self):       
       
        
        # Daten schreiben Funktion
        ### So ließe sich das handhaben
        #Wege definieren
        trassen = QgsProject.instance().mapLayersByName("sgv_trassen")[0]
        dlm_strassen = QgsProject.instance().mapLayersByName("strassen_wege")[0]
        osm_wege = QgsProject.instance().mapLayersByName("osm_wege")[0]
        
        # Configuration setzen
        ms = QgsMapSettings()
        u = QgsSnappingUtils()
        u.setMapSettings(ms)
        cfg = u.config()
        cfg.setEnabled(True)
        cfg.setIntersectionSnapping(True)
        cfg.setSelfSnapping(True)
        #cfg.intersectionSnapping()
        cfg.setMode(QgsSnappingConfig.AdvancedConfiguration)

        cfg.setIndividualLayerSettings(trassen,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.Vertex, 8, QgsTolerance.Pixels))
        cfg.setIndividualLayerSettings(dlm_strassen,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.VertexAndSegment, 6, QgsTolerance.Pixels))
        cfg.setIndividualLayerSettings(osm_wege,QgsSnappingConfig.IndividualLayerSettings(True, QgsSnappingConfig.VertexAndSegment, 8, QgsTolerance.Pixels))
        
        self.cfg = cfg
        

    def snap_an(self):
        cfg = self.cfg
        cfg.setEnabled(True)            
        QgsProject.instance().setSnappingConfig(cfg)
        
    def snap_aus(self):
        cfg = self.cfg
        cfg.setEnabled(False)            
        QgsProject.instance().setSnappingConfig(cfg)
    
            

            
