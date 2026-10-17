# Construtor — rodada 04

## Versão examinada

Sem commit (pasta sem Git). SHA-256 dos artefatos da entrega:

| Arquivo | SHA-256 |
|---|---|
| `projeto-dashboard/README.md` | `41FF68F4ACB6D2BA3D45995FB2F73D4B86AD97CFD38A5EE66B3A673284571DD9` |
| `projeto-dashboard/preparar_dados.py` | `030680E4BAB5B65998BF7D124F47DB5E1B7709C726EF4C8DA7BE287D3B21DC41` |
| `projeto-dashboard/site/index.html` | `2E5207E5607048A91626CBA18C8331483AE14B7D950D7AD98FD906332DE88A08` |
| `projeto-dashboard/site/estilos.css` | `01699C2C21144C7C302850A7FF324C56C06CE4C9C5BCB2F8D028ADFB6B20F4CC` |
| `projeto-dashboard/site/dashboard.js` | `2279F2050DD2BA52C8C6480A7EC9DEF4A0AFFEAA136BC0BB3F184E85FF432DE4` |
| `projeto-dashboard/site/dados.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `projeto-dashboard/tests/test_dashboard.py` | `72B65821D54804A8B0F1371B4333A317A7B77D80C08A00588C85E18FDD922508` |

## Preservação conferida

| Arquivo preservado | SHA-256 |
|---|---|
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` | `543C97179CED2CE2C6BFDECA0693D19BC1BD4BA78A7BED7EAC7A33C7F1DD9930` |
| `resumo.md` | `88E8155BCF8DF341FCBC6BCC8FF9866D74B7F33450EB01C7696821F6386AD2A2` |
| `verificacao.md` | `0AD78DF5DF4A7C543900063C7EED05616D3DB916EA87EE2CA8945D7B5666A8AF` |
| `graficos.py` | `8ADD46A542DA318C077B8329F58929A5F6C8CDCAEAE8C33733E493FFB8471F59` |
| `cidades.png` | `DE0F1FA2B843064C7D95B9842B22DCDE0E272A8B1D1625366E9D9A996B9BEA36` |
| `categorias.png` | `CE9DF3F85C09354E2036BD6761D54BC9F3FC976D79D3BBD91FB1F7045B07E8CB` |

Relatórios anteriores não editados; hashes SHA-256: `relatorios/FINAL.md` `F202A45E913C928740D1646913FE33B9FF8F9ED0E0275C601510D91EAA90DE81`; rodada 01 — `coordenador.md` `30A8E1B123D662DB865CA218226E1F538D3DCA3A2EBC3F1A5E56F701320B2418`, `construtor.md` `B12D0DB084842CC6AC8786A8F1B8CFC960E3D9B150113EC5841AA51A5FD09FA6`, `tester.md` `CFC832D9526736FA4E68B7B3FF09C0CB237DA97D4D82B6EB784FC77156D77F5A`, `revisor.md` `ADA99968C9107ABE02A1A82A0CD37E59D5DC0FF3468C0973431CFD506F0807E6`; rodada 02 — `construtor.md` `A7BFF492DCF72DB8129E6FA21FA5571B60533826C0461ADD012B736A7AE8350F`, `tester.md` `783BA7D5D0EF938CDDFF022DAD88F09B6F3B8CD2F978133E0E111F131F09FB55`, `revisor.md` `BB88FD8FD60E21AE55F26BB98BE21AB2A495B61F62BD4E3F2D7AA02F5E824801`; rodada 03 — `construtor.md` `3D2FE65A3B97C9096B44D795C40883995784FD8D6B97D2949BDDE7A23CF1F6E9`, `tester.md` `AD03A84F6D915C38D2FA38C693333C1C0119DDE77D4396E996B676DCEB3BF614`, `revisor.md` `8CE2F1D61EAE21ADD14A70B14EB312AC07D85DBE0656289FCF6739DAA1B4FBE2`.

## Alterações realizadas

- Reconstruído o pipeline pandas. Ele valida as nove colunas, ausências, texto vazio, IDs, datas, valores finitos, quantidade inteira positiva e a regra `valor_venda = quantidade × preco_unitario`. Não altera o CSV limpo. Gera `dados.json` e embute os mesmos registros no HTML, com gravação atômica.
- Reconstruído o dashboard para abertura direta: dados autocontidos no `index.html`, CSS e JavaScript locais, sem CDN, `fetch`, XHR, módulos ou APIs modernas essenciais. O JavaScript usa sintaxe ES5 e DOM/SVG locais. `dados.json` permanece como artefato espelhado.
- Mantidos três KPIs (valor vendido, quantidade de vendas e ticket médio), gráficos por categoria e mês, tabela, filtros cidade/categoria sincronizados, botão limpar, estado vazio e layout responsivo com foco por teclado. Os rótulos distinguem número de vendas de unidades; valor vendido não é apresentado como lucro.
- O README documenta preparação/testes, abertura por duplo clique/`file://`, servidor HTTP opcional e `site/` como pasta publicável.
- Os testes existentes foram ampliados, não enfraquecidos: verificam JSON embutido igual ao artefato, ausência de APIs/modularização de rede e incluem teste Playwright para abertura `file://` sem requisições HTTP. Os testes reais de navegador permanecem na suíte e são pulados somente quando o ambiente não fornece Playwright/navegador.
- Os caminhos locais `.agents/skills/explore-data/SKILL.md`, `data-visualization/SKILL.md` e `validate-data/SKILL.md` não foram encontrados. As skills correspondentes disponíveis no harness foram consultadas; não se afirma uso dos arquivos locais ausentes.

## Comandos, resultados e evidências

- `.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py` — **passou**; atualizou JSON e HTML embutido com 180 registros.
- `node --check .\projeto-dashboard\site\dashboard.js` — **passou**, sem erro sintático.
- Smoke Python de payload — **passou**: JSON embutido decodifica, coincide com `dados.json`, contém 180 registros e totaliza R$ 20.059,00.
- Smoke HTTP local na porta 8768 — **passou**: `/`, `/dashboard.js`, `/estilos.css` e `/dados.json` responderam HTTP 200; JSON decodificado com 180 registros.
- `.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v` — **14 testes descobertos; 10 passaram e 4 foram pulados; código de saída 0**. Os quatro pulos são testes de interação, responsividade, teclado e abertura real `file://` no browser.
- Ambiente conferido: Playwright e Selenium ausentes; `chrome`, `msedge`, `chromium` e `firefox` não encontrados no PATH.

## Pendências e encaminhamento

- **PENDENTE/BLOQUEADO — browser real:** duplo clique real/`file://`, interação de filtros, sincronização de KPIs/gráficos/tabela, ausência de erros no navegador, teclado e layouts de tela pequena/grande ainda não foram executados em navegador. Disponibilizar Playwright e Chromium (ou navegador compatível) e repetir a suíte.
- Não há ferramenta de delegação de subagentes nesta execução; por isso, não foi produzida revisão independente nova nem foi simulada aprovação do Tester/Revisor. Os respectivos relatórios de rodadas anteriores foram preservados.
- Os smoke checks estáticos e HTTP não substituem a validação real de browser.

## Status

**BLOQUEADO** para aprovação conjunta: preparação e verificações executáveis passaram, mas 4 testes de browser e a revisão independente desta rodada permanecem **PENDENTES**.
