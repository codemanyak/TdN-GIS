# encoding: utf-8
#-----------------------------------------------------------
# Claas Leiner GKG auf Grundlage von:
# 2020 Thomas Baumann Fork von
# based on qgis-minimal-plugin from Martin Dobias
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

# noinspection PyPep8Naming
def classFactory(iface):  
    from .tdn import tdn
    return tdn(iface)
