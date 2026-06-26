# -*- coding: utf-8 -*-
"""
Print Layout com Atlas para o parecer/RAT: 1+ páginas por imóvel em conflito.
Cabeçalho com ícone, mapa (zoom no imóvel), legenda, escala gráfica e numérica, e o
parecer em HTML que flui para novas páginas quando há muitas sobreposições.
"""
import os
from qgis.core import (Qgis, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
                       QgsLayoutItemLegend, QgsLayoutItemScaleBar, QgsLayoutItemPicture,
                       QgsLayoutItemHtml, QgsLayoutFrame, QgsLayoutMultiFrame,
                       QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes)
from qgis.PyQt.QtGui import QFont, QColor

# --- compat de enums (Qt5/Qt6) ---
try:
    MM = Qgis.LayoutUnit.Millimeters
except AttributeError:
    MM = QgsUnitTypes.LayoutMillimeters
try:
    MAP_AUTO = QgsLayoutItemMap.AtlasScalingMode.Auto
except AttributeError:
    MAP_AUTO = QgsLayoutItemMap.Auto
try:
    HTML_MANUAL = QgsLayoutItemHtml.ContentMode.ManualHtml
except AttributeError:
    HTML_MANUAL = QgsLayoutItemHtml.ManualHtml
try:
    RESIZE_EXTEND = QgsLayoutMultiFrame.ResizeMode.ExtendToNextPage
except AttributeError:
    RESIZE_EXTEND = QgsLayoutMultiFrame.ExtendToNextPage

_ICON = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon.svg')


def _coloca(item, x, y, w, h):
    item.attemptMove(QgsLayoutPoint(x, y, MM))
    item.attemptResize(QgsLayoutSize(w, h, MM))


def criar_layout_parecer(project, cobertura, map_layers, nome="Parecer Pré-Val CAR"):
    if cobertura is None:
        return None

    manager = project.layoutManager()
    antigo = manager.layoutByName(nome)
    if antigo:
        manager.removeLayout(antigo)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()  # A4 retrato
    layout.setName(nome)

    # --- Cabeçalho: ícone + título + subtítulo ---
    if os.path.exists(_ICON):
        pic = QgsLayoutItemPicture(layout)
        pic.setPicturePath(_ICON)
        layout.addLayoutItem(pic)
        _coloca(pic, 180, 6, 20, 20)

    titulo = QgsLayoutItemLabel(layout)
    titulo.setText("PARECER DE PRÉ-VALIDAÇÃO TÉCNICA — Pré-Val CAR")
    f = QFont(); f.setPointSize(13); f.setBold(True)
    titulo.setFont(f); titulo.setFontColor(QColor(44, 62, 80))
    layout.addLayoutItem(titulo)
    _coloca(titulo, 10, 8, 165, 9)

    sub = QgsLayoutItemLabel(layout)
    sub.setText("Imóvel: [% cod_imovel %]   ·   Município: [% municipio %]   ·   "
                "Score de risco: [% round(score, 1) %]")
    fs = QFont(); fs.setPointSize(9)
    sub.setFont(fs); sub.setFontColor(QColor(90, 90, 90))
    layout.addLayoutItem(sub)
    _coloca(sub, 10, 18, 165, 7)

    # --- Mapa: apenas os polígonos objeto do parecer (conflitos + imóvel) ---
    mapa = QgsLayoutItemMap(layout)
    layout.addLayoutItem(mapa)
    _coloca(mapa, 10, 28, 190, 88)
    mapa.setFrameEnabled(True)
    if map_layers:
        mapa.setLayers(map_layers)
    try:
        mapa.setCrs(cobertura.crs())
        mapa.zoomToExtent(cobertura.extent())
    except Exception:
        pass
    mapa.setAtlasDriven(True)
    mapa.setAtlasScalingMode(MAP_AUTO)
    mapa.setAtlasMargin(0.25)

    # --- Legenda ---
    legenda = QgsLayoutItemLegend(layout)
    legenda.setTitle("Legenda")
    legenda.setLinkedMap(mapa)
    legenda.setAutoUpdateModel(True)
    layout.addLayoutItem(legenda)
    _coloca(legenda, 10, 119, 90, 22)

    # --- Escala gráfica + numérica ---
    barra = QgsLayoutItemScaleBar(layout)
    barra.setStyle('Single Box')
    barra.setLinkedMap(mapa)
    barra.applyDefaultSize()
    layout.addLayoutItem(barra)
    _coloca(barra, 110, 120, 90, 12)

    barra_num = QgsLayoutItemScaleBar(layout)
    barra_num.setStyle('Numeric')
    barra_num.setLinkedMap(mapa)
    layout.addLayoutItem(barra_num)
    _coloca(barra_num, 110, 133, 90, 6)

    # --- Parecer (HTML que flui para novas páginas) ---
    html = QgsLayoutItemHtml(layout)
    layout.addMultiFrame(html)
    html.setContentMode(HTML_MANUAL)
    html.setEvaluateExpressions(True)
    html.setHtml("[% parecer_html %]")
    frame = QgsLayoutFrame(layout, html)
    _coloca(frame, 10, 144, 190, 145)
    html.addFrame(frame)
    html.setResizeMode(RESIZE_EXTEND)
    try:
        html.loadHtml()
    except Exception:
        pass

    # --- Atlas: 1 página por imóvel em conflito, ordenado por score desc. ---
    atlas = layout.atlas()
    atlas.setEnabled(True)
    atlas.setCoverageLayer(cobertura)
    atlas.setFilterFeatures(True)
    atlas.setFilterExpression('"conflito" = 1')
    atlas.setSortFeatures(True)
    atlas.setSortExpression('"score"')
    atlas.setSortAscending(False)

    manager.addLayout(layout)
    return layout
