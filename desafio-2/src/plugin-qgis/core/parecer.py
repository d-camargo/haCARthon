# -*- coding: utf-8 -*-
import json

# Como o rótulo HTML (Qt rich text) não pagina, limitamos as linhas da tabela
# e resumimos o excedente para o parecer caber na folha.
_LIMITE_LINHAS = 12


def formatar_memoria_html(json_str, cod_imovel, area_imovel_ha):
    """
    Transforma a memória de cálculo (JSON gerado na detecção) num HTML compacto,
    adequado ao rótulo HTML do Print Layout (Qt rich text, sem WebKit).
    """
    base_style = "font-family:Arial,sans-serif;font-size:9pt;color:#333;"
    if not json_str or json_str == '[]':
        return (f"<div style='{base_style}'>Nenhuma sobreposição detectada na base de "
                f"referência (dentro da tolerância).</div>")
    try:
        sobreposicoes = json.loads(json_str)
    except Exception as e:
        return f"<div style='{base_style}'>Erro ao processar a memória de cálculo: {e}</div>"

    sobreposicoes.sort(key=lambda s: (s.get('sobrep_ha', 0) or 0), reverse=True)
    total_area = sum((s.get('sobrep_ha', 0) or 0) for s in sobreposicoes)
    tem_assentamento = any(s.get('tipo') == 'CARxAssentamento' for s in sobreposicoes)
    visiveis = sobreposicoes[:_LIMITE_LINHAS]
    extras = sobreposicoes[_LIMITE_LINHAS:]

    td = "border:1px solid #bbb;padding:3px;"
    h = [f"<div style='{base_style}'>"]
    h.append(f"<p style='margin:2px 0;'>Imóvel <b>{cod_imovel}</b> · área declarada "
             f"{area_imovel_ha:.2f} ha · {len(sobreposicoes)} sobreposição(ões) · "
             f"total {total_area:.2f} ha</p>")

    h.append("<table style='width:100%;border-collapse:collapse;font-size:8.5pt;'>")
    h.append(f"<tr style='background:#f0f0f0;'>"
             f"<td style='{td}'><b>Tipo</b></td>"
             f"<td style='{td}'><b>Conflitante</b></td>"
             f"<td style='{td}text-align:right;'><b>Área (ha)</b></td>"
             f"<td style='{td}text-align:right;'><b>% imóvel</b></td></tr>")
    for s in visiveis:
        pct = s.get('pct_imovel', 0) or 0
        cor = "color:#c0392b;font-weight:bold;" if pct > 10 else ""
        h.append("<tr>"
                 f"<td style='{td}'>{s.get('tipo', '')}</td>"
                 f"<td style='{td}'>{s.get('contra', '')}</td>"
                 f"<td style='{td}text-align:right;'>{(s.get('sobrep_ha', 0) or 0):.3f}</td>"
                 f"<td style='{td}text-align:right;{cor}'>{pct:.1f}%</td></tr>")
    if extras:
        area_extra = sum((e.get('sobrep_ha', 0) or 0) for e in extras)
        h.append(f"<tr><td colspan='4' style='{td}font-style:italic;color:#666;'>"
                 f"… e mais {len(extras)} sobreposição(ões), somando {area_extra:.2f} ha.</td></tr>")
    h.append("</table>")

    h.append("<p style='margin-top:6px;'><b style='color:#2c3e50;'>Enquadramento e recomendação preliminar</b></p>")
    h.append("<div style='background:#fdfaf6;border:1px solid #e0c0a0;padding:6px;'>")
    if tem_assentamento:
        h.append("<p style='color:#c0392b;margin:2px 0;'><b>ALERTA:</b> sobreposição com perímetro "
                 "de Assentamento da Reforma Agrária (INCRA).</p>")
        h.append("<p style='margin:2px 0;'>Recomenda-se bloqueio cautelar da análise automática, "
                 "notificação ao declarante e encaminhamento à câmara de conciliação fundiária.</p>")
    else:
        h.append("<p style='margin:2px 0;'><b>Divergência de divisas (CAR × CAR):</b> sobreposição "
                 "com imóveis rurais de terceiros.</p>")
        h.append("<p style='margin:2px 0;'>Recomenda-se reter a análise de conformidade e proceder à "
                 "Retificação Dinamizada, notificando os declarantes para ajuste do traçado, conforme "
                 "a regulação do SICAR.</p>")
    h.append("</div>")
    h.append("<p style='font-size:7.5pt;color:#888;text-align:right;margin-top:4px;'>"
             "<i>Parecer pré-gerado pelo módulo Pré-Val CAR — sujeito a homologação técnica.</i></p>")
    h.append("</div>")
    return "".join(h)
