import os

from qgis.core import QgsVectorLayer, QgsDataSourceUri

pfad = QgsProject.instance().homePath() 

oberhalb = os.path.dirname(pfad)

pfad = os.path.join(str(oberhalb) + '/' + 'conf/' + 'pg_service.conf')

pfad = os.path.normcase(pfad)

pa_list = []
datei = open(pfad,'r') 
for zeile in datei:
    ze = zeile.replace('\n','')
    pa_list.append(ze)
datei.close()
print(pa_list)

host = (pa_list[1]).replace('host=','')
port = (pa_list[2]).replace('port=','')
user = (pa_list[3]).replace('user=','')
password = (pa_list[4]).replace('password=','')
dbname = (pa_list[6]).replace('dbname=','')



uri = QgsDataSourceUri()
uri.setConnection(host, port, dbname, user, password ,sslmode=3)
uri.setDataSource ("sgv", "sta_geometryanalyse", "ring_geom","","fid")
vlayer=QgsVectorLayer (uri .uri(False), "sta_line_ring", "postgres")
QgsProject.instance().addMapLayer(vlayer)

####################################################

'''
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











if( "strecke" >= 25,
with_variable('rech',

			(
			case
				when floor("kilomet") % 4 = 0
				then floor("kilomet") 
				else ceil("kilomet") 
			end
			),
 with_variable('rune',
					
			case 
			WHEN round((@rech % 4),1)  = 0 THEN @rech 
			when  round((@rech % 4),1)  >= 3 then ((@rech ) + 1) 
			when  round((@rech % 4),1) > 2 then ((@rech )  + 2) 
			when  round((@rech % 4),1)  <= 1 then ((@rech ) - 1) 
			when  round((@rech % 4),1)  <= 2  then ((@rech ) - 2) 
			
			else @rech 
			end
			,
	case
	when 
	"fid" < (maximum(fid) -1) then @rune

		

	else 
		with_variable('l2d',
				
		(
			"strecke" -
			  (
			  maximum(  @rune,
			 "name",
			 "fid" = (maximum("fid") -2)
			 ) -4
			 ) 
			 ) 
			/ 2
			 ,
			 
			 
				case
				when "fid" = maximum("fid")
				then round("kilomet",1)
				when "fid" = (maximum("fid") -1) 
				then  round(( "strecke"  - @l2d),1)
				else "kilomet"
				end
				
					
)

end
)
),
"kilomet"
)
'''
