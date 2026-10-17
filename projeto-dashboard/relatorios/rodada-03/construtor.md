# Construtor — rodada 03

## Versão examinada

Sem commit (pasta sem Git). SHA-256 da entrega e da suíte preservada:

| Arquivo | SHA-256 |
|---|---|
| `projeto-dashboard/preparar_dados.py` | `C0FC3887AFF24BB31F84FA60FC40DC90472C43B7A71AFE831D03182E8BD8DAB0` |
| `projeto-dashboard/README.md` | `5DFFCE1FE33FD85E9E5DBDB74F3DCF55126C8CA5320ECE4DE3AE0596C9802995` |
| `projeto-dashboard/site/index.html` | `FFEE17D383465B705BF3842D521A3F19352A93FCAFF3D1F637878836D08FFB62` |
| `projeto-dashboard/site/estilos.css` | `EA17053B040D1130DFFC6741EC77CB21D039E00BCE6F5AF0263AB4C69F102A9F` |
| `projeto-dashboard/site/dashboard.js` | `D426E4B18697AB045799A713CAA3620134BAC4ED3902B9C858319D278E5ED9A1` |
| `projeto-dashboard/site/dados.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `projeto-dashboard/tests/test_dashboard.py` | `A36E9C9F427F5F472E262F85A61896B031E34FFFAAF1F2C13A8687A254839531` |

## Preservação conferida

| Arquivo mantido | SHA-256 |
|---|---|
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` | `543C97179CED2CE2C6BFDECA0693D19BC1BD4BA78A7BED7EAC7A33C7F1DD9930` |
| `resumo.md` | `88E8155BCF8DF341FCBC6BCC8FF9866D74B7F33450EB01C7696821F6386AD2A2` |
| `verificacao.md` | `0AD78DF5DF4A7C543900063C7EED05616D3DB916EA87EE2CA8945D7B5666A8AF` |
| `graficos.py` | `8ADD46A542DA318C077B8329F58929A5F6C8CDCAEAE8C33733E493FFB8471F59` |
| `cidades.png` | `DE0F1FA2B843064C7D95B9842B22DCDE0E272A8B1D1625366E9D9A996B9BEA36` |
| `categorias.png` | `CE9DF3F85C09354E2036BD6761D54BC9F3FC976D79D3BBD91FB1F7045B07E8CB` |

Relatórios/artefatos de rodadas anteriores preservados (SHA-256): `relatorios/FINAL.md` `685B459DF6769C037FF2BDEC292607DAEE83734DD2443FFD9483477FD3332331`; rodada 01 — `coordenador.md` `30A8E1B123D662DB865CA218226E1F538D3DCA3A2EBC3F1A5E56F701320B2418`, `construtor.md` `B12D0DB084842CC6AC8786A8F1B8CFC960E3D9B150113EC5841AA51A5FD09FA6`, `tester.md` `CFC832D9526736FA4E68B7B3FF09C0CB237DA97D4D82B6EB784FC77156D77F5A`, `revisor.md` `ADA99968C9107ABE02A1A82A0CD37E59D5DC0FF3468C0973431CFD506F0807E6`; rodada 02 — `construtor.md` `A7BFF492DCF72DB8129E6FA21FA5571B60533826C0461ADD012B736A7AE8350F`, `tester.md` `783BA7D5D0EF938CDDFF022DAD88F09B6F3B8CD2F978133E0E111F131F09FB55`, `revisor.md` `BB88FD8FD60E21AE55F26BB98BE21AB2A495B61F62BD4E3F2D7AA02F5E824801`.

## Alterações realizadas

- Reconstruído o pipeline pandas para validar o contrato das nove colunas, dados ausentes/texto vazio, IDs únicos, datas válidas, números finitos, quantidade inteira e `valor_venda = quantidade × preco_unitario`. O JSON é gravado atomicamente em UTF-8 em `site/dados.json`; o CSV limpo é somente lido.
- Reconstruídos HTML, CSS e JavaScript do dashboard estático, sem CDN: três KPIs explícitos (valor vendido, quantidade de vendas e ticket médio), gráfico comparativo por categoria, linha mensal, tabela e filtros cidade/categoria que atualizam todos os elementos. Inclui limpar, estado sem resultados, rótulos e foco por teclado, layout responsivo e mensagens em português.
- O JSON mantém os nove campos por registro. Cada linha é uma venda identificada por `id_venda`; não é contagem de unidades. A limpeza anterior permanece a descrita em `resumo.md` (duas duplicatas exatas removidas, espaços de cidade aparados, categorias padronizadas, pagamentos vazios preenchidos e `valor_venda` calculado). O projeto não deduplica nem modifica a base limpa. Não há custos para calcular lucro.
- A suíte existente foi mantida sem alterações. Nenhum CSV, imagem, análise ou relatório anterior foi editado.
- Os caminhos locais `.agents/skills/explore-data/SKILL.md`, `data-visualization/SKILL.md` e `validate-data/SKILL.md` não existem. As skills correspondentes disponíveis no harness foram consultadas; isso não substitui nem é apresentado como uso dos arquivos locais ausentes.

## Comandos executados, resultados e evidências

- `.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py` — **passou**; JSON gerado com 180 vendas e 9 colunas. Evidência: `projeto-dashboard/site/dados.json`.
- Smoke JSON com pandas e `json` — **passou**: 180 registros, nove colunas, 180 IDs únicos e total de R$ 20.059,00; comparado ao CSV limpo.
- `node --check .\projeto-dashboard\site\dashboard.js` — **passou**, sem erro sintático.
- Smoke HTTP local na porta 8766 — **passou**: `/`, `/dados.json`, `/dashboard.js` e `/estilos.css` responderam HTTP 200; JSON decodificado com 180 linhas.
- `.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v` — **12 testes descobertos; 9 passaram e 3 foram pulados; código de saída 0**. Passaram os testes de preservação/limpeza, exemplo conhecido, agregações independentes, pipeline, JSON, contrato DOM, referências, sintaxe JS e HTTP. Os três pulos são testes de browser.
- Ambiente conferido: módulos Playwright e Selenium ausentes; `chrome`, `msedge`, `chromium` e `firefox` não encontrados no PATH.

## Pendências e encaminhamento

- **PENDENTE/BLOQUEADO — interface em navegador:** filtros isolados e combinados, combinação vazia/limpar, sincronização interativa, ausência de erros no browser, responsividade real e teclado não foram executados com navegador. Próximo passo: disponibilizar Playwright e Chromium (ou navegador compatível) e repetir os testes.
- A ferramenta para delegar tester/revisor não está disponível nesta execução. Os relatórios independentes das rodadas anteriores foram preservados, mas a revisão independente desta nova versão ainda está **PENDENTE**; não simulei nova aprovação dos outros papéis.

## Status

**BLOQUEADO** para aprovação conjunta: pipeline, smoke checks e nove testes automatizados não-browser passaram; três testes de interface e a revisão independente da rodada 03 permanecem **PENDENTES**.
