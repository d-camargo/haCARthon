# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayer
import urllib.parse
from datetime import datetime

def build_sicar_wfs_uri(uf, municipio):
    """
    Constrói a URI WFS para acessar o geoserver do SICAR filtrado por município.
    """
    uf_lower = uf.lower()
    muni_encoded = urllib.parse.quote(municipio)
    
    base_url = "https://geoserver.car.gov.br/geoserver/sicar/wfs"
    # Adicionamos srsName=EPSG:4674 para garantir a projeção
    uri = f"WFS:{base_url}?service=WFS&version=2.0.0&request=GetFeature&typeNames=sicar:sicar_imoveis_{uf_lower}&srsName=EPSG:4674&CQL_FILTER=municipio='{muni_encoded}'"
    return uri

def load_sicar_layer(uf, municipio, layer_name=None):
    """
    Carrega a camada WFS do SICAR como um QgsVectorLayer.
    """
    if not layer_name:
        layer_name = f"CAR - {municipio} ({uf})"
    
    uri = build_sicar_wfs_uri(uf, municipio)
    layer = QgsVectorLayer(uri, layer_name, "WFS")
    
    # Registra proveniência da base
    layer.setCustomProperty("data_extracao", datetime.now().strftime("%Y-%m-%d"))
    layer.setCustomProperty("fonte", "SICAR WFS")
    
    return layer

def build_incra_wfs_uri(uf):
    """
    Constrói a URI WFS para acessar o geoserver i3geo do INCRA.
    O WFS 1.0.0 do MapServer do INCRA envia lat,lon. 
    Usamos InvertAxisOrientation=1 para o PyQGIS tratar isso nativamente para EPSG:4674 (lon,lat).
    """
    uf_lower = uf.lower()
    base_url = "https://acervofundiario.incra.gov.br/i3geo/ogc.php"
    
    uri = f"WFS:{base_url}?service=WFS&version=1.0.0&request=GetFeature&typename=assentamentos_{uf_lower}&srsName=EPSG:4674&InvertAxisOrientation=1"
    return uri

def load_incra_layer(uf, layer_name=None):
    """
    Carrega a camada WFS do INCRA como um QgsVectorLayer.
    """
    if not layer_name:
        layer_name = f"Assentamentos INCRA - {uf}"
        
    uri = build_incra_wfs_uri(uf)
    layer = QgsVectorLayer(uri, layer_name, "WFS")
    
    if layer.isValid():
        layer.setCustomProperty("data_extracao", datetime.now().strftime("%Y-%m-%d"))
        layer.setCustomProperty("fonte", "INCRA i3geo")
        
        # Aliasing para visualização no QGIS, caso não seja exportado para outra camada
        idx = layer.fields().lookupField('nome_projeto')
        if idx != -1:
            layer.setEditorWidgetSetup(idx, layer.editorWidgetSetup(idx))
            layer.setFieldAlias(idx, 'nome')

    return layer
