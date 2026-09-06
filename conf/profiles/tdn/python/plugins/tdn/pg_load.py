import os

from qgis.core import *



##############################################
#Postgis-Verbindung inititieren
######################################################

class pg_load:
	# Daten schreiben Funktion
	def pgl(self,schema,tab,geom,fid,name):
		# Service-datei auslesen'#
		#########################
		# projektpfad ermitteln
		pfad = QgsProject.instance().homePath() 

		# ein Verzeichnis hoeher
		oberhalb = os.path.dirname(pfad)
		# Von dort zum verzeichnis mit der pg_service.conf
		pfad = os.path.join(str(oberhalb) + '/' + 'conf/' + 'pg_service.conf')
		# Normpfad für Windows
		pfad = os.path.normcase(pfad)

		# zeilen aus der Servicedatei lesen
		pa_list = []
		datei = open(pfad,'r') 
		for zeile in datei:
			ze = zeile.replace('\n','')
			pa_list.append(ze)
		datei.close()
		print(pa_list)

		#aus der resultierenden Liste die Verbindungsparamemer den Variablen zuordnen, dabei die Bezeichnungen entfernen
		host = (pa_list[1]).replace('host=','')
		port = (pa_list[2]).replace('port=','')
		user = (pa_list[3]).replace('user=','')
		password = (pa_list[4]).replace('password=','')
		dbname = (pa_list[6]).replace('dbname=','')

		uri = QgsDataSourceUri()
		#Datenbankverbidnung connectionString erzuegen
		uri.setConnection(host, port, dbname, user, password ,sslmode=3)
		#Gewünschten Layer über die mit der Funktion übergebennen Prammeter wählen
		uri.setDataSource(schema, tab, geom,"",fid)
		# QGIS-Vektorlayer erzeugen
		pglayer=QgsVectorLayer(uri.uri(False), name, "postgres")
		# Vektorlayer laden

		#QgsProject.instance().addMapLayer(pglayer)
		return pglayer

####################################################

	'''

	uri = QgsDataSourceUri()
	uri.setConnection(host, port, dbname, user, password ,sslmode=3)
	uri.setDataSource ("sgv", "sta_geometryanalyse", "ring_geom","","fid")
	pgl=QgsVectorLayer (uri .uri(False), "sta_line_ring", "postgres")
	QgsProject.instance().addMapLayer(pgl)

	from qgis.core import QgsVectorLayer, QgsDataSourceUri
	uri = QgsDataSourceUri()
	uri.setConnection("gis.sgv.de", "51353", "sgv_gis", "claas", "fraxinus!",sslmode=3)
	uri.setDataSource ("sgv", "sta_geometryanalyse", "ring_geom","fid is not NULL","fid")
	vlayer=QgsVectorLayer (uri .uri(False), "sta_line_ring", "postgres")
	QgsProject.instance().addMapLayer(vlayer)


	SslRequire = 3
	sslmode=require;



	################################################################
	setConnection(self, aHost: str, aPort: str, aDatabase: str, aUsername: str, aPassword: str, sslmode: QgsDataSourceUri.SslMode = QgsDataSourceUri.SslPrefer, authConfigId: str = '')¶

Sets all connection related members at once.

setConnection(self, aService: str, aDatabase: str, aUsername: str, aPassword: str, sslmode: QgsDataSourceUri.SslMode = QgsDataSourceUri.SslPrefer, authConfigId: str = ‘’) Sets all connection related members at once (for a service case).

Parameters

aHost (str) –

aPort (str) –

aDatabase (str) –

aUsername (str) –

aPassword (str) –

sslmode (QgsDataSourceUri.SslMode = QgsDataSourceUri.SslPrefer) –

authConfigId (str = '') –

	#########################

	setDataSource(self, aSchema: str, aTable: str, aGeometryColumn: str, aSql: str = '', aKeyColumn: str = '')¶

Sets all data source related members at once.

Parameters

aSchema (str) –

aTable (str) –

aGeometryColumn (str) –

aSql (str = '') –

aKeyColumn (str = '') –

	####################################


	dbname='sgv_gis' host=gis.sgv.de port=51353 user='claas' checkPrimaryKeyUnicity='1' table="sgv"."sta_geometryanalyse" (ring_geom)

	service='sgv_gis' sslmode=require key='fid' srid=25832 type=MultiLineString checkPrimaryKeyUnicity='1' table="sgv"."sta_geometryanalyse" (ring_geom)


	uri = QgsDataSourceURI()
	# set host name, port, database name, username and password
	uri.setConnection("localhost", "5432", "dbname", "johny", "xxx")
	# set database schema, table name, geometry column and optionaly subset (WHERE clause)
	uri.setDataSource("public", "roads", "the_geom", "cityid = 2643")

	vlayer = QgsVectorLayer(uri.uri(), "layer_name_you_like", "postgres")







	uri = QgsDataSourceUri()
	uri.setConnection("localhost", "5432", "myDatabase", "myUser", "myPassword")
	uri.setDataSource("mySchema", "myTable", "myGeomField", aKeyColumn="myUniqueIdField")
	vlayer = iface.addVectorLayer(uri.uri(False), "nameOfMyLayer", "postgres")

	'''







