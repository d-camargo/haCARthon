# -*- coding: utf-8 -*-
"""
Estilos nativos aplicados automaticamente às saídas da detecção, para que os
conflitos apareçam destacados no mapa sem configuração manual.
"""
from qgis.core import (QgsFillSymbol,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory,
                       QgsGraduatedSymbolRenderer, QgsRendererRange)


def estilo_conflitos(layer):
    """Camada de geometrias de conflito: categoriza por tipo (tons de vermelho)."""
    if layer is None:
        return
    cats = [
        QgsRendererCategory(
            'CARxAssentamento',
            QgsFillSymbol.createSimple({'color': '200,30,30,170',
                                        'outline_color': '120,0,0,255',
                                        'outline_width': '0.4'}),
            'CAR × Assentamento (INCRA)'),
        QgsRendererCategory(
            'CARxCAR',
            QgsFillSymbol.createSimple({'color': '230,120,40,150',
                                        'outline_color': '180,60,0,255',
                                        'outline_width': '0.3'}),
            'CAR × CAR'),
    ]
    layer.setRenderer(QgsCategorizedSymbolRenderer('tipo', cats))
    layer.triggerRepaint()


def estilo_fila(layer):
    """Camada da fila (imóveis): gradua por 'score' (sem conflito → claro; alto → vermelho)."""
    if layer is None:
        return
    def faixa(low, high, props, label):
        return QgsRendererRange(low, high, QgsFillSymbol.createSimple(props), label)

    ranges = [
        faixa(-0.0001, 0.0001,
              {'style': 'no', 'outline_color': '150,150,150,180', 'outline_width': '0.15'},
              'Sem conflito'),
        faixa(0.0001, 10,
              {'color': '255,221,87,110', 'outline_color': '200,160,0,255', 'outline_width': '0.2'},
              'Baixo (< 10)'),
        faixa(10, 50,
              {'color': '255,150,40,150', 'outline_color': '200,90,0,255', 'outline_width': '0.25'},
              'Médio (10–50)'),
        faixa(50, 1e9,
              {'color': '214,40,40,180', 'outline_color': '130,0,0,255', 'outline_width': '0.4'},
              'Alto (≥ 50 · assentamento)'),
    ]
    renderer = QgsGraduatedSymbolRenderer('score', ranges)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
