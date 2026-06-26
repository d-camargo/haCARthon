# -*- coding: utf-8 -*-
"""
Print Layout com Atlas para o parecer/RAT, em 2 páginas (A4 retrato) por imóvel:
  Página 1: cabeçalho centralizado (logo grande + identificação) + mapa + legenda/escala.
  Página 2: logo + cabeçalho "Memória de Cálculo" centralizado + o parecer (HTML).
"""
import os
from qgis.core import (Qgis, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
                       QgsLayoutItemLegend, QgsLayoutItemScaleBar, QgsLayoutItemPicture,
                       QgsLayoutItemPage, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes)
from qgis.PyQt.QtGui import QFont, QColor
from qgis.PyQt.QtCore import Qt

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
    LABEL_HTML = QgsLayoutItemLabel.Mode.ModeHtml
except AttributeError:
    LABEL_HTML = QgsLayoutItemLabel.ModeHtml
try:
    PIC_ZOOM = QgsLayoutItemPicture.ResizeMode.Zoom
except AttributeError:
    PIC_ZOOM = QgsLayoutItemPicture.Zoom
try:
    PORTRAIT = QgsLayoutItemPage.Orientation.Portrait
except AttributeError:
    PORTRAIT = QgsLayoutItemPage.Portrait
try:
    HCENTER = Qt.AlignmentFlag.AlignHCenter
    VCENTER = Qt.AlignmentFlag.AlignVCenter
except AttributeError:
    HCENTER = Qt.AlignHCenter
    VCENTER = Qt.AlignVCenter

_ICON = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon.svg')
_PW = 210.0  # largura A4 (mm)


def _coloca(item, x, y, w, h, page=0):
    item.attemptResize(QgsLayoutSize(w, h, MM))
    item.attemptMove(QgsLayoutPoint(x, y, MM), True, False, page)


def _logo(layout, lado, y, page):
    if not os.path.exists(_ICON):
        return
    pic = QgsLayoutItemPicture(layout)
    pic.setPicturePath(_ICON)
    pic.setResizeMode(PIC_ZOOM)
    layout.addLayoutItem(pic)
    _coloca(pic, (_PW - lado) / 2.0, y, lado, lado, page)  # centralizado


def _label(layout, texto, x, y, w, h, page, size, bold=False, color=(60, 60, 60), center=False, html=False):
    lb = QgsLayoutItemLabel(layout)
    if html:
        lb.setMode(LABEL_HTML)
    lb.setText(texto)
    f = QFont(); f.setPointSize(size); f.setBold(bold)
    lb.setFont(f)
    lb.setFontColor(QColor(*color))
    if center:
        lb.setHAlign(HCENTER)
        lb.setVAlign(VCENTER)
    layout.addLayoutItem(lb)
    _coloca(lb, x, y, w, h, page)
    return lb


def criar_layout_parecer(project, cobertura, map_layers, nome="Parecer Pré-Val CAR"):
    if cobertura is None:
        return None

    manager = project.layoutManager()
    antigo = manager.layoutByName(nome)
    if antigo:
        manager.removeLayout(antigo)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()  # página 1 (A4 retrato)
    layout.setName(nome)
    pagina2 = QgsLayoutItemPage(layout)
    pagina2.setPageSize('A4', PORTRAIT)
    layout.pageCollection().addPage(pagina2)

    # ===================== PÁGINA 1: identificação + mapa =====================
    _logo(layout, 60, 10, page=0)
    _label(layout, "PARECER DE PRÉ-VALIDAÇÃO TÉCNICA — Pré-Val CAR",
           10, 74, 190, 10, 0, size=14, bold=True, color=(44, 62, 80), center=True)
    _label(layout, "Imóvel: [% cod_imovel %]   ·   Município: [% municipio %]   ·   "
                   "Score de risco: [% round(score, 1) %]",
           10, 85, 190, 7, 0, size=10, color=(90, 90, 90), center=True)

    mapa = QgsLayoutItemMap(layout)
    layout.addLayoutItem(mapa)
    _coloca(mapa, 10, 96, 190, 158, 0)
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

    legenda = QgsLayoutItemLegend(layout)
    legenda.setTitle("Legenda")
    legenda.setLinkedMap(mapa)
    legenda.setAutoUpdateModel(True)
    layout.addLayoutItem(legenda)
    _coloca(legenda, 10, 257, 95, 33, 0)

    barra = QgsLayoutItemScaleBar(layout)
    barra.setStyle('Single Box')
    barra.setLinkedMap(mapa)
    barra.applyDefaultSize()
    layout.addLayoutItem(barra)
    _coloca(barra, 120, 258, 80, 12, 0)

    barra_num = QgsLayoutItemScaleBar(layout)
    barra_num.setStyle('Numeric')
    barra_num.setLinkedMap(mapa)
    layout.addLayoutItem(barra_num)
    _coloca(barra_num, 120, 272, 80, 6, 0)

    # ===================== PÁGINA 2: memória de cálculo =====================
    _logo(layout, 40, 10, page=1)
    _label(layout, "MEMÓRIA DE CÁLCULO",
           10, 54, 190, 12, 1, size=18, bold=True, color=(44, 62, 80), center=True)
    _label(layout, "[% parecer_html %]",
           10, 70, 190, 215, 1, size=9, color=(51, 51, 51), html=True)

    # ===================== Atlas =====================
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
