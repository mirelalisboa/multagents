# Relatório final — dashboard de vendas de papelaria

## Status conjunto — rodada 04

**BLOQUEADO — não aprovado**, conforme os critérios do `AGENTS.md`.

Construtor, Tester e Revisor conferiram a mesma versão reconstruída na rodada 04. Os dados, cálculos, pipeline, site estático e documentação estão consistentes. Porém, os quatro testes obrigatórios de abertura/interação real no navegador não puderam ser executados porque o ambiente não possui Playwright nem navegador compatível.
## Entrega

- Base usada: `papelaria_limpa.csv`.
- Site publicável: `projeto-dashboard/site/`.
- Preparação: `projeto-dashboard/preparar_dados.py` (reconstruído na rodada 04).
- Dados publicados: `projeto-dashboard/site/dados.json`.
- Testes: `projeto-dashboard/tests/test_dashboard.py`.
- Documentação: `projeto-dashboard/README.md`.
- Histórico: `relatorios/rodada-01/`, `relatorios/rodada-02/`, `relatorios/rodada-03/` e `relatorios/rodada-04/`.

O dashboard contém três indicadores, dois gráficos, tabela, filtros por cidade e categoria, botão de limpeza, mensagem para seleção vazia, formatação brasileira e layout responsivo. O valor vendido é documentado como diferente de lucro.

## Resultados verificados na rodada 04

- 180 vendas e 9 colunas na base limpa.
- R$ 20.059,00 em valor vendido.
- Ticket médio: R$ 111,44.
- 548 unidades vendidas.
- CSV original e CSV limpo preservados; hashes conferidos.
- Suíte: **14 testes descobertos; 10 passaram; 4 foram pulados** por falta de Playwright/navegador.
- Preparação, JSON, cálculos independentes, referências locais, sintaxe JavaScript, HTTP, DOM estático e preservação dos arquivos passaram.
- O HTML contém os dados necessários e o dashboard não usa `fetch`, XHR, módulos ou CDN; pode ser aberto por duplo clique. CSS e JavaScript continuam sendo arquivos locais que devem permanecer junto do HTML.
- Hashes principais da reconstrução: `preparar_dados.py` `C0FC3887AFF24BB31F84FA60FC40DC90472C43B7A71AFE831D03182E8BD8DAB0`; `site/index.html` `FFEE17D383465B705BF3842D521A3F19352A93FCAFF3D1F637878836D08FFB62`; `site/dashboard.js` `D426E4B18697AB045799A713CAA3620134BAC4ED3902B9C858319D278E5ED9A1`; `site/dados.json` `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694`.

## Pendência obrigatória

Instalar Playwright e um navegador Chromium (ou disponibilizar navegador compatível) e executar novamente:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v
```

Os testes pendentes verificam abertura real por `file://`, filtros isolados e combinados, seleção sem resultados, botão limpar, atualização conjunta de KPIs/gráficos/tabela, ausência de `NaN`/`Infinity`, responsividade, teclado e erros reais de JavaScript.

## Como abrir

Na raiz que contém `papelaria_limpa.csv`:

```powershell
.\.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py
.\.venv\Scripts\python.exe -m http.server 8000 --directory .\projeto-dashboard\site
```

Abra <http://localhost:8000>. A publicação estática deve usar somente `projeto-dashboard/site/`.

## Observação sobre skills

Os arquivos locais `SKILL.md` de `explore-data`, `data-visualization` e `validate-data`, nos caminhos indicados pelo `AGENTS.md`, não foram encontrados. Essa ausência foi registrada nos relatórios; não se afirma o uso desses arquivos locais.

## Relatórios de evidência

- `relatorios/rodada-01/construtor.md`
- `relatorios/rodada-01/tester.md`
- `relatorios/rodada-01/revisor.md`
- `relatorios/rodada-02/construtor.md`
- `relatorios/rodada-02/tester.md`
- `relatorios/rodada-02/revisor.md`
- `relatorios/rodada-03/construtor.md`
- `relatorios/rodada-03/tester.md`
- `relatorios/rodada-03/revisor.md`
- `relatorios/rodada-04/construtor.md`
- `relatorios/rodada-04/tester.md`
- `relatorios/rodada-04/revisor.md`
