# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsField)

from ..core.parecer import formatar_memoria_html
from ..compat import FIELD_STRING, FAST_INSERT

class GerarParecerAlgorithm(QgsProcessingAlgorithm):
    INPUT_FILA = 'INPUT_FILA'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GerarParecerAlgorithm()

    def name(self):
        return 'preparar_pareceres'

    def displayName(self):
        return self.tr('Preparar Contexto de Pareceres (HTML)')

    def group(self):
        return self.tr('3. Relatórios')

    def groupId(self):
        return 'relatorios'

    def shortHelpString(self):
        return self.tr("Lê a memória de cálculo em JSON da Fila Priorizada e gera um campo HTML elegante. Este campo está pronto para ser injetado nativamente no Atlas do QGIS para gerar PDFs em lote.")

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT_FILA, self.tr('Camada da Fila Priorizada (com JSON de conflitos)')))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Fila com Pareceres (Pronta para o Atlas)')))

    def processAlgorithm(self, parameters, context, feedback):
        layer_fila = self.parameterAsSource(parameters, self.INPUT_FILA, context)

        campos = layer_fila.fields()
        
        # Cria o novo campo de HTML que será lido pelo Print Layout
        idx_html = campos.indexFromName('parecer_html')
        if idx_html == -1:
            campos.append(QgsField('parecer_html', FIELD_STRING))
            
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            campos, layer_fila.wkbType(), layer_fila.sourceCrs()
        )

        if sink is None:
            return {}

        idx_json = layer_fila.fields().indexFromName('json_sobreposicoes')
        idx_area = layer_fila.fields().indexFromName('area')
        idx_cod = layer_fila.fields().indexFromName('cod_imovel')

        if idx_json == -1 or idx_cod == -1:
            feedback.reportError("A camada de entrada não parece ser uma Fila Priorizada válida (faltam as colunas json_sobreposicoes ou cod_imovel).")
            return {}

        total = layer_fila.featureCount()
        step = 100.0 / total if total > 0 else 1
        
        for i, feat in enumerate(layer_fila.getFeatures()):
            if feedback.isCanceled():
                break
                
            json_str = feat[idx_json]
            cod_imovel = feat[idx_cod]
            area_ha = feat[idx_area] if idx_area != -1 else 0.0
            
            # Chama a core logic para gerar a string HTML do parecer
            html = formatar_memoria_html(json_str, cod_imovel, area_ha)
            
            attr = list(feat.attributes())
            if idx_html == -1:
                attr.append(html)
            else:
                attr[idx_html] = html
                
            nova_feat = QgsFeature(campos)
            nova_feat.setGeometry(feat.geometry())
            nova_feat.setAttributes(attr)
            sink.addFeature(nova_feat, FAST_INSERT)
            
            feedback.setProgress(int(i * step))

        return {self.OUTPUT: dest_id}
