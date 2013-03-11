#!python
def name():
 return "TiledMap"
def description():
 return "Add tiled web maps as raster layer."
def version():
 return "Version 1.0"
def qgisMinimumVersion(): 
 return "1.8"
def authorName():
 return "Jochen Topf"
def classFactory(iface):
 from plugin import TiledMapPlugin
 return TiledMapPlugin(iface)
