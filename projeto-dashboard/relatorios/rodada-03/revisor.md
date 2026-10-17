# Relatório do Revisor — rodada 03

## Versão examinada

Sem commit (diretório sem Git). Hashes SHA-256 conferidos nesta revisão:

| Arquivo | SHA-256 |
|---|---|
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` | `543C97179CED2CE2C6BFDECA0693D19BC1BD4BA78A7BED7EAC7A33C7F1DD9930` |
| `projeto-dashboard/README.md` | `5DFFCE1FE33FD85E9E5DBDB74F3DCF55126C8CA5320ECE4DE3AE0596C9802995` |
| `projeto-dashboard/preparar_dados.py` | `C0FC3887AFF24BB31F84FA60FC40DC90472C43B7A71AFE831D03182E8BD8DAB0` |
| `projeto-dashboard/site/index.html` | `FFEE17D383465B705BF3842D521A3F19352A93FCAFF3D1F637878836D08FFB62` |
| `projeto-dashboard/site/estilos.css` | `EA17053B040D1130DFFC6741EC77CB21D039E00BCE6F5AF0263AB4C69F102A9F` |
| `projeto-dashboard/site/dashboard.js` | `D426E4B18697AB045799A713CAA3620134BAC4ED3902B9C858319D278E5ED9A1` |
| `projeto-dashboard/site/dados.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `projeto-dashboard/tests/test_dashboard.py` | `A36E9C9F427F5F472E262F85A61896B031E34FFFAAF1F2C13A8687A254839531` |

Os hashes coincidem com os relatórios do Construtor e Tester da rodada 03. Os arquivos das skills locais `explore-data`, `data-visualization` e `validate-data` continuam ausentes conforme registrado pelo Construtor; não afirmo uso desses arquivos.

## O que foi conferido

- **Preservação e pipeline:** o pipeline valida as nove colunas, ausências/texto vazio, IDs, datas, números finitos, quantidade inteira, positividade e `valor_venda = quantidade × preco_unitario`. A geração atômica do JSON não modifica o CSV original nem o limpo.
- **Cálculos:** conferência independente do JSON encontrou 180 linhas, 180 IDs únicos, total `20059` (R$ 20.059,00) e agrupamentos por categoria: Acessórios `10517`, Livros `7438`, Papelaria `2104`. Os valores conferem com a suíte independente.
- **Dashboard e documentação:** o HTML contém três indicadores (valor vendido, quantidade de vendas e ticket médio), dois gráficos, tabela, filtros de cidade/categoria, limpar filtros e estado vazio. A documentação define venda por linha, quantidade de unidades, tratamento herdado, limitações de lucro, período, comandos de preparação/testes/HTTP e `site/` como pasta publicável. Não chama valor vendido de lucro.
- **Acessibilidade estática:** há `lang=pt-BR`, labels associados, títulos, `scope=col`, `aria-live`, `role=status`, nomes dos SVGs e foco visível para controles/elementos dos gráficos. Responsividade, teclado e sincronização interativa precisam de execução real no navegador.

## Comandos, resultados e evidências

1. `.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v` — **12 testes descobertos; 9 passaram e 3 foram pulados; código 0**. Os nove cobrem preservação/limpeza, cálculos independentes, exemplo conhecido, pipeline, JSON, contrato DOM, referências, sintaxe JS e HTTP. Os três testes browser foram pulados por falta de Playwright/navegador.
2. `.\.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py` — passou e gerou 180 vendas/9 colunas.
3. `node --check .\projeto-dashboard\site\dashboard.js` — passou, sem erro sintático.
4. Servidor conforme README (`.\.venv\Scripts\python.exe -m http.server ... --directory .\projeto-dashboard\site`) — `/`, `/index.html`, `/dados.json`, `/dashboard.js` e `/estilos.css` responderam **HTTP 200**.
5. Hashes antes/depois da preparação — `raw_unchanged=True; clean_unchanged=True`.

## Problemas e encaminhamento

- **Tester/ambiente:** os três testes reais de navegador continuam **PENDENTES/BLOQUEADOS**. Playwright/Selenium e Chrome/Chromium/Edge/Firefox não estão disponíveis. Ainda não há evidência de filtros isolados/combinados, combinação vazia/limpar, atualização conjunta de KPIs/gráficos/tabela, ausência de erros no browser, responsividade real ou teclado. Disponibilizar Playwright com navegador e executar a suíte completa.
- Não encontrei falha reproduzível no pipeline, nos cálculos, na preservação, nos requisitos estáticos do dashboard, nos caminhos documentados ou no smoke HTTP. A aprovação visual/interativa não pode ser inferida dos testes estáticos.

## Status

**BLOQUEADO** — os dados, pipeline, documentação, site estático e nove testes não-browser estão consistentes, mas os três testes obrigatórios de interface real permanecem pendentes por falta de Playwright/navegador. Não é possível declarar **APROVADO**.
