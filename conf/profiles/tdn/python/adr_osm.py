"""Autor: Stefan Giese, 17.03.2020
Geändert Claas Leiner 02-03.2022"""
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
import urllib.request, json

@qgsfunction(args='auto', group='Geocode')
def adr_osm(w1,feature, parent):
    """
    Reverse geocoding for Point features
    <h2>Example usage:</h2>
    <ul>
      <li>reverse_geocode() -> Schwimmbadstr. 2, 79100 Freiburg, Deutschland</li>
    </ul>
    """
    #if feature.attribute() =="":
    address = ""
    geom = feature.geometry()
    if geom.type() != 0:
        geom=geom.centroid()
    if geom.type() == 0: #Nur Punktgeometrien
        sourceCrs = iface.activeLayer().crs()  #Koordinatensystem bestimmen
        if sourceCrs.srsid()!=4326: #Umprojizieren falls nicht WGS84
            destCrs = QgsCoordinateReferenceSystem("EPSG:4326")
            tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
            geom.transform(tr)   

        x = geom.asPoint().x()  #Koordinaten bestimmen
        y = geom.asPoint().y()
        #Koordinaten an Nominatim übergeben
        url = "http://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=1&limit=1".format(y,x)
        #response = urllib.request.urlopen(url) #Anfrage stellen 
        #data = json.loads(response.read()) #Ergebnisse in ein Pythonojekt konvertieren
        headers = {
        "User-Agent": "GKG-Kassel (claas.leiner@gkg-kassel.de)"
        }
        req = urllib.request.Request(url, headers=headers)        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if data:  #Adressse zusammenstellen
            if w1 == 'plz':
                address = data["address"].get("postcode","")
            elif w1 == 'add':
                address = data["address"].get("road","")+ ' ' + data["address"].get("house_number","")
            elif w1 == 'cit':
                address = data["address"].get("city","") + data["address"].get("town","") + data["address"].get("village","")
            elif w1 == 'str':
                address = data["address"].get("road","")
            elif w1 == 'hnr':
                address =  data["address"].get("house_number","")
        
    return address
