# Relatório do Construtor — rodada 01

## Versão examinada

Sem commit (pasta de trabalho sem Git). SHA-256 dos arquivos da entrega:

| Arquivo | SHA-256 |
|---|---|
| `projeto-dashboard/preparar_dados.py` | `6C8593F138BB003BF23B54E151C992DA835764888EBA341B5B4F90C7976B68F3` |
| `projeto-dashboard/README.md` | `528D8E1549FF701550BACB50D1852B284BF97AFC43A0A1C89E3F360E4F3285EA` |
| `projeto-dashboard/site/dados.json` | `65FE7740872B4820AA0CB93E366B440CEA22C1660D6997F384046E7B9D1F421F` |
| `projeto-dashboard/site/index.html` | `4A65103A926C4A4197E22824FFF9043EF5CD1D4DDA2A99B505683848A9E14993` |
| `projeto-dashboard/site/estilos.css` | `B2ACFCCE41F76A583ADA800C724EAF635B2323009C57DB8CE33D85DC28277A51` |
| `projeto-dashboard/site/dashboard.js` | `C6300B0699206108993D66634E9FB0E9A1785A9465561ACD77B09ED6FAF1A117` |

Preservação conferida contra as referências de início da coordenação: `papelaria_limpa.csv` `543C97179CED2CE2C6BFDECA0693D19BC1BD4BA78A7BED7EAC7A33C7F1DD9930`; `resumo.md` `88E8155BCF8DF341FCBC6BCC8FF9866D74B7F33450EB01C7696821F6386AD2A2`; `verificacao.md` `0AD78DF5DF4A7C543900063C7EED05616D3DB916EA87EE2CA8945D7B5666A8AF`. Os hashes coincidem; esses arquivos não foram alterados.

## Construído

- `preparar_dados.py` valida a estrutura, IDs, ausências, datas e a relação `quantidade × preco_unitario`; usa pandas e gera `site/dados.json` sem mudar o CSV limpo.
- Site estático responsivo com três KPIs, gráfico por categoria, gráfico mensal, tabela, filtros de cidade/categoria, limpar filtros, estado vazio e navegação padrão por teclado. Sem CDN ou servidor de aplicação.
- `README.md` descreve granularidade, tratamento herdado, métricas, limites, preparação, suíte de testes e HTTP local. `site/` está indicada como pasta publicável.
- As instruções locais em `.agents/skills/` para `explore-data`, `data-visualization` e `validate-data` não existem. Não afirmo uso dessas skills; consultei `resumo.md` e `verificacao.md` para preservar a análise anterior.

## Comandos, resultados e evidências

- `.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py` — passou; gerou 180 registros e 9 colunas em `site/dados.json`.
- Conferência ad hoc com pandas/JSON — passou: 180 IDs únicos, esquema de nove campos e soma de `valor_venda` igual a 20059.00. Resultado registrado no terminal.
- `node --check .\projeto-dashboard\site\dashboard.js` — passou, sem erro de sintaxe.
- Smoke HTTP com `http.server` em porta local — passou; `index.html`, `dados.json`, `dashboard.js` e `estilos.css` responderam; conferência registrada no terminal.
- A primeira tentativa da conferência ad hoc foi interrompida por aspas incorretas no comando PowerShell; o comando corrigido foi executado e passou.
- A suíte de `projeto-dashboard/tests/test_dashboard.py` foi preparada pelo tester/coordenador em paralelo e não foi executada por este agente, para deixar a execução e evidências ao tester. Testes de navegador e interação real: **PENDENTES**.

## Problemas e encaminhamento

- Tester: executar a suíte independente, validar os filtros combinados/vazios e registrar a evidência de interação. Navegador/Playwright ainda não foi validado nesta etapa.
- Revisor: revisar cálculos, interface e evidências após a execução dos testes.
- Skill local ausente: informar na síntese final que os três arquivos de skill não foram encontrados.

## Status

**BLOQUEADO** para aprovação conjunta: a construção e os smoke checks passaram, mas a suíte do tester, a interação de navegador e a revisão independente permanecem **PENDENTES**. Próximo passo: tester executar os testes sobre estes hashes e encaminhar qualquer falha ao construtor.
