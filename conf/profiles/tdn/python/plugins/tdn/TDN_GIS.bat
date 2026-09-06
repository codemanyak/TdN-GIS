
cls
cls
@echo off
:: Codepage auf utf-8 setzen
chcp 65001

:: Die üblichen QGIS-Installationspfade für qgis 3.4 2.18 und gis 2.14  werden nacheinander geprüft
echo  **************************************************************************
echo Testen in welchem Verzeichnis sich die QGIS-Installation befindet

setlocal enableextensions
::pfad zum Skript ermitteln
set "scriptp=%~dp0"
::in Skript-Ordner wechseln
cd "%~dp0"
::Laufwerk wechseln
%~d0
echo ***************************************************************
echo Testen in welchem Verzeichnis sich die QGIS-Installation befindet


::QGIS suchen
for /d %%d in ("C:\Program Files\QGIS 3.4*"   "C:\Program Files\QGIS 3.3*"   "C:\Program Files\QGIS 3.2*"  "C:\Program Files\QGIS 3*"  "C:\Program Files (x86)\QGIS 3*" "C:\Programme (x86)\QGIS 3*"  "C:\Programme\QGIS 3*" "C:\OSGeo*" ) do call :checkQGIS "%%d"


::Nicht gefunden
::if "%ogrp%"=="" goto qf
::gefunden
::goto start

:checkQGIS
::echo.check %~1
if exist "%~1\bin\ogr2ogr.exe" set "ogrp=%~1"
::Nicht gefunden
if "%ogrp%"=="" goto qf
::goto :eof
goto start

    :qf
    echo.
    echo.
    set inst=nein
    echo ***************************************************************
    echo QGIS scheint nicht an einem üblichen Ort installiert zu sein?
    set /p inst="Ist QGIS installiert? ja oder nein? "
    if %inst%==nein goto wars
    echo Geben Sie den Pfad Ihrer QGIS-Installation ein:
    echo.
    set /p ogrp="Bitte vollen Pfad der QGIS-Installation eingeben: "
    set path=%path%;%ogrp%\bin;%scriptp%
    goto start
    :wars
    echo Skript wird abgebrochen - Bitte  QGIS installieren
    pause
    exit
    :start
    set "path=%path%;%ogrp%\bin\;%scriptp%"


echo.
echo ***************************************************************
echo QGIS ist installiert unter %ogrp%
echo  ***************************************************************
echo.

:: Neu 2019-12-01 Setzen der Umgebungsvariablen
SET GDAL_DATA=%ogrp%\share\gdal
SET GDAL_DRIVER_PATH=%ogrp%\bin\gdalplugins
SET PROJ_LIB=%ogrp%\share\proj

:: Python-Pfad etc.
call "%ogrp%\bin\o4w_env.bat"
if exist "%ogrp%\bin\py3_env.bat" call "%ogrp%\bin\py3_env.bat"


:: PGCONF setzen
if  exist "%scriptp%conf\pg_service.conf"  goto pgc

if exist "%scriptp%conf\profiles\tdn\python\plugins\tdn\pg_service.conf"  goto cp
:cp
copy "%scriptp%conf\profiles\tdn\python\plugins\tdn\pg_service.conf"  "%scriptp%conf\pg_service.conf" 

::set pg_conf="%scriptp%conf\profiles\tdn\python\plugins\tdn"

::goto pgc2
:pgc
echo %scriptp%
set pg_conf="%scriptp%conf"


:pgc2
echo ***********************************************************
echo Alte PG Variable:  %PGSYSCONFDIR% 
echo Neuer PG-Conf-Pfad: %pg_conf%
echo **********************************************************


echo  "%PGSYSCONFDIR%" NEQ %pg_conf%
if "%PGSYSCONFDIR%" NEQ %pg_conf% goto confsetz

goto qgstart

:confsetz

setx PGSYSCONFDIR %pg_conf%
echo.
echo *********************************************************************
echo Neuer Pfad für PostGis-Service gesetzt: Bitte noch einmal neu Starten
echo *********************************************************************
echo.
pause
exit



:qgstart
if not exist "%ogrp%\bin\qgis-ltr.bat" goto qgi2b


call "%ogrp%\bin\qgis-ltr.bat"  --profiles-path "%scriptp%conf" --profile tdn --project  "%scriptp%daten\TDN_2026.qgz"

:qgi2b

call "%ogrp%\bin\qgis.bat"  --profiles-path "%scriptp%conf" --profile tdn  --project  "%scriptp%daten\TDN_2026.qgz"

goto ende
:setzen


:ende
exit
