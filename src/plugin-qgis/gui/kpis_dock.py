# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QDockWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFrame
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject

# Compatibilidade QGIS 3 (PyQt5) e QGIS 4 (PyQt6)
try:
    ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
    LEFT_DOCK = Qt.DockWidgetArea.LeftDockWidgetArea
    RIGHT_DOCK = Qt.DockWidgetArea.RightDockWidgetArea
    FRAME_STYLED_PANEL = QFrame.Shape.StyledPanel
    FRAME_RAISED = QFrame.Shadow.Raised
except AttributeError:
    ALIGN_CENTER = Qt.AlignCenter
    LEFT_DOCK = Qt.LeftDockWidgetArea
    RIGHT_DOCK = Qt.RightDockWidgetArea
    FRAME_STYLED_PANEL = QFrame.StyledPanel
    FRAME_RAISED = QFrame.Raised

class KpiCard(QFrame):
    """
    Componente visual para exibir uma métrica no painel.
    """
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(FRAME_STYLED_PANEL)
        self.setFrameShadow(FRAME_RAISED)
        
        # Estilo "clean" para emular o painel web
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
            QLabel {
                border: none;
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #6c757d; font-size: 10pt; font-weight: bold;")
        self.lbl_title.setAlignment(ALIGN_CENTER)
        self.lbl_title.setWordWrap(True)
        
        self.lbl_value = QLabel("-")
        self.lbl_value.setStyleSheet("color: #212529; font-size: 18pt; font-weight: bold;")
        self.lbl_value.setAlignment(ALIGN_CENTER)
        
        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)
        
    def set_value(self, value):
        self.lbl_value.setText(str(value))

class KpisDockWidget(QDockWidget):
    """
    Única GUI customizada do plugin, contendo os 4 KPIs de monitoramento da análise.
    É reativa à adição de camadas no projeto.
    """
    def __init__(self, iface, parent=None):
        super().__init__("Painel de KPIs - Pré-Val CAR", parent)
        self.iface = iface
        self.setObjectName("PreValCarKpisDock")
        self.setAllowedAreas(LEFT_DOCK | RIGHT_DOCK)
        
        self.init_gui()
        self.connect_signals()

    def init_gui(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        
        header = QLabel("Visão Geral do Recorte")
        header.setStyleSheet("font-weight: bold; font-size: 11pt; margin-bottom: 5px;")
        main_layout.addWidget(header)
        
        grid_layout = QVBoxLayout()
        grid_layout.setSpacing(10)
        
        row1 = QHBoxLayout()
        row1.setSpacing(10)
        self.card_imoveis = KpiCard("Total\nImóveis")
        self.card_conflitos = KpiCard("Com\nSobreposição")
        row1.addWidget(self.card_imoveis)
        row1.addWidget(self.card_conflitos)
        
        row2 = QHBoxLayout()
        row2.setSpacing(10)
        self.card_assentamentos = KpiCard("Assentamentos\nEnvolvidos")
        self.card_area = KpiCard("Área em\nConflito")
        row2.addWidget(self.card_assentamentos)
        row2.addWidget(self.card_area)
        
        grid_layout.addLayout(row1)
        grid_layout.addLayout(row2)
        
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        
        # Dica de uso com recurso nativo
        dica = QLabel("<i>Dica: Ordene a tabela de atributos da camada 'Fila Priorizada' pela coluna 'score' para iniciar a triagem.</i>")
        dica.setWordWrap(True)
        dica.setStyleSheet("color: #666; font-size: 9pt;")
        main_layout.addWidget(dica)
        
        self.setWidget(widget)

    def connect_signals(self):
        # Mantém as métricas vivas caso a analista carregue novas análises
        QgsProject.instance().layersAdded.connect(self.update_kpis)
        QgsProject.instance().layersRemoved.connect(self.update_kpis)

    def update_kpis(self):
        layers = QgsProject.instance().mapLayers().values()
        
        layer_fila = None
        layer_sobrep = None
        
        # Tenta inferir as camadas da análise pelos nomes padrão do Processing
        for lyr in layers:
            name = lyr.name()
            if "Fila Priorizada" in name:
                layer_fila = lyr
            elif "Geometrias de Conflito" in name:
                layer_sobrep = lyr
                
        if not layer_fila:
            self.card_imoveis.set_value("-")
            self.card_conflitos.set_value("-")
            self.card_assentamentos.set_value("-")
            self.card_area.set_value("-")
            return
            
        # Calcula Imóveis e Conflitos
        total_imoveis = layer_fila.featureCount()
        idx_conflito = layer_fila.fields().indexFromName('conflito')
        total_com_conflito = 0
        
        if idx_conflito != -1:
            for feat in layer_fila.getFeatures():
                if feat['conflito'] == 1:
                    total_com_conflito += 1
        
        self.card_imoveis.set_value(str(total_imoveis))
        self.card_conflitos.set_value(str(total_com_conflito))
        
        # Calcula Assentamentos e Área de Conflito usando as geometrias reais
        if layer_sobrep:
            assentamentos = set()
            area_total = 0.0
            idx_tipo = layer_sobrep.fields().indexFromName('tipo')
            idx_contra = layer_sobrep.fields().indexFromName('contra')
            idx_area = layer_sobrep.fields().indexFromName('sobrep_ha')
            
            for f in layer_sobrep.getFeatures():
                if idx_tipo != -1 and idx_contra != -1 and f[idx_tipo] == 'CARxAssentamento':
                    assentamentos.add(f[idx_contra])
                    
                if idx_area != -1 and f[idx_area]:
                    area_total += f[idx_area]
                
            self.card_assentamentos.set_value(str(len(assentamentos)))
            self.card_area.set_value(f"{area_total:.1f} ha")
