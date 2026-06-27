# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFeatureSink)
from ..core.wfs import load_sicar_layer
from ..compat import FAST_INSERT

class BaixarSicarAlgorithm(QgsProcessingAlgorithm):
    UF = 'UF'
    MUNICIPIO = 'MUNICIPIO'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return BaixarSicarAlgorithm()

    def name(self):
        return 'baixar_sicar'

    def displayName(self):
        return self.tr('Baixar imóveis CAR (SICAR)')

    def group(self):
        return self.tr('1. Aquisição de Dados')

    def groupId(self):
        return 'aquisicao'

    def shortHelpString(self):
        return self.tr("Baixa os imóveis do SICAR via WFS filtrados por Município e exporta como uma nova camada.")

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString(self.UF, self.tr('UF (Ex: PR)'), defaultValue='PR'))
        self.addParameter(QgsProcessingParameterString(self.MUNICIPIO, self.tr('Município (Ex: Itaguajé)'), defaultValue='Itaguajé'))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Imóveis CAR')))

    def processAlgorithm(self, parameters, context, feedback):
        uf = self.parameterAsString(parameters, self.UF, context)
        municipio = self.parameterAsString(parameters, self.MUNICIPIO, context)

        wfs_layer = load_sicar_layer(uf, municipio)
        
        if not wfs_layer.isValid():
            err_msg = getattr(wfs_layer, 'error_msg', 'Erro desconhecido')
            feedback.reportError(f"Falha ao conectar no WFS do SICAR para {uf} - {municipio}. Detalhes: {err_msg}")
            return {}

        total = wfs_layer.featureCount()
        feedback.pushInfo(f"Encontrados {total} imóveis. Baixando feições (isso pode demorar dependendo da internet)...")

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            wfs_layer.fields(), wfs_layer.wkbType(), wfs_layer.sourceCrs()
        )

        if sink is None:
            return {}

        step = 100.0 / total if total > 0 else 1
        
        for current, feature in enumerate(wfs_layer.getFeatures()):
            if feedback.isCanceled():
                break
            sink.addFeature(feature, FAST_INSERT)
            feedback.setProgress(int(current * step))

        return {self.OUTPUT: dest_id}
