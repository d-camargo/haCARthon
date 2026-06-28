"""Módulo para seleção determinística de imóveis de demonstração (Querência do Norte/PR).

Varre a base local de Querência do Norte em busca de imóveis com APP e RL
declaradas, filtrando para garantir que apenas pequena e média propriedade
(até 15 módulos fiscais) sejam selecionadas para a demonstração do Seu Raimundo.
"""
import sys
import json
from pathlib import Path
import cadastro
import analise

# Constante de módulo fiscal de Querência do Norte/PR (INCRA)
MODULO_FISCAL_HA = 30.0


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
            # Calcula o enquadramento em módulos fiscais e classificação
            mf = an["area_ha"] / MODULO_FISCAL_HA
            if mf <= 4.0:
                classe = "Pequeno"
            elif mf <= 15.0:
                classe = "Médio"
            else:
                classe = "Grande"
                
            an["modulos_fiscais"] = mf
            an["classe"] = classe
            candidatos.append((cod, an))
            
    if len(candidatos) < 3:
        print(f"Erro: Apenas {len(candidatos)} candidatos com APP e RL encontrados (necessário pelo menos 3).")
        sys.exit(1)
        
    # Grava a tabela completa contendo TODOS os candidatos em data/candidatos_demo.local.txt
    candidatos_txt.parent.mkdir(parents=True, exist_ok=True)
    with open(candidatos_txt, "w", encoding="utf-8") as f:
        f.write("Tabela de Candidatos de Demonstração (Querência do Norte/PR)\n")
        f.write("="*90 + "\n")
        f.write(f"{'Índice':<6} | {'cod_imovel':<44} | {'Área (ha)':<10} | {'MF':<6} | {'Classe':<10} | {'RL Prop (ha)':<12} | {'RL Exig (ha)':<12} | {'RL Def (ha)':<12} | {'APP (ha)':<8}\n")
        f.write("-"*125 + "\n")
        for i, (cod, an) in enumerate(candidatos):
            def_str = f"{an['rl_deficit_ha']:.1f}" if an.get("rl_deficit_ha") is not None else "None"
            f.write(f"{i:<6} | {cod:<44} | {an['area_ha']:<10.1f} | {an['modulos_fiscais']:<6.1f} | {an['classe']:<10} | {an['rl_proposta_ha']:<12.1f} | {an['rl_exigida_ha']:<12.1f} | {def_str:<12} | {an['app_mata_ciliar_ha']:<8.1f}\n")

    # Filtra os candidatos para pequeno e médio produtor rural (<= 15 módulos fiscais)
    candidatos_validos = [c for c in candidatos if c[1]["modulos_fiscais"] <= 15.0]
    print(f"Total de candidatos válidos (Pequeno/Médio, <= 15 MF): {len(candidatos_validos)} de {len(candidatos)}")

    if len(candidatos_validos) < 3:
        print(f"Erro: Apenas {len(candidatos_validos)} candidatos pequeno/médio com APP e RL encontrados.")
        sys.exit(1)

    # Seleciona 3 contrastantes de forma determinística
    # 1. Perfil 1: Pequena propriedade (1-4 MF) com maior déficit de RL ("herói")
    candidatos_pequenos = [c for c in candidatos_validos if c[1]["classe"] == "Pequeno"]
    if candidatos_pequenos:
        candidatos_pequenos_sort = sorted(candidatos_pequenos, key=lambda x: x[1].get("rl_deficit_ha") or 0.0, reverse=True)
        cod_max_deficit, an_max_deficit = candidatos_pequenos_sort[0]
    else:
        # Fallback caso não haja pequeno
        candidatos_sort_deficit = sorted(candidatos_validos, key=lambda x: x[1].get("rl_deficit_ha") or 0.0, reverse=True)
        cod_max_deficit, an_max_deficit = candidatos_sort_deficit[0]
    
    # 2. Perfil 2: Menor déficit de RL (mais perto da regularidade, déficit ~0) entre os demais pequeno/médio
    candidatos_sem_p1 = [c for c in candidatos_validos if c[0] != cod_max_deficit]
    candidatos_sort_min_deficit = sorted(candidatos_sem_p1, key=lambda x: x[1].get("rl_deficit_ha") or 0.0)
    cod_min_deficit, an_min_deficit = candidatos_sort_min_deficit[0]

    # 3. Perfil 3: Maior área de mata ciliar (APP) entre os demais pequeno/médio
    candidatos_sem_p1_p2 = [c for c in candidatos_validos if c[0] not in (cod_max_deficit, cod_min_deficit)]
    candidatos_sort_app = sorted(candidatos_sem_p1_p2, key=lambda x: x[1].get("app_mata_ciliar_ha") or 0.0, reverse=True)
    cod_max_app, an_max_app = candidatos_sort_app[0]
        
    selected = [
        (cod_max_deficit, an_max_deficit, "Perfil 1: Pequeno Produtor com maior déficit de Reserva Legal (Herói)"),
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
    print("="*70)
    for i, (_, an, perfil) in enumerate(selected):
        def_str = f"{an['rl_deficit_ha']:.1f}" if an.get("rl_deficit_ha") is not None else "None"
        print(f"Demo {i+1} - {perfil}:")
        print(f"  Classe: {an['classe']} ({an['modulos_fiscais']:.1f} Módulos Fiscais)")
        print(f"  Área Total: {an['area_ha']:.1f} ha")
        print(f"  Reserva Legal Proposta: {an['rl_proposta_ha']:.1f} ha (Exigida: {an['rl_exigida_ha']:.1f} ha)")
        print(f"  Déficit de Reserva Legal: {def_str} ha")
        print(f"  Mata Ciliar (APP): {an['app_mata_ciliar_ha']:.1f} ha ({an['campos_futebol']} campos de futebol)")
        print()
        
    print(f"Códigos reais gravados em {local_txt}")
    print(f"Tabela completa de candidatos gravada em {candidatos_txt}")

if __name__ == '__main__':
    main()
