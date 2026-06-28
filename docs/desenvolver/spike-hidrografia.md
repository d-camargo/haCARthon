# Spike - Nome do Rio e Faixa de Mata Ciliar por Hidrografia de Referência

**Data da análise:** 2026-06-28  
**Autor:** Executor Júnior  
**Status do Spike:** Concluído (Pesquisa)  
**Recomendação:** Adiar a integração em tempo real e focar na leitura dos dados declarados do próprio CAR.

---

## 1. Objetivo
Investigar a viabilidade de consultar fontes externas de hidrografia em tempo real (via WFS/WMS) para extrair o **nome do rio** que corta ou faz divisa com o imóvel rural e determinar a largura do rio (e consequentemente a faixa de APP de 30m, 50m, etc.).

---

## 2. Fontes de Dados Investigadas

### A. ANA (Agência Nacional de Águas) - Base Hidrográfica Ottocodificada (BHO)
* **Endpoint:** Serviços OGC integrados no Portal de Geoserviços/ArcGIS Server do SNIRH.
* **Viabilidade técnica:** 
  - A ANA migrou a maior parte dos serviços OGC legados (GeoServer) para a infraestrutura do ArcGIS Online/Portal de Geoserviços. Os endpoints WFS oficiais são difíceis de rastrear de forma estática e apresentam frequentes janelas de manutenção.
  - A escala da BHO nacional (1:250.000) é inadequada para pequenas propriedades. Rios menores (onde ficam a maioria das APPs de 30 metros) frequentemente não são mapeados ou nomeados nessa escala.
  - O tempo de resposta de requisições espaciais por `bbox` em bases nacionais pesadas via `/vsicurl/` excede os 20 segundos em momentos de pico, inviabilizando a experiência conversacional do bot.

### B. IBGE - Base Cartográfica Integrada Contínua do Brasil (BCIM)
* **Endpoint WFS:** `https://geoservicos.ibge.gov.br/geoserver/wfs`
* **Viabilidade técnica:** 
  - Possui dados de drenagem e corpos d'água estruturados.
  - Assim como a BHO, sofre com a questão de escala de detalhamento (1:250.000). Apenas rios de médio e grande porte possuem nomes associados nos atributos da feição.
  - Servidores do IBGE têm instabilidade histórica sob grande volume de requisições externas simultâneas.

### C. SNIF (Sistema Nacional de Informações Florestais)
* **Status:** O servidor GeoServer do SNIF apresentou erros recorrentes HTTP 500 (Erro Interno) e redirecionamentos HTTP 301 instáveis durante os testes.

---

## 3. Achados Importantes
1. **Ausência de Nomes em Rios Pequenos:** A esmagadora maioria dos córregos e rios que cruzam pequenas propriedades rurais (sítios de até 4 módulos fiscais) são corpos d'água de pequeno porte (menos de 10m de largura). Nessas bases de escala nacional (1:250.000), esses rios aparecem sem nome nos atributos (campos de nome nulos ou vazios).
2. **Dados Declarados do CAR como Melhor Fonte:** O próprio arquivo vetorial de APP gerado no SICAR e preenchido na declaração do produtor (já disponível na base local e no download oficial do CAR) possui o desenho exato da hidrografia declarada pelo proprietário ou vetorizada pelo órgão ambiental. Essa fonte é 100% precisa em relação ao que está sendo cobrado na notificação.

---

## 4. Recomendação
**Recomendamos adiar a integração de WFS de hidrografia de referência externa em tempo real.**

### Justificativas:
1. **Instabilidade:** A dependência de múltiplos endpoints governamentais adicionais (ANA/IBGE) multiplica os pontos de falha e lentidão do bot.
2. **Frustração do Usuário:** O produtor (Seu Raimundo) poderia receber mensagens confusas como "Seu imóvel fica perto de um rio sem nome no sistema" ou com o nome incorreto do rio devido a generalizações de escala.
3. **Alternativa Prática para o Futuro:** Em vez de consultar um WFS de hidrografia geral, o bot deve ler a camada de **Hidrografia Declarada** ou **APP** contida no pacote de dados do próprio imóvel. Quando o imóvel for carregado da base local (como na demo de Querência do Norte), as informações de APP já são extraídas das feições reais ali presentes. Para o WFS online (que traz apenas o perímetro), o bot deve continuar tratando a mata ciliar de forma dimensional (presumindo rio com menos de 10m de largura e faixa de 30m), orientando o produtor rural a realizar a conferência detalhada diretamente no SICAR.
