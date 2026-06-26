# -*- coding: utf-8 -*-
"""
Monta um Print Layout com Atlas para o parecer/RAT: 1 página por imóvel em conflito,
com mapa (zoom no imóvel) + o HTML do parecer (campo 'parecer_html').
"""
from qgis.core import (Qgis, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
                       QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes)

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
    cobertura  : camada com 'parecer_html', 'cod_imovel', 'conflito' (saída do passo 3).
    map_layers : camadas a desenhar no mapa (geometrias de conflito, fila, assentamentos).
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

    # Título (HTML + expressões do Atlas)
    titulo = QgsLayoutItemLabel(layout)
    titulo.setMode(LABEL_HTML)
    titulo.setText(
        '<b style="font-size:13pt; color:#2c3e50;">PARECER DE PRÉ-VALIDAÇÃO TÉCNICA</b><br>'
        '<span style="color:#555;">Imóvel: [% "cod_imovel" %] &nbsp;·&nbsp; '
        'Município: [% "municipio" %] &nbsp;·&nbsp; Score de risco: [% round("score",1) %]</span>'
    )
    layout.addLayoutItem(titulo)
    _coloca(titulo, 10, 8, 190, 16)

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

    # Parecer (HTML por feição)
    parecer = QgsLayoutItemLabel(layout)
    parecer.setMode(LABEL_HTML)
    parecer.setText('[% "parecer_html" %]')
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
