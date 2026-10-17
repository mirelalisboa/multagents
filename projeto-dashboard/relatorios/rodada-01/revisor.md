# Relatório do Revisor — rodada 01

## Versão examinada

Sem commit (pasta sem Git). Hashes SHA-256 conferidos nesta revisão:

| Arquivo | SHA-256 |
|---|---|
| `projeto-dashboard/preparar_dados.py` | `6C8593F138BB003BF23B54E151C992DA835764888EBA341B5B4F90C7976B68F3` |
| `projeto-dashboard/README.md` | `528D8E1549FF701550BACB50D1852B284BF97AFC43A0A1C89E3F360E4F3285EA` |
| `projeto-dashboard/site/dados.json` | `65FE7740872B4820AA0CB93E366B440CEA22C1660D6997F384046E7B9D1F421F` |
| `projeto-dashboard/site/index.html` | `4A65103A926C4A4197E22824FFF9043EF5CD1D4DDA2A99B505683848A9E14993` |
| `projeto-dashboard/site/estilos.css` | `B2ACFCCE41F76A583ADA800C724EAF635B2323009C57DB8CE33D85DC28277A51` |
| `projeto-dashboard/site/dashboard.js` | `C6300B0699206108993D66634E9FB0E9A1785A9465561ACD77B09ED6FAF1A117` |
| `projeto-dashboard/tests/test_dashboard.py` | `A36E9C9F427F5F472E262F85A61896B031E34FFFAAF1F2C13A8687A254839531` |

Os hashes coincidem com os relatórios do Construtor e Tester. A execução da preparação nesta revisão regenerou o mesmo `dados.json`; não alterou os CSVs originais/limpos.

## O que foi conferido

- `preparar_dados.py`: valida as nove colunas, ausências, IDs, datas, tipos, positividade e `quantidade × preco_unitario`, sem chamar valor vendido de lucro.
- `dados.json`: conferência independente com PowerShell encontrou 180 registros, soma `valor_venda` de `20059` (R$ 20.059,00), cidades Campinas/Santos/Sorocaba e categorias Acessórios/Livros/Papelaria.
- `index.html`, CSS e JavaScript: existem três indicadores, dois gráficos SVG, tabela, dois filtros por colunas, limpeza, estado vazio, formatação pt-BR, `lang=pt-BR`, títulos hierárquicos, `label` associado aos selects, `scope=col`, `aria-live`, `role=status`, foco visível e layout responsivo declarado. A estrutura satisfaz os critérios estáticos; responsividade e interação visual real permanecem pendentes.
- Testes: os 9 testes não-browser passaram; os 3 testes reais de browser foram pulados por ausência de Playwright/navegador. Portanto, filtros isolados/combinados, atualização conjunta de KPIs/gráficos/tabela, seleção vazia, limpar, teclado, telas pequena/grande e ausência de erros JavaScript não têm evidência de execução real.
- Os arquivos locais das skills `explore-data`, `data-visualization` e `validate-data` previstos no `AGENTS.md` não existem nesta pasta; não afirmo uso dessas skills. O Construtor registrou a mesma limitação.

## Comandos executados e evidências

- `.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v` — **12 descobertos: 9 OK e 3 skipped**, saída 0. Evidência na saída do terminal e em `relatorios/rodada-01/tester.md`.
- `.\.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py` — passou; gerou 180 vendas/9 colunas.
- `node --check .\projeto-dashboard\site\dashboard.js` — passou.
- `Get-FileHash ... -Algorithm SHA256` — hashes acima.
- Conferência independente do JSON com `ConvertFrom-Json`/`Measure-Object` — 180 linhas e soma 20059.
- Comando HTTP exatamente como documentado no README, `\.venv\Scripts\python.exe -m http.server 8000 --directory .\projeto-dashboard\site` — **falhou** no PowerShell: o caminho `\.venv\Scripts\python.exe` não existe. O comando correto é `..\.venv\Scripts\python.exe`? Não: é **`.\.venv\Scripts\python.exe`** (um ponto antes da barra).

## Problemas e encaminhamento

1. **Construtor — correção necessária no README:** a linha 14 usa `\.venv\Scripts\python.exe`, diferente dos comandos anteriores, e não inicia o servidor em um ambiente normal. Substituir por `.\.venv\Scripts\python.exe`. A linha 17 também afirma que a suíte do tester “ainda [não] foi entregue”, mas `tests/test_dashboard.py` já existe; atualizar essa documentação.
2. **Tester/ambiente — pendência obrigatória:** instalar Playwright e um navegador Chromium (ou disponibilizar navegador equivalente) e executar novamente os três testes browser. Teste pulado não é aprovação.
3. Não encontrei defeito reproduzível nos cálculos, no pipeline, nas referências locais, na sintaxe JavaScript ou no contrato DOM estático. A revisão visual/interativa em navegador não pôde ser concluída por bloqueio do ambiente.

## Status

**BLOQUEADO** — a base, os cálculos, o pipeline e os 9 testes não-browser passaram, mas há um comando real incorreto no README e os 3 testes obrigatórios de interface estão pendentes por ausência de Playwright/navegador. Encaminhar a correção do README ao Construtor e repetir toda a suíte/revisão após a execução browser. Não é **APROVADO**.
