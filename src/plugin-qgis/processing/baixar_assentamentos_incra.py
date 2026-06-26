# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFeatureSink,
                       QgsField,
                       QgsGeometry)
from ..core.wfs import load_incra_layer
from ..compat import FIELD_STRING, FAST_INSERT

class BaixarAssentamentosAlgorithm(QgsProcessingAlgorithm):
    UF = 'UF'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return BaixarAssentamentosAlgorithm()

    def name(self):
        return 'baixar_assentamentos'

    def displayName(self):
        return self.tr('Baixar assentamentos (INCRA)')

    def group(self):
        return self.tr('1. Aquisição de Dados')

    def groupId(self):
        return 'aquisicao'

    def shortHelpString(self):
        return self.tr("Baixa os assentamentos do INCRA via WFS por UF, garantindo que o eixo X/Y (lon/lat) esteja correto e padronizando as colunas 'nome' e 'fonte'.")

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString(self.UF, self.tr('UF (Ex: PR)'), defaultValue='PR'))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Assentamentos INCRA')))

    def processAlgorithm(self, parameters, context, feedback):
        uf = self.parameterAsString(parameters, self.UF, context)

        wfs_layer = load_incra_layer(uf)
        
        if not wfs_layer.isValid():
            err_msg = getattr(wfs_layer, 'error_msg', 'Erro desconhecido')
            feedback.reportError(f"Falha ao conectar no WFS do INCRA para a UF {uf}. Detalhes: {err_msg}")
            return {}

        total = wfs_layer.featureCount()
        feedback.pushInfo(f"Encontrados {total} assentamentos. Baixando e padronizando...")

        fields = wfs_layer.fields()
        # Garante a existência do campo 'nome'
        nome_idx = fields.indexFromName('nome')
        if nome_idx == -1:
            fields.append(QgsField('nome', FIELD_STRING))
            
        fonte_idx = fields.indexFromName('fonte')
        if fonte_idx == -1:
            fields.append(QgsField('fonte', FIELD_STRING))

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            fields, wfs_layer.wkbType(), wfs_layer.sourceCrs()
        )

        if sink is None:
            return {}

        step = 100.0 / total if total > 0 else 1
        
        for current, feature in enumerate(wfs_layer.getFeatures()):
            if feedback.isCanceled():
                break
                
            # Popula o campo 'nome' através do 'nome_projeto' caso precise
            if feature.fields().indexFromName('nome_projeto') != -1:
                # setAttribute em novo campo necessita que usemos um novo feature ou acessemos os atributos extendidos
                pass
            
            # Feature vinda do getFeatures pode não ter os novos campos (pois foram adicionados no sink).
            # Para popular corretamente, setamos no objeto Feature.
            attr = feature.attributes()
            
            # Se a feature original não tinha 'nome', extendemos a lista de atributos
            if nome_idx == -1:
                nome_val = feature['nome_projeto'] if feature.fields().indexFromName('nome_projeto') != -1 else ''
                attr.append(nome_val)
            else:
                attr[nome_idx] = feature['nome_projeto'] if feature.fields().indexFromName('nome_projeto') != -1 else ''
                
            if fonte_idx == -1:
                attr.append('INCRA i3geo')
            else:
                attr[fonte_idx] = 'INCRA i3geo'
                
            feature.setAttributes(attr)

            # O GDAL lê o WFS 1.0.0 do INCRA como lat,lon — corrige o eixo (X <-> Y).
            geom = QgsGeometry(feature.geometry())
            abs_geom = geom.get()
            if abs_geom is not None:
                abs_geom.swapXy()
                feature.setGeometry(geom)

            sink.addFeature(feature, FAST_INSERT)
            feedback.setProgress(int(current * step))

        return {self.OUTPUT: dest_id}
