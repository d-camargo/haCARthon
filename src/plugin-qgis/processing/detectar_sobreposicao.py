# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsField,
                       QgsFields,
                       QgsGeometry)
import json

from ..core.detector import DetectorQGIS
from ..core.priorizacao import calcular_score_risco
from ..compat import (FIELD_STRING, FIELD_DOUBLE, FIELD_INT,
                      GEOM_POLYGON, WKB_MULTIPOLYGON, FAST_INSERT,
                      PARAM_NUMBER_DOUBLE)

class DetectarSobreposicaoAlgorithm(QgsProcessingAlgorithm):
    INPUT_CAR = 'INPUT_CAR'
    INPUT_INCRA = 'INPUT_INCRA'
    TOLERANCIA = 'TOLERANCIA'
    OUTPUT_FILA = 'OUTPUT_FILA'
    OUTPUT_GEOMETRIAS = 'OUTPUT_GEOMETRIAS'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DetectarSobreposicaoAlgorithm()

    def name(self):
        return 'detectar_sobreposicao'

    def displayName(self):
        return self.tr('Detecção e Priorização de Fila')

    def group(self):
        return self.tr('2. Análise e Fila')

    def groupId(self):
        return 'analise'

    def shortHelpString(self):
        return self.tr("Detecta sobreposições CAR x CAR e CAR x Assentamento, gerando a camada de conflitos (geometrias da interseção) e a Fila Priorizada (atributos enriquecidos).")

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT_CAR, self.tr('Camada de Imóveis (CAR)'), [GEOM_POLYGON]))
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT_INCRA, self.tr('Camada de Assentamentos (Opcional)'), [GEOM_POLYGON], optional=True))

        self.addParameter(QgsProcessingParameterNumber(self.TOLERANCIA, self.tr('Tolerância de área (hectares)'), type=PARAM_NUMBER_DOUBLE, defaultValue=0.01))

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT_FILA, self.tr('Fila Priorizada (CAR atualizado)')))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT_GEOMETRIAS, self.tr('Geometrias de Conflito (Interseções)')))

    def processAlgorithm(self, parameters, context, feedback):
        layer_car = self.parameterAsSource(parameters, self.INPUT_CAR, context)
        layer_incra = self.parameterAsSource(parameters, self.INPUT_INCRA, context)
        tolerancia = self.parameterAsDouble(parameters, self.TOLERANCIA, context)

        # 1. Configurar saídas
        # Geometrias (interseções) — saída MultiPolygon para acomodar interseções multipart
        campos_conflito = QgsFields()
        campos_conflito.append(QgsField('tipo', FIELD_STRING))
        campos_conflito.append(QgsField('imovel', FIELD_STRING))
        campos_conflito.append(QgsField('contra', FIELD_STRING))
        campos_conflito.append(QgsField('sobrep_ha', FIELD_DOUBLE))
        campos_conflito.append(QgsField('pct_imovel', FIELD_DOUBLE))
        (sink_geom, dest_geom_id) = self.parameterAsSink(
            parameters, self.OUTPUT_GEOMETRIAS, context,
            campos_conflito, WKB_MULTIPOLYGON, layer_car.sourceCrs()
        )

        # Fila (CAR modificado)
        campos_fila = layer_car.fields()
        if campos_fila.indexFromName('conflito') == -1:
            campos_fila.append(QgsField('conflito', FIELD_INT))
            campos_fila.append(QgsField('score', FIELD_DOUBLE))
            campos_fila.append(QgsField('json_sobreposicoes', FIELD_STRING))  # Memória de cálculo resumida

        (sink_fila, dest_fila_id) = self.parameterAsSink(
            parameters, self.OUTPUT_FILA, context,
            campos_fila, layer_car.wkbType(), layer_car.sourceCrs()
        )

        if sink_geom is None or sink_fila is None:
            return {}

        # 2. Executar Detector
        detector = DetectorQGIS(layer_car, layer_incra)

        feedback.pushInfo("Detectando sobreposições CAR x CAR...")
        conflitos_cxc = detector.detectar_car_x_car(tolerancia_ha=tolerancia, feedback=feedback)

        conflitos_cxa = []
        if layer_incra:
            feedback.pushInfo("Detectando sobreposições CAR x Assentamento...")
            conflitos_cxa = detector.detectar_car_x_assentamento(tolerancia_ha=tolerancia, feedback=feedback)

        # 3. Gerar Saída de Geometrias e agrupar por imóvel
        agrupado_por_imovel = {}

        def processar_conflito(c, salvar_geom=True):
            cod = c['imovel']
            agrupado_por_imovel.setdefault(cod, []).append(c)

            if salvar_geom:
                geom = c['geom']
                # A saída é MultiPolygon: promove interseções simples para multipart.
                if not geom.isMultipart():
                    geom = QgsGeometry(geom)
                    geom.convertToMultiType()
                f = QgsFeature()
                f.setGeometry(geom)
                f.setAttributes([c['tipo'], c['imovel'], c['contra'], c['sobrep_ha'], c['pct_imovel']])
                sink_geom.addFeature(f, FAST_INSERT)

        for c in conflitos_cxc:
            # CARxCAR vem em pares simétricos (a×b e b×a); salva a geometria só uma vez.
            salvar_geom = (c['imovel'] < c['contra'])
            processar_conflito(c, salvar_geom)

        for c in conflitos_cxa:
            processar_conflito(c, salvar_geom=True)

        # 4. Processar Fila e Priorização
        feedback.pushInfo("Calculando fila e scores...")

        total_car = layer_car.featureCount()
        step = 100.0 / total_car if total_car > 0 else 1

        idx_conflito = campos_fila.indexFromName('conflito')
        idx_score = campos_fila.indexFromName('score')
        idx_json = campos_fila.indexFromName('json_sobreposicoes')

        for i, feat in enumerate(layer_car.getFeatures()):
            if feedback.isCanceled():
                break

            cod_imovel = feat['cod_imovel']
            conflitos_deste = agrupado_por_imovel.get(cod_imovel, [])

            area_ha = detector.calcular_area_ha(detector._fix_geom(feat.geometry()))
            score = calcular_score_risco(conflitos_deste, area_ha)

            # Memória JSON para o RAT (Atlas)
            memoria = [{'tipo': c['tipo'], 'contra': c['contra'], 'sobrep_ha': c['sobrep_ha'], 'pct_imovel': c['pct_imovel']} for c in conflitos_deste]

            attr = list(feat.attributes())
            # Garante que a lista de atributos tenha o tamanho dos campos de saída.
            while len(attr) < len(campos_fila):
                attr.append(None)
            attr[idx_conflito] = 1 if score > 0 else 0
            attr[idx_score] = score
            attr[idx_json] = json.dumps(memoria)

            nova_feat = QgsFeature(campos_fila)
            nova_feat.setGeometry(feat.geometry())
            nova_feat.setAttributes(attr)
            sink_fila.addFeature(nova_feat, FAST_INSERT)

            feedback.setProgress(int(i * step))

        return {self.OUTPUT_FILA: dest_fila_id, self.OUTPUT_GEOMETRIAS: dest_geom_id}
