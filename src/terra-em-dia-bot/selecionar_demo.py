"""Módulo para seleção determinística de imóveis de demonstração (Querência do Norte/PR).

Varre a base local de Querência do Norte em busca de imóveis com APP e RL
declaradas, selecionando 3 perfis contrastantes (maior déficit de RL, menor déficit
de RL, e maior mata ciliar) e salvando-os em arquivo gitignored.
"""
import sys
import json
from pathlib import Path
import cadastro
import analise

def main():
    # Parse --forcar
    forcar = "--forcar" in sys.argv or "-f" in sys.argv
    
    local_txt = Path("data/imoveis_teste.local.txt")
    candidatos_txt = Path("data/candidatos_demo.local.txt")
    
    if local_txt.exists() and not forcar:
        print("data/imoveis_teste.local.txt já existe. Use --forcar para sobrescrever.")
        return

    geojson_path = Path("data/sicar/imoveis_pr_querencia_do_norte.geojson")
    if not geojson_path.exists():
        print(f"Erro: arquivo {geojson_path} não encontrado.")
        sys.exit(1)
        
    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    features = data.get("features", [])
    candidatos = []
    
    print(f"Escaneando {len(features)} imóveis locais em Querência do Norte...")
    for feat in features:
        attrs = feat.get("properties", {})
        cod = attrs.get("cod_imovel")
        if not cod:
            continue
            
        perimetro, local_attrs = cadastro._ler(geojson_path, cod)
        if not perimetro:
            continue
            
        imovel = {
            "cod": cod,
            "perimetro": perimetro,
            "attrs": local_attrs or attrs,
            "app": cadastro._camadas(cadastro.APP_DIR, cod),
            "rl": cadastro._camadas(cadastro.RL_DIR, cod),
            "fonte": "local"
        }
        
        an = analise.analisar(imovel)
        if an.get("tem_app") and an.get("tem_rl"):
            candidatos.append((cod, an))
            
    if len(candidatos) < 3:
        print(f"Erro: Apenas {len(candidatos)} candidatos com APP e RL encontrados (necessário pelo menos 3).")
        sys.exit(1)
        
    print(f"Encontrados {len(candidatos)} candidatos com APP e RL declarados.")
    
    # Grava a tabela completa em data/candidatos_demo.local.txt (gitignored)
    candidatos_txt.parent.mkdir(parents=True, exist_ok=True)
    with open(candidatos_txt, "w", encoding="utf-8") as f:
        f.write("Tabela de Candidatos de Demonstração (Querência do Norte/PR)\n")
        f.write("="*80 + "\n")
        f.write(f"{'Índice':<6} | {'cod_imovel':<44} | {'Área (ha)':<10} | {'RL Prop (ha)':<12} | {'RL Exig (ha)':<12} | {'RL Def (ha)':<12} | {'APP (ha)':<8}\n")
        f.write("-"*110 + "\n")
        for i, (cod, an) in enumerate(candidatos):
            def_str = f"{an['rl_deficit_ha']:.1f}" if an.get("rl_deficit_ha") is not None else "None"
            f.write(f"{i:<6} | {cod:<44} | {an['area_ha']:<10.1f} | {an['rl_proposta_ha']:<12.1f} | {an['rl_exigida_ha']:<12.1f} | {def_str:<12} | {an['app_mata_ciliar_ha']:<8.1f}\n")

    # Seleciona 3 contrastantes de forma determinística
    # 1. Maior déficit de RL
    candidatos_sort_deficit = sorted(candidatos, key=lambda x: x[1].get("rl_deficit_ha") or 0.0, reverse=True)
    cod_max_deficit, an_max_deficit = candidatos_sort_deficit[0]
    
    # 2. Menor déficit de RL (idealmente > 0, mas o menor possível)
    deficits_positivos = [c for c in candidatos if (c[1].get("rl_deficit_ha") or 0.0) > 0.0]
    if deficits_positivos:
        candidatos_sort_min_deficit = sorted(deficits_positivos, key=lambda x: x[1].get("rl_deficit_ha"))
    else:
        candidatos_sort_min_deficit = sorted(candidatos, key=lambda x: x[1].get("rl_deficit_ha") or 0.0)
    
    idx = 0
    while idx < len(candidatos_sort_min_deficit) and candidatos_sort_min_deficit[idx][0] == cod_max_deficit:
        idx += 1
    if idx < len(candidatos_sort_min_deficit):
        cod_min_deficit, an_min_deficit = candidatos_sort_min_deficit[idx]
    else:
        cod_min_deficit, an_min_deficit = candidatos_sort_deficit[-1]

    # 3. Maior mata ciliar, certificando que não repete nenhum dos outros
    candidatos_sort_app = sorted(candidatos, key=lambda x: x[1].get("app_mata_ciliar_ha") or 0.0, reverse=True)
    idx = 0
    while idx < len(candidatos_sort_app) and candidatos_sort_app[idx][0] in (cod_max_deficit, cod_min_deficit):
        idx += 1
    if idx < len(candidatos_sort_app):
        cod_max_app, an_max_app = candidatos_sort_app[idx]
    else:
        resto = [c for c in candidatos if c[0] not in (cod_max_deficit, cod_min_deficit)]
        cod_max_app, an_max_app = resto[0]
        
    selected = [
        (cod_max_deficit, an_max_deficit, "Perfil 1: Maior déficit de Reserva Legal"),
        (cod_min_deficit, an_min_deficit, "Perfil 2: Menor déficit / Mais próximo da regularidade"),
        (cod_max_app, an_max_app, "Perfil 3: Maior área de mata ciliar")
    ]
    
    # Grava data/imoveis_teste.local.txt
    local_txt.parent.mkdir(parents=True, exist_ok=True)
    with open(local_txt, "w", encoding="utf-8") as f:
        for cod, _, _ in selected:
            f.write(f"{cod}\n")
            
    # Imprime no stdout sem o cod
    print("\nSelecionados para Demonstração (Sem exibir os códigos reais):")
    print("="*60)
    for i, (_, an, perfil) in enumerate(selected):
        def_str = f"{an['rl_deficit_ha']:.1f}" if an.get("rl_deficit_ha") is not None else "None"
        print(f"Demo {i+1} - {perfil}:")
        print(f"  Área Total: {an['area_ha']:.1f} ha")
        print(f"  Reserva Legal Proposta: {an['rl_proposta_ha']:.1f} ha (Exigida: {an['rl_exigida_ha']:.1f} ha)")
        print(f"  Déficit de Reserva Legal: {def_str} ha")
        print(f"  Mata Ciliar (APP): {an['app_mata_ciliar_ha']:.1f} ha ({an['campos_futebol']} campos de futebol)")
        print()
        
    print(f"Códigos reais gravados em {local_txt}")
    print(f"Tabela completa de candidatos gravada em {candidatos_txt}")

if __name__ == '__main__':
    main()
