# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

class PreValCarProvider(QgsProcessingProvider):
    def __init__(self):
        super().__init__()

    def loadAlgorithms(self):
        """Load all algorithms belonging to this provider."""
        from .processing.baixar_sicar import BaixarSicarAlgorithm
        from .processing.baixar_assentamentos_incra import BaixarAssentamentosAlgorithm
        from .processing.detectar_sobreposicao import DetectarSobreposicaoAlgorithm
        from .processing.gerar_parecer import GerarParecerAlgorithm
        
        self.addAlgorithm(BaixarSicarAlgorithm())
        self.addAlgorithm(BaixarAssentamentosAlgorithm())
        self.addAlgorithm(DetectarSobreposicaoAlgorithm())
        self.addAlgorithm(GerarParecerAlgorithm())

    def id(self):
        return 'prevalcar'

    def name(self):
        return 'Pré-Val CAR'

    def icon(self):
        import os
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        return QIcon(icon_path)
