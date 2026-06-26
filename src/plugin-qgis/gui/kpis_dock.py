# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import (QDockWidget, QVBoxLayout, QHBoxLayout, QWidget,
                                 QLabel, QFrame, QPushButton, QLineEdit, QFormLayout,
                                 QApplication)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject, QgsApplication
import unicodedata

from ..compat import LOG_INFO, LOG_CRITICAL

# Compatibilidade QGIS 3 (PyQt5) e QGIS 4 (PyQt6)
try:
    ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
    LEFT_DOCK = Qt.DockWidgetArea.LeftDockWidgetArea
    RIGHT_DOCK = Qt.DockWidgetArea.RightDockWidgetArea
    FRAME_STYLED_PANEL = QFrame.Shape.StyledPanel
    FRAME_RAISED = QFrame.Shadow.Raised
    WAIT_CURSOR = Qt.CursorShape.WaitCursor
except AttributeError:
    ALIGN_CENTER = Qt.AlignCenter
    LEFT_DOCK = Qt.LeftDockWidgetArea
    RIGHT_DOCK = Qt.RightDockWidgetArea
    FRAME_STYLED_PANEL = QFrame.StyledPanel
    FRAME_RAISED = QFrame.Raised
    WAIT_CURSOR = Qt.WaitCursor


class KpiCard(QFrame):
    """Componente visual para exibir uma métrica."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(FRAME_STYLED_PANEL)
        self.setFrameShadow(FRAME_RAISED)
        self.setStyleSheet("""
            QFrame { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; }
            QLabel { border: none; background-color: transparent; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #6c757d; font-size: 9pt; font-weight: bold;")
        self.lbl_title.setAlignment(ALIGN_CENTER)
        self.lbl_title.setWordWrap(True)
        self.lbl_value = QLabel("-")
        self.lbl_value.setStyleSheet("color: #212529; font-size: 17pt; font-weight: bold;")
        self.lbl_value.setAlignment(ALIGN_CENTER)
        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)

    def set_value(self, value):
        self.lbl_value.setText(str(value))


