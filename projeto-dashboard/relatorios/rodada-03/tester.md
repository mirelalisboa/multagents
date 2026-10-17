# Tester — rodada 03

## Versão examinada

Sem commit (diretório não Git). SHA-256 após a execução da suíte:

- `vendas_papelaria.csv`: `bf95b7609e30eb7e3e6a30cfc16e43d9fb5bdfc48a410e49148cceb92e2494ff`
- `papelaria_limpa.csv`: `543c97179ced2ce2c6bfdeca0693d19bc1bd4ba78a7bed7eac7a33c7f1dd9930`
- `projeto-dashboard/README.md`: `5dffce1fe33fd85e9e5dbdb74f3dcf55126c8ca5320ece4de3ae0596c9802995`
- `projeto-dashboard/preparar_dados.py`: `c0fc3887aff24bb31f84fa60fc40dc90472c43b7a71afe831d03182e8bd8dab0`
- `projeto-dashboard/site/index.html`: `ffee17d383465b705bf3842d521a3f19352a93fcaff3d1f637878836d08ffb62`
- `projeto-dashboard/site/dashboard.js`: `d426e4b18697ab045799a713caa3620134bac4ed3902b9c858319d278e5ed9a1`
- `projeto-dashboard/site/estilos.css`: `ea17053b040d1130dffc6741ec77cb21d039e00bce6f5af0263ab4c69f102a9f`
- `projeto-dashboard/site/dados.json`: `0cc873ce9c6e13a6f9dc1d4653c2ee22b5b444e471b07cebb98eaaf86a66d694`
- `projeto-dashboard/tests/test_dashboard.py`: `a36e9c9f427f5f472e262f85a61896b031e34fffaaf1f2c13a8687a254839531`

Os hashes dos dois CSVs correspondem aos registrados nas rodadas anteriores e na referência do coordenador. O teste de pipeline também conferiu os hashes antes/depois da geração do JSON; não houve alteração dos CSVs.

## Comando, resultados e evidências

Comando executado na raiz do projeto:

```powershell
.venv/Scripts/python.exe -m unittest discover -s projeto-dashboard/tests -v
```

Resultado: **12 testes descobertos; 9 aprovados e 3 pendentes/pulados**; código de saída 0. Evidências reproduzíveis: `projeto-dashboard/tests/test_dashboard.py`, saída deste comando e hashes acima.

Os 9 testes executados passaram, cobrindo:

- estrutura, preservação, regras de limpeza, valores ausentes e duplicatas nos CSVs;
- recálculos independentes dos totais e agrupamentos, além de exemplo pequeno conhecido;
- execução do pipeline sem modificar os CSVs e correspondência entre CSV e JSON;
- contrato de IDs e rótulos DOM;
- referências locais, sintaxe JavaScript via Node e HTTP do site/JSON.

O teste HTTP obteve 200 para `/`, `/index.html` e `/dados.json`, e decodificou a resposta JSON como array.

## Pendências e status

- **PENDENTE/BLOQUEADO — 3 testes de navegador:** Playwright e Selenium não estão instalados, e não foram encontrados Chrome, Chromium, Edge ou Firefox no PATH. Não foram executados os testes de filtros e sincronização interativa, nem os de responsividade e teclado. Próximo passo: disponibilizar Playwright com Chromium (ou navegador compatível) e executar novamente a suíte completa.
- Status do Tester: **BLOQUEADO** para aprovação integral. Os 9 testes não-browser passaram, mas os 3 testes de browser permanecem pendentes. Não constitui aprovação conjunta.
