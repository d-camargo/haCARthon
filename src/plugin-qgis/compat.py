# -*- coding: utf-8 -*-
"""
Compatibilidade de enums entre QGIS 3.x (PyQt5) e QGIS 4.x (PyQt6).

Centraliza, num só lugar, os pontos de API que mudaram de escopo entre as duas
linhas, para o plugin rodar tanto na 3.x (LTR) quanto na 4.x sem espalhar `try/except`.
"""
from qgis.core import Qgis, QgsFeatureSink, QgsProcessingParameterNumber, QgsFeatureRequest

# --- Tipos de campo (construtor do QgsField) ---
# A partir do QGIS 3.38 o construtor usa QMetaType; antes, QVariant (removido no PyQt6).
if Qgis.versionInt() >= 33800:
    from qgis.PyQt.QtCore import QMetaType
    FIELD_STRING = QMetaType.Type.QString
    FIELD_DOUBLE = QMetaType.Type.Double
    FIELD_INT = QMetaType.Type.Int
else:  # QGIS < 3.38 (PyQt5)
    from qgis.PyQt.QtCore import QVariant
    FIELD_STRING = QVariant.String
    FIELD_DOUBLE = QVariant.Double
    FIELD_INT = QVariant.Int

# --- Tipos de geometria / WKB (Qgis.* é escopado e estável em 3.30+/4.x) ---
GEOM_POLYGON = Qgis.GeometryType.Polygon
WKB_MULTIPOLYGON = Qgis.WkbType.MultiPolygon

# --- Flags/enums com escopo alterado no Qt6 ---
try:
    FAST_INSERT = QgsFeatureSink.Flag.FastInsert
except AttributeError:
    FAST_INSERT = QgsFeatureSink.FastInsert

try:
    PARAM_NUMBER_DOUBLE = QgsProcessingParameterNumber.Type.Double
except AttributeError:
    PARAM_NUMBER_DOUBLE = QgsProcessingParameterNumber.Double

try:
    LOG_CRITICAL = Qgis.MessageLevel.Critical
    LOG_INFO = Qgis.MessageLevel.Info
    LOG_WARNING = Qgis.MessageLevel.Warning
except AttributeError:
    LOG_CRITICAL = Qgis.Critical
    LOG_INFO = Qgis.Info
    LOG_WARNING = Qgis.Warning

# --- Política de geometria inválida (deixa o algoritmo tratar via makeValid) ---
try:
    GEOM_NO_CHECK = QgsFeatureRequest.InvalidGeometryCheck.GeometryNoCheck
except AttributeError:
    GEOM_NO_CHECK = QgsFeatureRequest.GeometryNoCheck

