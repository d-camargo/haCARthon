"""Script para simular atendimento do bot de forma local (sem Telegram).

Permite passar um código de imóvel e opcionalmente uma pergunta,
ou ler do arquivo de demonstração para rodar simulações rápidas.
"""
import sys
from pathlib import Path
import cadastro
import analise
import conteudo
import llm


def is_car_code(s: str) -> bool:
    """Verifica heurística para formato do código do CAR."""
    return len(s) >= 20 and s[2] == '-' and s[:2].isalpha()


def main():
    cod = None
    question = None
    
    args = sys.argv[1:]
    
    if len(args) == 0:
        pass
    elif len(args) == 1:
        if is_car_code(args[0]):
            cod = args[0]
        else:
            question = args[0]
    else:
        if is_car_code(args[0]):
            cod = args[0]
            question = args[1]
        else:
            question = args[0]
            
    # Se não temos o cod, lê o primeiro código da demo
    if not cod:
        local_txt = Path("data/imoveis_teste.local.txt")
        # imoveis_teste.example.txt é criado em src/terra-em-dia-bot/
        example_txt = Path("src/terra-em-dia-bot/imoveis_teste.example.txt")
        
        if local_txt.exists():
            with open(local_txt, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if lines:
                    cod = lines[0].strip()
        elif example_txt.exists():
            with open(example_txt, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        cod = line
                        break
                        
    if not cod:
        print("Erro: Nenhum código de imóvel foi fornecido e nenhum arquivo de teste foi encontrado.")
        sys.exit(1)
        
    imv = cadastro.carregar_imovel(cod)
    if not imv:
        print("Erro: Não foi possível carregar os dados da propriedade.")
        sys.exit(1)
        
    an = analise.analisar(imv)
    
    if not question:
        # Apresentação (resumo do imóvel)
        print(conteudo.resumo_imovel(an))
    else:
        # Histórico mínimo para llm
        hist = [{"role": "user", "content": question}]
        resp = llm.conversar(hist, an) or conteudo.resposta_curta(question, an)
        print(resp)


if __name__ == '__main__':
    main()
