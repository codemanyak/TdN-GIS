#!/bin/bash


ver="$(pwd)"   
qgis --profiles-path "$ver/conf" --profile tdn --project "$ver/daten/TDN_2026.qgz"