class KpisDockWidget(QDockWidget):
    """
    Painel único do plugin: orquestra aquisição → detecção → parecer (reusando os
    algoritmos do Processing via processing.run) e mostra os KPIs da análise.
    """
    def __init__(self, iface, parent=None):
        super().__init__("Pré-Val CAR", parent)
        self.iface = iface
        self.setObjectName("PreValCarKpisDock")
        self.setAllowedAreas(LEFT_DOCK | RIGHT_DOCK)
        self._car = None
        self._incra = None
        self._fila = None
        self._geom = None
        self._muni = None
        self.init_gui()

    # ------------------------------------------------------------------ GUI
    def init_gui(self):
        widget = QWidget()
        main = QVBoxLayout(widget)

        form = QFormLayout()
        self.uf_edit = QLineEdit("PR")
        self.muni_edit = QLineEdit("Itaguajé")
        form.addRow("UF:", self.uf_edit)
        form.addRow("Município:", self.muni_edit)
        main.addLayout(form)

        self.btn_baixar = QPushButton("1 · Baixar CAR + assentamentos do município")
        self.btn_detectar = QPushButton("2 · Detectar e priorizar")
        self.btn_parecer = QPushButton("3 · Gerar pareceres (p/ Atlas)")
        self.btn_baixar.clicked.connect(self.acao_baixar)
        self.btn_detectar.clicked.connect(self.acao_detectar)
        self.btn_parecer.clicked.connect(self.acao_parecer)
        for b in (self.btn_baixar, self.btn_detectar, self.btn_parecer):
            main.addWidget(b)

        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine if hasattr(QFrame, 'Shape') else QFrame.HLine)
        main.addWidget(linha)

        row1 = QHBoxLayout()
        self.card_imoveis = KpiCard("Total\nImóveis")
        self.card_conflitos = KpiCard("Com\nSobreposição")
        row1.addWidget(self.card_imoveis)
        row1.addWidget(self.card_conflitos)
        row2 = QHBoxLayout()
        self.card_assentamentos = KpiCard("Assentamentos\nEnvolvidos")
        self.card_area = KpiCard("Área em\nConflito")
        row2.addWidget(self.card_assentamentos)
        row2.addWidget(self.card_area)
        main.addLayout(row1)
        main.addLayout(row2)

        self.lbl_status = QLabel("Pronto. Informe UF/Município e comece pelo passo 1.")
        self.lbl_status.setWordWrap(True)
        self.lbl_status.setStyleSheet("color: #555; font-size: 9pt; margin-top: 6px;")
        main.addWidget(self.lbl_status)

        dica = QLabel("<i>A fila fica na tabela de atributos da camada 'Fila Priorizada' "
                      "(ordene por 'score'). Os conflitos vão para 'Geometrias de Conflito'.</i>")
        dica.setWordWrap(True)
        dica.setStyleSheet("color: #888; font-size: 8pt;")
        main.addWidget(dica)
        main.addStretch()

        self.setWidget(widget)
        self._atualizar_habilitacao()

    def disconnect_signals(self):
        # Mantido por compatibilidade com o unload() do plugin (nada conectado).
        pass

    # -------------------------------------------------------------- helpers
    def _atualizar_habilitacao(self):
        self.btn_detectar.setEnabled(self._car is not None)
        self.btn_parecer.setEnabled(self._fila is not None)

    def _status(self, msg, erro=False):
        self.lbl_status.setText(msg)
        QgsApplication.messageLog().logMessage(msg, "Pré-Val CAR",
                                               LOG_CRITICAL if erro else LOG_INFO)
        QApplication.processEvents()

    @staticmethod
    def _norm(s):
        return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode('ascii').strip().upper()

    # ---------------------------------------------------------------- ações
    def acao_baixar(self):
        from qgis import processing
        uf = self.uf_edit.text().strip()
        muni = self.muni_edit.text().strip()
        if not uf or not muni:
            self._status("Informe UF e Município.", True)
            return

        # Resolve a grafia oficial (IBGE) — aceita "querencia do norte", "MARINGA" etc.
        from ..core.municipios import resolver_municipio
        canonico, status = resolver_municipio(uf, muni)
        if status == 'nao_existe':
            self._status(f"Município '{muni}' não existe em {uf}. Verifique a grafia.", True)
            return
        if canonico and canonico != muni:
            muni = canonico
            self.muni_edit.setText(canonico)  # mostra a grafia corrigida
        self._muni = muni

        QApplication.setOverrideCursor(WAIT_CURSOR)
        try:
            self._status(f"Baixando imóveis do CAR de {muni}/{uf}…")
            r1 = processing.runAndLoadResults(
                "prevalcar:baixar_sicar",
                {'UF': uf, 'MUNICIPIO': muni, 'OUTPUT': 'TEMPORARY_OUTPUT'})
            self._car = QgsProject.instance().mapLayer(r1['OUTPUT'])
            if self._car is not None:
                self._car.setName(f"Imóveis CAR - {muni}")
                if self._car.featureCount() == 0:
                    self._status(f"Nenhum imóvel do CAR retornado para {muni}/{uf}. "
                                 f"Confira a grafia do município.", True)

            self._status(f"Baixando assentamentos do INCRA de {uf} e filtrando {muni}…")
            r2 = processing.runAndLoadResults(
                "prevalcar:baixar_assentamentos",
                {'UF': uf, 'OUTPUT': 'TEMPORARY_OUTPUT'})
            incra_estado = QgsProject.instance().mapLayer(r2['OUTPUT'])
            self._incra = self._filtrar_incra(incra_estado, muni)

            n_car = self._car.featureCount() if self._car else 0
            n_inc = self._incra.featureCount() if self._incra else 0
            self._status(f"Dados prontos: {n_car} imóveis e {n_inc} assentamentos. Siga para o passo 2.")
        except Exception as e:
            self._status(f"Erro ao baixar dados: {e}", True)
        finally:
            QApplication.restoreOverrideCursor()
            self._atualizar_habilitacao()

    def _filtrar_incra(self, incra_estado, muni):
        """Filtra os assentamentos do estado para o município (comparação sem acento/caixa)."""
        from qgis import processing
        if incra_estado is None:
            return None
        alvo = self._norm(muni)
        ids = [f.id() for f in incra_estado.getFeatures()
               if self._norm(f['municipio']) == alvo]
        if not ids:
            # Município válido, mas sem assentamentos: remove a camada estadual e segue só com CAR×CAR.
            QgsProject.instance().removeMapLayer(incra_estado.id())
            self._status(f"Nenhum assentamento do INCRA em {muni}.")
            return None
        incra_estado.selectByIds(ids)
        res = processing.runAndLoadResults(
            "native:saveselectedfeatures",
            {'INPUT': incra_estado, 'OUTPUT': 'TEMPORARY_OUTPUT'})
        filtrado = QgsProject.instance().mapLayer(res['OUTPUT'])
        if filtrado is not None:
            filtrado.setName(f"Assentamentos INCRA - {muni}")
        QgsProject.instance().removeMapLayer(incra_estado.id())  # remove a camada estadual
        return filtrado

    def acao_detectar(self):
        from qgis import processing
        if self._car is None:
            self._status("Baixe os dados primeiro (passo 1).", True)
            return
        QApplication.setOverrideCursor(WAIT_CURSOR)
        try:
            self._status("Detectando sobreposições e calculando a fila…")
            params = {'INPUT_CAR': self._car, 'TOLERANCIA': 0.01,
                      'OUTPUT_FILA': 'TEMPORARY_OUTPUT',
                      'OUTPUT_GEOMETRIAS': 'TEMPORARY_OUTPUT'}
            if self._incra is not None:
                params['INPUT_INCRA'] = self._incra
            res = processing.runAndLoadResults("prevalcar:detectar_sobreposicao", params)
            self._fila = QgsProject.instance().mapLayer(res['OUTPUT_FILA'])
            self._geom = QgsProject.instance().mapLayer(res['OUTPUT_GEOMETRIAS'])

            suf = f" - {self._muni}" if self._muni else ""
            if self._fila is not None:
                self._fila.setName(f"Fila Priorizada{suf}")
            if self._geom is not None:
                self._geom.setName(f"Geometrias de Conflito{suf}")

            # Estilo automático: conflitos em vermelho, fila graduada por risco.
            from ..estilos import estilo_conflitos, estilo_fila
            estilo_fila(self._fila)
            estilo_conflitos(self._geom)

            self.update_kpis()
            self._status("Detecção concluída. Veja os KPIs e a 'Fila Priorizada'.")
        except Exception as e:
            self._status(f"Erro na detecção: {e}", True)
        finally:
            QApplication.restoreOverrideCursor()
            self._atualizar_habilitacao()

    def acao_parecer(self):
        from qgis import processing
        if self._fila is None:
            self._status("Rode a detecção primeiro (passo 2).", True)
            return
        QApplication.setOverrideCursor(WAIT_CURSOR)
        try:
            self._status("Gerando o HTML dos pareceres…")
            processing.runAndLoadResults(
                "prevalcar:preparar_pareceres",
                {'INPUT_FILA': self._fila, 'OUTPUT': 'TEMPORARY_OUTPUT'})
            self._status("Pareceres prontos: use o campo 'parecer_html' no Atlas do Layout.")
        except Exception as e:
            self._status(f"Erro ao gerar pareceres: {e}", True)
        finally:
            QApplication.restoreOverrideCursor()

    # ----------------------------------------------------------------- KPIs
    def update_kpis(self):
        fila, geom = self._fila, self._geom
        if fila is None:
            for c in (self.card_imoveis, self.card_conflitos,
                      self.card_assentamentos, self.card_area):
                c.set_value("-")
            return

        total = fila.featureCount()
        idx_c = fila.fields().indexFromName('conflito')
        n_conf = 0
        if idx_c != -1:
            for f in fila.getFeatures():
                if f['conflito'] in (1, '1', True):
                    n_conf += 1
        self.card_imoveis.set_value(str(total))
        self.card_conflitos.set_value(str(n_conf))

        assent = set()
        area = 0.0
        if geom is not None:
            campos = geom.fields()
            it = campos.indexFromName('tipo')
            ic = campos.indexFromName('contra')
            ia = campos.indexFromName('sobrep_ha')
            for f in geom.getFeatures():
                if it != -1 and ic != -1 and f['tipo'] == 'CARxAssentamento':
                    assent.add(f['contra'])
                if ia != -1 and f['sobrep_ha'] is not None:
                    area += f['sobrep_ha']
        self.card_assentamentos.set_value(str(len(assent)))
        self.card_area.set_value(f"{area:.1f} ha")
