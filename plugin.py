#!python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# initialize Qt resources from file resouces.py
import resources
import json
class TiledMapPlugin:
  def __init__(self, iface):
    self.iface = iface
    xml = """<GDAL_WMS>
    <Service name="TMS">
        <ServerUrl>[URL]</ServerUrl>
    </Service>
    <DataWindow>
        <UpperLeftX>-20037508.34</UpperLeftX>
        <UpperLeftY>20037508.34</UpperLeftY>
        <LowerRightX>20037508.34</LowerRightX>
        <LowerRightY>-20037508.34</LowerRightY>
        <TileLevel>[MAXZOOM]</TileLevel>
        <TileCountX>1</TileCountX>
        <TileCountY>1</TileCountY>
        <YOrigin>top</YOrigin>
    </DataWindow>
    <Projection>EPSG:3785</Projection>
    <BlockSizeX>256</BlockSizeX>
    <BlockSizeY>256</BlockSizeY>
    <BandsCount>3</BandsCount>
    <MaxConnections>5</MaxConnections>
    <Cache>
        <Path>[SETTINGSDIR]cache/tiled_map_plugin</Path>
    </Cache>
</GDAL_WMS>"""
    self.xml = xml.replace('[SETTINGSDIR]', QgsApplication.qgisSettingsDirPath())
    tile_server_file = QgsApplication.qgisSettingsDirPath() + 'tile_servers.json'
    f = open(tile_server_file)
    self.tile_servers = json.load(f)
    f.close()
#    self.tile_servers = [ { 'name': 'MLM Background', 'url': 'http://a.tile.openstreetmap.de:8002/tiles/1.0.0/bg//${z}/${x}/${y}.png', 'maxzoom': '18' },
#                          { 'name': 'tile.osm.org', 'url': 'http://tile.openstreetmap.org/${z}/${x}/${y}.png', 'maxzoom': '18' } ]
  def initGui(self):
    for tile_server in self.tile_servers:
        action = QAction(QIcon(":/images/themes/default/mActionAddWmsLayer.png"), 'Add layer ' + tile_server['name'], self.iface.mainWindow())
        tile_server['action'] = action
        f = (lambda x: lambda : self.run(x))(tile_server)
        QObject.connect(action, SIGNAL("triggered()"), f)
        self.iface.addPluginToMenu("TiledMap", action)
  def unload(self):
    for tile_server in self.tile_servers:
        self.iface.removePluginMenu("TiledMap", tile_server['action'])
  def run(self, tile_server):
    rlayer = QgsRasterLayer(self.xml.replace('[URL]', tile_server['url']).replace('[MAXZOOM]', tile_server['maxzoom']), tile_server['name'])
    if not rlayer.isValid():
        print "Layer failed to load!"
        return
    QgsMapLayerRegistry.instance().addMapLayer(rlayer)
