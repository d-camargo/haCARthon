# -*- coding: utf-8 -*-
from qgis.core import QgsSpatialIndex, QgsDistanceArea, QgsProject
from typing import List, Dict, Any

class DetectorQGIS:
    """
    Detector de sobreposições em Python puro para o QGIS.
    Usa QgsSpatialIndex para performance e QgsDistanceArea (SIRGAS 2000) 
    para cálculo de área geodésica em hectares.
    """
    def __init__(self, layer_car, layer_assentamentos=None, crs=None):
        self.layer_car = layer_car
        self.layer_assentamentos = layer_assentamentos
        self.crs = crs or layer_car.sourceCrs()
        
        # Configurar cálculo de área geodésica em hectares (SIRGAS 2000)
        self.da = QgsDistanceArea()
        # QgsProcessingFeatureSource não expõe transformContext(); usa o do projeto.
        self.da.setSourceCrs(self.crs, QgsProject.instance().transformContext())
        # Elipsoide do SIRGAS 2000 é o GRS80. ('EPSG:4674' é um CRS, não um
        # elipsoide — passá-lo aqui faz o measureArea cair para área planar em graus².)
        self.da.setEllipsoid('GRS80')
        
        self.index_car = QgsSpatialIndex(self.layer_car.getFeatures())
        self.index_assentamento = None
        if self.layer_assentamentos:
            self.index_assentamento = QgsSpatialIndex(self.layer_assentamentos.getFeatures())
            
    def calcular_area_ha(self, geom):
        if geom.isEmpty():
            return 0.0
        # QgsDistanceArea measureArea retorna metros quadrados, dividir por 10000 para ha
        return self.da.measureArea(geom) / 10000.0

    def _fix_geom(self, geom):
        if not geom.isGeosValid():
            return geom.makeValid()
        return geom

    def detectar_car_x_car(self, tolerancia_ha=0.01, feedback=None):
        conflitos = []
        features_car = {f.id(): f for f in self.layer_car.getFeatures()}
        
        total = len(features_car)
        step = 100.0 / total if total > 0 else 1
        
        for i, (fid_a, feat_a) in enumerate(features_car.items()):
            if feedback and feedback.isCanceled():
                break
                
            geom_a = self._fix_geom(feat_a.geometry())
            if geom_a.isEmpty():
                continue
                
            # Buscar candidatos no índice espacial (Bounding Box)
            candidatos = self.index_car.intersects(geom_a.boundingBox())
            
            for fid_b in candidatos:
                if fid_a >= fid_b:  # Evita duplicidade (a < b) e comparar consigo mesmo
                    continue
                    
                feat_b = features_car[fid_b]
                geom_b = self._fix_geom(feat_b.geometry())
                
                if geom_a.intersects(geom_b):
                    intersecao = geom_a.intersection(geom_b)
                    sobrep_ha = self.calcular_area_ha(intersecao)
                    
                    if sobrep_ha > tolerancia_ha:
                        area_a_ha = self.calcular_area_ha(geom_a)
                        area_b_ha = self.calcular_area_ha(geom_b)
                        menor_ha = min(area_a_ha, area_b_ha)
                        pct_do_menor = (sobrep_ha / menor_ha * 100.0) if menor_ha > 0 else 0.0
                        
                        conflitos.append({
                            'tipo': 'CARxCAR',
                            'imovel': feat_a['cod_imovel'],
                            'contra': feat_b['cod_imovel'],
                            'sobrep_ha': sobrep_ha,
                            'pct_imovel': (sobrep_ha / area_a_ha * 100.0) if area_a_ha > 0 else 0.0,
                            'pct_do_menor': pct_do_menor,
                            'geom': intersecao
                        })
                        
                        # Adiciona simetria (b x a) para facilitar a busca por imóvel
                        conflitos.append({
                            'tipo': 'CARxCAR',
                            'imovel': feat_b['cod_imovel'],
                            'contra': feat_a['cod_imovel'],
                            'sobrep_ha': sobrep_ha,
                            'pct_imovel': (sobrep_ha / area_b_ha * 100.0) if area_b_ha > 0 else 0.0,
                            'pct_do_menor': pct_do_menor,
                            'geom': intersecao
                        })
            
            if feedback:
                feedback.setProgress(int(i * step))
                
        return conflitos

    def detectar_car_x_assentamento(self, tolerancia_ha=0.01, feedback=None):
        if not self.layer_assentamentos:
            return []
            
        conflitos = []
        features_ass = {f.id(): f for f in self.layer_assentamentos.getFeatures()}
        features_car = {f.id(): f for f in self.layer_car.getFeatures()}
        
        total = len(features_car)
        step = 100.0 / total if total > 0 else 1
        
        for i, (fid_car, feat_car) in enumerate(features_car.items()):
            if feedback and feedback.isCanceled():
                break
                
            geom_car = self._fix_geom(feat_car.geometry())
            if geom_car.isEmpty():
                continue
                
            candidatos = self.index_assentamento.intersects(geom_car.boundingBox())
            
            for fid_ass in candidatos:
                feat_ass = features_ass[fid_ass]
                geom_ass = self._fix_geom(feat_ass.geometry())
                
                if geom_car.intersects(geom_ass):
                    intersecao = geom_car.intersection(geom_ass)
                    sobrep_ha = self.calcular_area_ha(intersecao)
                    
                    if sobrep_ha > tolerancia_ha:
                        area_car_ha = self.calcular_area_ha(geom_car)
                        
                        nome_ass = feat_ass['nome'] if feat_ass.fields().indexFromName('nome') != -1 else str(fid_ass)
                        
                        conflitos.append({
                            'tipo': 'CARxAssentamento',
                            'imovel': feat_car['cod_imovel'],
                            'contra': nome_ass,
                            'sobrep_ha': sobrep_ha,
                            'pct_imovel': (sobrep_ha / area_car_ha * 100.0) if area_car_ha > 0 else 0.0,
                            'pct_do_menor': None,
                            'geom': intersecao
                        })
            if feedback:
                feedback.setProgress(int(i * step))
                
        return conflitos
