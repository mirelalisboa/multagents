# Relatório do Revisor — rodada 04

## Versão examinada

Sem commit (diretório sem Git). Hashes SHA-256 conferidos após a regeneração:

| Arquivo | SHA-256 |
|---|---|
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` | `543C97179CED2CE2C6BFDECA0693D19BC1BD4BA78A7BED7EAC7A33C7F1DD9930` |
| `projeto-dashboard/README.md` | `41FF68F4ACB6D2BA3D45995FB2F73D4B86AD97CFD38A5EE66B3A673284571DD9` |
| `projeto-dashboard/preparar_dados.py` | `030680E4BAB5B65998BF7D124F47DB5E1B7709C726EF4C8DA7BE287D3B21DC41` |
| `projeto-dashboard/site/index.html` | `2E5207E5607048A91626CBA18C8331483AE14B7D950D7AD98FD906332DE88A08` |
| `projeto-dashboard/site/estilos.css` | `01699C2C21144C7C302850A7FF324C56C06CE4C9C5BCB2F8D028ADFB6B20F4CC` |
| `projeto-dashboard/site/dashboard.js` | `2279F2050DD2BA52C8C6480A7EC9DEF4A0AFFEAA136BC0BB3F184E85FF432DE4` |
| `projeto-dashboard/site/dados.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `projeto-dashboard/tests/test_dashboard.py` | `72B65821D54804A8B0F1371B4333A317A7B77D80C08A00588C85E18FDD922508` |

## Conferências

- `index.html` embute os 180 registros no `<script type="application/json" id="dashboard-data">`. O payload embutido coincide com `site/dados.json`; não há `fetch()`/XHR, CDN, `<script type="module">`, `import`, `export`, `const`, `let`, `async`, `await` ou arrow functions. A busca textual por “fetch/XHR” encontrou somente o comentário explicativo do JavaScript, não uma chamada executável.
- O HTML usa duas referências locais (`estilos.css` e `dashboard.js`), ambas existentes. Assim, é autocontido como pacote estático para `file://` (dados locais embutidos, sem rede), mas não é um arquivo único que dispense esses dois arquivos locais.
- O dashboard mantém três indicadores (valor vendido, quantidade de vendas e ticket médio), dois gráficos, tabela, filtros de cidade/categoria, limpar filtros, estado vazio, formatação monetária, rótulos semânticos e layout responsivo. A documentação não chama vendas de lucro.
- O README documenta preparação, testes, duplo clique/`file://`, `Start-Process`, HTTP local e publicação de `site/`.
- O pipeline valida as nove colunas, ausências/texto vazio, IDs, datas, números finitos, quantidade inteira positiva e `valor_venda = quantidade × preco_unitario`; grava `dados.json` e atualiza o payload HTML atomicamente.
- A conferência independente mantém 180 vendas, 180 IDs únicos e total de `20059` (R$ 20.059,00). Os CSVs original e limpo permaneceram preservados.

## Comandos e evidências

1. `.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v` — **14 testes descobertos; 10 passaram e 4 foram pulados; código 0**. Os quatro testes pendentes são `file://`, filtros/interação, responsividade e teclado, todos dependentes de browser.
2. `.\.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py` — passou; atualizou `dados.json` e dados embutidos com 180 registros.
3. `node --check .\projeto-dashboard\site\dashboard.js` — passou, sem erro sintático.
4. Servidor HTTP com `.\.venv\Scripts\python.exe -m http.server ... --directory .\projeto-dashboard\site` — `/`, `/index.html`, `/dados.json`, `/dashboard.js` e `/estilos.css` responderam HTTP 200.
5. Verificação estática do HTML/JS — `inline_rows=180; module_refs=0; local_refs=2`; as duas referências locais existem.
6. Hashes e suíte confirmaram que a preparação não alterou `vendas_papelaria.csv` nem `papelaria_limpa.csv`.

## Problemas e encaminhamento

- **Tester/ambiente — pendência obrigatória:** Playwright/Selenium e Chrome/Chromium/Edge/Firefox não estão disponíveis. Os 4 testes reais de abertura `file://`, interação de filtros, responsividade e teclado permanecem **PENDENTES**. Disponibilizar Playwright com navegador e repetir a suíte completa.
- Não encontrei falha reproduzível nos cálculos, preservação, requisitos estáticos, dependências de rede, documentação ou smoke HTTP. A distinção entre pacote autocontido e arquivo único deve ser mantida clara se “autocontido” for interpretado como um único HTML.

## Status

**BLOQUEADO** — as verificações estáticas, pipeline, dados, documentação, sintaxe e HTTP passaram (10 testes); os 4 testes reais de browser continuam pendentes. Não é possível declarar **APROVADO** sem evidência de interação, `file://`, responsividade e teclado em navegador real.
