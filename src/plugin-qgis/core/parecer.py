# -*- coding: utf-8 -*-
import json

def formatar_memoria_html(json_str, cod_imovel, area_imovel_ha):
    """
    Transforma a memória de cálculo JSON (gerada no momento da detecção) em um trecho HTML formatado.
    Este HTML contém tabelas e formatação amigável para ser injetado diretamente em 
    um componente 'HTML Frame' do Print Layout/Atlas do QGIS.
    """
    if not json_str or json_str == '[]':
        return "<p>Nenhuma sobreposição detectada na base de referência (dentro da tolerância).</p>"
        
    try:
        sobreposicoes = json.loads(json_str)
    except Exception as e:
        return f"<p>Erro ao processar memória de cálculo: {e}</p>"
        
    html = []
    
    # Cabeçalho da memória de cálculo
    html.append(f"<h3 style='color: #2c3e50; border-bottom: 1px solid #ddd;'>Memória de Cálculo - Divergências de Geometria</h3>")
    html.append(f"<p><b>Imóvel Analisado:</b> {cod_imovel}<br>")
    html.append(f"<b>Área Total Declarada:</b> {area_imovel_ha:.2f} ha</p>")
    
    # Tabela de detalhamento
    html.append("<table style='width:100%; border-collapse: collapse; margin-top: 10px; font-family: Arial, sans-serif;'>")
    html.append("<tr style='background-color: #f2f2f2;'>")
    html.append("<th style='border: 1px solid #aaa; padding: 8px; text-align: left;'>Tipo do Conflito</th>")
    html.append("<th style='border: 1px solid #aaa; padding: 8px; text-align: left;'>Objeto Conflitante</th>")
    html.append("<th style='border: 1px solid #aaa; padding: 8px; text-align: right;'>Área (ha)</th>")
    html.append("<th style='border: 1px solid #aaa; padding: 8px; text-align: right;'>Comprometimento</th>")
    html.append("</tr>")
    
    total_area_sobreposta = 0.0
    tem_assentamento = False
    
    for s in sobreposicoes:
        area_conflito = s.get('sobrep_ha', 0)
        total_area_sobreposta += area_conflito
        pct = s.get('pct_imovel', 0)
        tipo = s.get('tipo', '')
        contra = s.get('contra', '')
        
        if tipo == 'CARxAssentamento':
            tem_assentamento = True
            
        # Cor de destaque se a % for grande
        color = "color: #e74c3c; font-weight: bold;" if pct > 10 else "color: #333;"
            
        html.append("<tr>")
        html.append(f"<td style='border: 1px solid #aaa; padding: 8px;'>{tipo}</td>")
        html.append(f"<td style='border: 1px solid #aaa; padding: 8px;'>{contra}</td>")
        html.append(f"<td style='border: 1px solid #aaa; padding: 8px; text-align: right;'>{area_conflito:.3f}</td>")
        html.append(f"<td style='border: 1px solid #aaa; padding: 8px; text-align: right; {color}'>{pct:.1f}%</td>")
        html.append("</tr>")
        
    html.append("</table>")
    
    # Seção de Enquadramento Legal e Recomendação baseada no Código Florestal / Normas
    html.append("<h3 style='color: #2c3e50; border-bottom: 1px solid #ddd; margin-top: 20px;'>Enquadramento e Recomendação Preliminar</h3>")
    html.append("<div style='background-color: #fdfaf6; border-left: 4px solid #e67e22; padding: 10px; margin-top: 10px;'>")
    
    if tem_assentamento:
        html.append("<p style='color: #c0392b;'><b>ALERTA GRAVE:</b> Constatada sobreposição com perímetro de Assentamento da Reforma Agrária (INCRA).</p>")
        html.append("<p><b>Ação Recomendada:</b><br>1. Bloqueio cautelar do processamento automático.<br>2. Notificar imediatamente o proprietário declarante e encaminhar o caso para a câmara de conciliação fundiária competente.</p>")
    elif total_area_sobreposta > 0:
        html.append("<p><b>Divergência de Divisas:</b> Sobreposição com polígonos de imóveis rurais de terceiros confirmada (CAR x CAR).</p>")
        html.append("<p><b>Ação Recomendada:</b><br>1. Reter a análise de conformidade.<br>2. Proceder com a etapa de <i>Retificação Dinamizada</i>, notificando os respectivos declarantes para adequação e acordo do traçado geométrico, conforme prevê a regulação do SICAR.</p>")
        
    html.append("</div>")
    html.append("<br><br><p style='font-size: 8pt; color: #7f8c8d; text-align: right;'><i>Parecer pré-gerado pelo Módulo Analítico 'Pré-Val CAR' — Sujeito à homologação técnica.</i></p>")
    
    return "".join(html)
