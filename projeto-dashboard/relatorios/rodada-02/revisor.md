# Relatório do Revisor — rodada 02

## Versão examinada

Sem commit (pasta sem Git). Hashes SHA-256 conferidos:

| Arquivo | SHA-256 |
|---|---|
| `projeto-dashboard/README.md` | `5DFFCE1FE33FD85E9E5DBDB74F3DCF55126C8CA5320ECE4DE3AE0596C9802995` |
| `projeto-dashboard/preparar_dados.py` | `6C8593F138BB003BF23B54E151C992DA835764888EBA341B5B4F90C7976B68F3` |
| `projeto-dashboard/site/dados.json` | `65FE7740872B4820AA0CB93E366B440CEA22C1660D6997F384046E7B9D1F421F` |
| `projeto-dashboard/site/index.html` | `4A65103A926C4A4197E22824FFF9043EF5CD1D4DDA2A99B505683848A9E14993` |
| `projeto-dashboard/site/estilos.css` | `B2ACFCCE41F76A583ADA800C724EAF635B2323009C57DB8CE33D85DC28277A51` |
| `projeto-dashboard/site/dashboard.js` | `C6300B0699206108993D66634E9FB0E9A1785A9465561ACD77B09ED6FAF1A117` |
| `projeto-dashboard/tests/test_dashboard.py` | `A36E9C9F427F5F472E262F85A61896B031E34FFFAAF1F2C13A8687A254839531` |

O `README.md` é o único arquivo de produto alterado desde a rodada 01. O relatório `rodada-02/tester.md` não estava disponível nesta revisão; foi considerado o relatório `rodada-02/construtor.md` e a execução local da suíte.

## Conferências e achados

- O comando HTTP documentado agora está correto: `..\.venv` não é usado; a linha 14 contém `.\.venv\Scripts\python.exe -m http.server 8000 --directory .\projeto-dashboard\site`. A forma equivalente executada nesta revisão serviu a página com **HTTP 200** e 4.299 bytes.
- A frase antiga sobre a suíte ainda não ter sido entregue foi removida. O README agora identifica `projeto-dashboard/tests/test_dashboard.py` e o comando de execução.
- A preparação continua consistente: 180 registros, nove colunas, IDs únicos e `dados.json` com soma independente de `valor_venda` igual a `20059` (R$ 20.059,00). Os hashes do pipeline, site, dados e testes permanecem iguais aos da rodada 01.
- A estrutura estática permanece consistente com os critérios: três indicadores, dois gráficos, tabela, dois filtros, limpeza, estado vazio, formatação monetária e documentação de que valor vendido não é lucro. Não foram encontradas mudanças que invalidem os cálculos ou referências locais.

## Comandos executados e evidências

1. `.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v` — **12 testes descobertos; 9 passaram e 3 foram pulados; código de saída 0**. Os três pulos são os testes reais de browser por ausência de Playwright/navegador.
2. Servidor equivalente ao README com `.\.venv\Scripts\python.exe -m http.server 18765 --directory .\projeto-dashboard\site`, seguido de `Invoke-WebRequest http://127.0.0.1:18765/` — **HTTP=200; BYTES=4299**.
3. `Get-FileHash ... -Algorithm SHA256` — hashes registrados acima.
4. Conferência independente de `site/dados.json` com `ConvertFrom-Json`/`Measure-Object` — `rows=180; sum=20059; ids=180`.

## Pendências e encaminhamento

- **Tester/ambiente:** `rodada-02/tester.md` não foi entregue/disponibilizado, portanto a evidência independente formal do Tester desta rodada está pendente.
- **Interface real:** os três testes browser continuam pulados. Ainda não há evidência de execução real para filtros isolados/combinados, atualização conjunta de indicadores/gráficos/tabela, seleção vazia, limpar, responsividade, teclado e ausência de erros no navegador. Disponibilizar Playwright com navegador e executar a suíte completa.

## Status

**BLOQUEADO** — README corrigido e executável, documentação da suíte atualizada, cálculos/site consistentes e 9 testes não-browser aprovados. Os 3 testes reais de browser continuam pendentes; portanto não é possível declarar **APROVADO**.
