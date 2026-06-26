# -*- coding: utf-8 -*-
"""
Monta um Print Layout com Atlas para o parecer/RAT: 1 página por imóvel em conflito,
com mapa (zoom no imóvel) + o HTML do parecer (campo 'parecer_html').

Notas:
- Expressões usam os campos SEM aspas duplas ([% cod_imovel %]); em rótulos HTML as
  aspas viram &quot; e quebram a expressão.
- Título/subtítulo ficam em modo fonte (avaliação de expressão confiável); só o parecer
  usa modo HTML.
"""
from qgis.core import (Qgis, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
                       QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes)
from qgis.PyQt.QtGui import QFont, QColor

# --- compat de enums (Qt5/Qt6) ---
try:
    MM = Qgis.LayoutUnit.Millimeters
except AttributeError:
    MM = QgsUnitTypes.LayoutMillimeters
try:
    LABEL_HTML = QgsLayoutItemLabel.Mode.ModeHtml
except AttributeError:
    LABEL_HTML = QgsLayoutItemLabel.ModeHtml
try:
    MAP_AUTO = QgsLayoutItemMap.AtlasScalingMode.Auto
except AttributeError:
    MAP_AUTO = QgsLayoutItemMap.Auto


def _coloca(item, x, y, w, h):
    item.attemptMove(QgsLayoutPoint(x, y, MM))
    item.attemptResize(QgsLayoutSize(w, h, MM))


def criar_layout_parecer(project, cobertura, map_layers, nome="Parecer Pré-Val CAR"):
    """
    cobertura  : camada com 'parecer_html', 'cod_imovel', 'municipio', 'score', 'conflito'.
    map_layers : camadas a desenhar no mapa.
    Retorna o QgsPrintLayout (já adicionado ao gerenciador do projeto).
    """
    if cobertura is None:
        return None

    manager = project.layoutManager()
    antigo = manager.layoutByName(nome)
    if antigo:
        manager.removeLayout(antigo)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()  # A4 retrato
    layout.setName(nome)

    # Título (modo fonte)
    titulo = QgsLayoutItemLabel(layout)
    titulo.setText("PARECER DE PRÉ-VALIDAÇÃO TÉCNICA — Pré-Val CAR")
    f = QFont(); f.setPointSize(13); f.setBold(True)
    titulo.setFont(f)
    titulo.setFontColor(QColor(44, 62, 80))
    layout.addLayoutItem(titulo)
    _coloca(titulo, 10, 8, 190, 9)

    # Subtítulo com expressões do Atlas (campos SEM aspas duplas)
    sub = QgsLayoutItemLabel(layout)
    sub.setText("Imóvel: [% cod_imovel %]   ·   Município: [% municipio %]   ·   "
                "Score de risco: [% round(score, 1) %]")
    fs = QFont(); fs.setPointSize(9)
    sub.setFont(fs)
    sub.setFontColor(QColor(90, 90, 90))
    layout.addLayoutItem(sub)
    _coloca(sub, 10, 17, 190, 7)

    # Mapa (segue o Atlas, com zoom no imóvel)
    mapa = QgsLayoutItemMap(layout)
    layout.addLayoutItem(mapa)
    _coloca(mapa, 10, 26, 190, 95)
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

    # Parecer (modo HTML; expressão sem aspas duplas)
    parecer = QgsLayoutItemLabel(layout)
    parecer.setMode(LABEL_HTML)
    parecer.setText("[% parecer_html %]")
    layout.addLayoutItem(parecer)
    _coloca(parecer, 10, 125, 190, 162)

    # Atlas: 1 página por imóvel em conflito, ordenado por score desc.
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
