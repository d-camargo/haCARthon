# Decisão de canal de entrega: Plugin QGIS × Painel Web × Híbrido

> Analisa a proposta de entregar o pipeline (R1+R2) como **plugin do QGIS** para a Luana, em vez de
> (ou além de) o painel web. Inclui validação da suposição "Luana usa QGIS", o que ela faz com as
> análises, comparação Impacto×Esforço e o "Pedido" (passos fora do escopo deste projeto).
> Data: 2026-06-25.

## 1. O que a Luana faz com as análises (fundamenta o escopo da ferramenta)

Fonte: `Onde-Estamos-2025.pdf` (Fig. 8 "Etapas da Análise Dinamizada", p.84; "Principais Desafios da
Análise", p.86) + manuais do SICAR.

A Luana (equipe técnica do órgão estadual) recebe os cadastros que a automação **não** resolveu ou
que o produtor **não aceitou**. O fluxo dela:

1. **Análise do CAR pela equipe técnica** — confere o declarado contra as bases (cobertura do solo,
   hidrografia, fundiárias, sobreposições).
2. **Análise de regularidade ambiental** — verifica conformidade com o Código Florestal.
3. **Decisão / encaminhamento:**
   - **Passivos de APP/RL? → encaminha ao PRA** (Programa de Regularização Ambiental, termo de compromisso).
   - **Sem passivos → atesta "CAR analisado, em conformidade".**
   - **Inconsistência → notifica o proprietário** para retificar/complementar → **ciclos sucessivos** de reanálise.

**Produtos do trabalho dela:** parecer/Relatório de Análise Técnica (RAT), **notificações**, e a decisão
de validação. **Para que serve a jusante:** habilita regularização (PRA), **crédito rural**, compliance/
rastreabilidade (Selo Verde, *due diligence*), e fiscalização.

> 💡 Implicação de design: a ferramenta ideal não para na **detecção** de sobreposição — ela deve ajudar
> a **produzir o parecer/notificação** e priorizar a fila. Isso vale para qualquer canal (plugin ou web).

Os 4 desafios da análise nomeados pelo estudo (p.86) reforçam nossos gaps: (i) baixa qualidade dos
cadastros; (ii) comunicação com proprietários; (iii) equipe técnica reduzida/ausente; (iv) **bases
cartográficas de referência insuficientes**.

## 2. Validação da suposição "Luana usa QGIS" → CONFIRMADA

> Links e datas de acesso consolidados em `docs/referencias.md`.

| Evidência | Implicação |
|---|---|
| **Plugin [GeoCAR](https://plugins.qgis.org/plugins/geocar/)** no repositório oficial do QGIS (preparar/analisar/exportar CAR) | O padrão "plugin de CAR no QGIS" **já existe** — extensão, não invenção |
| **SFB ensina geoprocessamento do CAR em QGIS** ([Saberes da Floresta](https://saberes.florestal.gov.br/mod/page/view.php?id=11845)) | O ecossistema **oficial** já assume QGIS no fluxo de análise |
| **ENAP** oferece [Geoprocessamento Aplicado às Políticas Públicas](https://suap.enap.gov.br/vitrine/curso/1822/) (intro a QGIS) | O gancho de **capacitação** é real e do próprio organizador |
| Papers de análise de sobreposição do CAR em QGIS ([CONTECC 2025](https://www.confea.org.br/midias/uploads-imce/CONTECC2025/AGRO/AN%C3%81LISE_DE_SOBREPOSI%C3%87%C3%83O_NO_CADASTRO_AMBIENTAL_RURAL_(CAR)_COM_USO_DA_BASE_FUNDI%C3%81RIA_DO_SIGEF.pdf)) | Detecção de sobreposição em QGIS é **prática estabelecida** |
| QGIS é gratuito (sem licença vs. ArcGIS) | Padrão de fato no setor público estadual |

> ⚠️ Nuance importante (da pesquisa): **o SICAR admite sobreposições no momento da inscrição** (imóveis
> com CPF/CNPJ diferentes). Nem toda sobreposição é "ilegal" — muitas são declaradas e resolvidas na
> análise. Logo, a detecção precisa de **tolerância e classificação** (já temos tolerância na PoC), não
> tratar todo overlap como erro.

> 🔁 GeoCAR existe e **prepara/exporta** dados do CAR — nosso diferencial é a **detecção de sobreposição
> entre sistemas** (CAR×assentamento via INCRA) + **priorização da fila**, que o GeoCAR não faz. Coerente
> com o princípio do projeto: **estender o que já existe**, não recriar.

## 3. Comparação dos canais

| Critério | Plugin QGIS | Painel Web (Leaflet/RER) | Híbrido |
|---|---|---|---|
| Ataca o Gap C ("mais um sistema") | 🟢 dentro do que ela já usa | 🟠 risco de virar o 6º sistema | 🟢 |
| Encaixe com nosso pipeline (WFS/PostGIS/GDAL) | 🟢 nativo (PyQGIS/Processing) | 🟢 (já feito) | 🟢 |
| Poder de GIS (editar, medir, cruzar, mapa) | 🟢 completo, de graça | 🔴 reimplementar | 🟢 |
| Visão de **gestão/fila** (12 mil, métricas) | 🟠 fraco | 🟢 forte | 🟢 |
| Acionável (vs. dashboard read-only) | 🟢 | 🟠 | 🟢 |
| Custo de operação p/ o órgão (infra/host) | 🟢 roda na máquina dela | 🟠 hospedar app+servidor | 🟠 |
| Alinhamento à pilha do RER (web) | 🟠 canal distinto (mas consome WFS/PostGIS) | 🟢 | 🟢 |
| Manutenção | 🟠 API PyQGIS muda entre versões | 🟠 | 🔴 dois frontes |
| Pressupõe proficiência QGIS | 🟠 (mitiga: curso ENAP) | 🟢 baixa | 🟠 |
| Apelo no pitch | 🟢 banca técnica / 🟠 banca inovação | 🟢 visual | 🟢 |
| **Esforço de protótipo** | 🟡 médio (metadata + 1 algoritmo Processing) | 🟢 já existe | 🟡 |

### Impacto × Esforço
- **Plugin QGIS:** impacto 🟢 alto (ataca a raiz do Gap C) · esforço 🟡 médio (o motor já existe; falta o wrapper).
- **Painel web:** impacto 🟡 médio-alto · esforço 🟢 baixo (pronto).
- **Híbrido:** impacto 🟢 alto · esforço 🟡 médio (reusa os dois).

## 4. Recomendação: **Híbrido, liderando pelo plugin QGIS**

O ativo central é o **pipeline de integração**. Ele aflora por duas faces, **sem desperdiçar nada**:

| Face | Persona / uso | Estado |
|---|---|---|
| **Plugin QGIS** | Luana **analista** — trabalho profundo, caso a caso, gerar parecer | a construir (wrapper do pipeline) |
| **Painel web** | **gestão/triagem** + transparência + demo do pitch | ✅ já existe (`painel.html`) |

Se a Luana é A persona, **liderar pelo plugin** é a resposta mais fiel a "não crie mais um sistema".
Custo de mudar de rota agora é baixo porque o motor (baixar* + SQL de detecção) é o mesmo.

## 5. O "Pedido" — passos necessários **fora do escopo** deste projeto

(Para o eixo "Do que você precisa?" do pitch — ver `pitch.md`.) Validar a ideia ≠ colocar em produção.
Para virar realidade, precisamos de:

1. **Parceria com um órgão estadual** (ex.: IAT/PR) para **validar com analistas reais** e medir ganho de tempo na fila — a maior necessidade.
2. **Parceria SFB + ENAP** para **capacitação** (curso "QGIS aplicado à análise do CAR") — escala de adoção.
3. **Publicação do plugin** no repositório oficial do QGIS e **homologação pela TI** dos órgãos.
4. **Endpoints/bases estáveis**: assentamentos do INCRA hoje exigem login; integração SNCR/SIGEF (em curso via ADPF 743) e um WFS estável.
5. **Piloto** num recorte real (Querência do Norte/PR já tem dado para isso).
6. **Alinhamento com a Rede CAR / SFB** para não fragmentar (coerência com o movimento de integração federal).
7. **Infra PostGIS** para escala estadual (quando passar de município para UF inteira).

## 6. Assunções remanescentes / riscos
- A proficiência em QGIS **varia** entre analistas → o curso ENAP deixa de ser "bônus" e vira parte da proposta.
- Plugin desktop não cobre bem a **camada de gestão** → por isso o híbrido com o painel web.
- Manter alinhamento com o **RER/SFB** para o plugin ser visto como complemento oficial, não paralelo.

> Decisão a confirmar com a equipe: adotar o **híbrido (plugin como rosto da Luana + painel web como gestão)**?
> Se sim, próximo passo técnico é um **esqueleto de plugin QGIS** (metadata.txt + algoritmo Processing que
> chama a detecção do pipeline).
