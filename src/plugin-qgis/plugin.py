# -*- coding: utf-8 -*-
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import sip

from .provider import PreValCarProvider
from .gui.kpis_dock import KpisDockWidget

# Compatibilidade QGIS 3 (PyQt5) e QGIS 4 (PyQt6)
try:
    RIGHT_DOCK = Qt.DockWidgetArea.RightDockWidgetArea
except AttributeError:
    RIGHT_DOCK = Qt.RightDockWidgetArea

class PreValCarPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = PreValCarProvider()
        self.dockwidget = None

    def initProcessing(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()
        
        # Iniciar DockWidget de KPIs
        self.dockwidget = KpisDockWidget(self.iface)
        self.iface.addDockWidget(RIGHT_DOCK, self.dockwidget)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)

        if self.dockwidget is not None:
            self.dockwidget.disconnect_signals()
            self.iface.removeDockWidget(self.dockwidget)
            # Destruição síncrona evita o aviso de "widget duplicado" no reload
            # (o deleteLater() é assíncrono e o initGui recria antes de rodar).
            try:
                sip.delete(self.dockwidget)
            except Exception:
                self.dockwidget.deleteLater()
            self.dockwidget = None
