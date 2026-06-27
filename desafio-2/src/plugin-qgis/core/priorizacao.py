# -*- coding: utf-8 -*-

def calcular_score_risco(conflitos_imovel, area_imovel_ha, weights=None):
    """
    Calcula o score de priorização para compor a fila de análise.
    
    A fórmula considera:
    - Área total sobreposta do imóvel (ha)
    - Porcentagem da área do imóvel comprometida
    - Agravantes para tipos específicos (ex: sobrepor Assentamento INCRA tem peso enorme)
    """
    if weights is None:
        weights = {
            'w_sobrep_ha': 1.0, 
            'w_pct_imovel': 0.5, 
            'w_assentamento': 50.0
        }
        
    total_sobrep_ha = 0.0
    max_pct = 0.0
    tem_assentamento = False
    
    for c in conflitos_imovel:
        total_sobrep_ha += c['sobrep_ha']
        if c['pct_imovel'] > max_pct:
            max_pct = c['pct_imovel']
        if c['tipo'] == 'CARxAssentamento':
            tem_assentamento = True
            
    # Trava a área sobreposta total na área máxima do imóvel para não inflacionar
    # em caso de tripla sobreposição
    total_sobrep_ha = min(total_sobrep_ha, area_imovel_ha)
    pct_imovel_agregada = (total_sobrep_ha / area_imovel_ha * 100.0) if area_imovel_ha > 0 else 0.0
    
    score = (total_sobrep_ha * weights['w_sobrep_ha']) + \
            (pct_imovel_agregada * weights['w_pct_imovel'])
            
    # Agravante de tipologia
    if tem_assentamento:
        score += weights['w_assentamento']
        
    return round(score, 2)
