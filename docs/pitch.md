# Pitch — Pré-Val CAR (haCARthon · Desafio 2)

> Rascunho/roteiro do pitch. Estrutura baseada na Live 04 (ver
> `docs/base-documental/metodologia/pitch.md`). Pitch ≈ 3 min, gravado na plataforma do hackathon
> (slides em PDF, áudio narrado). Preencher/ajustar antes de gravar.

## Frase-síntese (Mad Lib)
> Para **analistas ambientais estaduais** que **afogam numa fila de milhares de cadastros e pulam entre
> vários sistemas**, o **Pré-Val CAR** é um **plugin de QGIS (open source)** que **detecta sobreposições,
> prioriza a fila por risco e gera o parecer técnico** — **dentro da ferramenta que ela já usa**,
> diferente de "mais um sistema" para aprender.

## 1. Introdução
- Quem somos + nome do projeto: **Pré-Val CAR**.
- 1 frase: "Pré-validação geoespacial do CAR no QGIS — menos fila, menos retrabalho, análise mais rápida."

## 2. O problema (com dados — fonte: estudo CPI/PUC-Rio "Onde Estamos 2025", ver `docs/briefing.md`)
- **Escala:** ~**8 milhões** de imóveis no CAR; só **24%** com análise iniciada e **~9% validados**.
  Nove UFs não chegam a 1% validado. A fila é nacional e enorme.
- **Persona — Luana** (analista estadual): fila de ~12.000; detecta sobreposições "no olho"; alterna
  entre ~**4–6 sistemas** (SICAR/estadual, SNCR/SIGEF, INCRA, imagens, painéis de BI).
- **Gargalos nomeados pelo estudo:** (1) **sobreposições / situação fundiária** — em Mato Grosso **~30%**
  dos cadastros têm sobreposição que **trava** a validação; (2) comunicação com o proprietário.
- **Fragmentação de sistemas** (Tabela 4): 16 UFs usam o SICAR direto, 11 têm sistema próprio (muitos
  "forks" sem sincronia). Não existe "um" sistema → a dor do "muitos sistemas".

## 3. A solução
- **Pré-Val CAR**: plugin **open source de QGIS** (entrega para a Luana) + um **painel web** (visão de
  gestão/transparência). O ativo central é um **pipeline de integração** que afluencia nas duas faces.
- Princípio: **não criar mais um sistema** — entregar dentro do **QGIS**, que a analista já domina.

## 4. Como funciona (macro — detalhes no vídeo de 2 min)
Numa janela só, a analista:
1. **Baixa** os imóveis do CAR (filtro por município, grafia resolvida via IBGE) e os assentamentos do INCRA.
2. **Detecta e prioriza**: sobreposições CAR×CAR e CAR×assentamento, com **score de risco** → fila ordenada.
3. **KPIs** ao vivo (imóveis, em conflito, assentamentos, ha em conflito) + **mapa estilizado** (vermelho = risco alto).
4. **Gera o parecer/RAT** em PDF (Atlas: 1 imóvel por parecer, com mapa + memória de cálculo).

## 5. Diferenciais
- **Dentro do QGIS** (zero "novo sistema"; ataca a raiz do gargalo "muitos sistemas").
- **Dados oficiais e abertos, integrados de fato**: SICAR (WFS) + INCRA (i3geo WFS) num clique
  (resolvemos CRS, eixo invertido, SSL, normalização de município — a integração que a Luana faz na mão).
- **Inspirado na Retificação Dinamizada** (declarado × referência), estendido para o lado da análise.
- **Pega carona no movimento real**: CAR Pré-Preenchido já integra SNCR/SIGEF na entrada; propomos o mesmo na análise.
- 100% **open source (DPG)**, reusável por qualquer órgão estadual.

## 6. Impacto esperado
- **Menos tempo por cadastro** e **fila priorizada por risco** (a analista ataca primeiro o que importa).
- **Menos sobreposição passando despercebida** (detecção automática + parecer pronto).
- Escalável e barato: roda na máquina da analista; sem hospedar servidor.

## 7. Equipe
- _(nomes, papéis, foto — preencher)_

## 8. O Pedido (próximos passos — fora do escopo do hackathon)
Ver `docs/definir/opcao-entrega-qgis-vs-web.md` §5:
1. **Parceria com um órgão estadual** (ex.: IAT/PR) para validar com analistas reais e medir ganho de tempo.
2. **SFB + ENAP** para **capacitação** (curso "QGIS aplicado à análise do CAR").
3. **Publicação do plugin** no repositório oficial do QGIS + homologação pela TI dos órgãos.
4. **Bases estáveis** (endpoint do INCRA, integração SNCR/SIGEF).
5. **Piloto** num município/UF (já temos dado real do PR).

## 9. Encerramento (frase de impacto)
> "O CAR já tem os dados. A Luana já tem o QGIS. O Pré-Val CAR só **junta as duas coisas** — e transforma
> uma fila de 12 mil numa fila que **se prioriza sozinha**."

---
## Checklist de produção
- [ ] Slides (PDF, pouco texto, prints do plugin/painel)
- [ ] Print do **mapa estilizado** + da **fila priorizada** + do **parecer PDF** (já temos)
- [ ] Roteiro escrito + ensaio cronometrado (~3 min)
- [ ] Vídeo de protótipo (2 min) mostrando o fluxo 1→2→3 no QGIS
- [ ] Gravar na plataforma do hackathon
