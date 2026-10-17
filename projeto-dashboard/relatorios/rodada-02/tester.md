# Tester — rodada 02

## Versão examinada

Sem commit (diretório não Git). SHA-256 da versão testada:

- `vendas_papelaria.csv`: `bf95b7609e30eb7e3e6a30cfc16e43d9fb5bdfc48a410e49148cceb92e2494ff`
- `papelaria_limpa.csv`: `543c97179ced2ce2c6bfdeca0693d19bc1bd4ba78a7bed7eac7a33c7f1dd9930`
- `projeto-dashboard/README.md`: `5dffce1fe33fd85e9e5dbdb74f3dcf55126c8ca5320ece4de3ae0596c9802995`
- `projeto-dashboard/preparar_dados.py`: `6c8593f138bb003bf23b54e151c992da835764888eba341b5b4f90c7976b68f3`
- `projeto-dashboard/site/index.html`: `4a65103a926c4a4197e22824fff9043ef5cd1d4dda2a99b505683848a9e14993`
- `projeto-dashboard/site/dashboard.js`: `c6300b0699206108993d66634e9fb0e9a1785a9465561acd77b09ed6faf1a117`
- `projeto-dashboard/site/estilos.css`: `b2acfcce41f76a583ada800c724eaf635b2323009c57db8ce33d85dc28277a51`
- `projeto-dashboard/site/dados.json`: `65fe7740872b4820aa0cb93e366b440cea22c1660d6997f384046e7b9d1f421f`
- `projeto-dashboard/tests/test_dashboard.py`: `a36e9c9f427f5f472e262f85a61896b031e34fffaaf1f2c13a8687a254839531`

Os hashes dos CSVs são iguais aos registrados na rodada 01 e à referência do coordenador. Os hashes do pipeline, site e JSON também permanecem iguais aos da rodada 01; a alteração de documentação não alterou produto nem dados. O README tem hash atualizado.

## Conferências e resultados

- Reexecutada a suíte completa de dados e dashboard: preservação/estrutura das bases, regras de limpeza, duplicatas, tipos e valores, recálculo independente de totais e agrupamentos, exemplo de resultado conhecido, JSON, execução do pipeline, contrato DOM, referências de arquivos, sintaxe JavaScript e carregamento HTTP.
- O pipeline terminou com sucesso. Os hashes de `vendas_papelaria.csv` e `papelaria_limpa.csv`, medidos após a execução, continuam iguais aos hashes-base.
- O site e `dados.json` responderam HTTP 200 para `/`, `/index.html` e `/dados.json`; o JSON servido foi decodificado como array.

## Comando e evidência

Comando executado na raiz:

```powershell
.venv/Scripts/python.exe -m unittest discover -s projeto-dashboard/tests -v
```

Resultado: **12 testes descobertos; 9 aprovados e 3 pendentes/pulados**. A suíte terminou com código de saída 0, mas a interface não está integralmente validada. Evidências reproduzíveis: `projeto-dashboard/tests/test_dashboard.py`, saída da execução acima e hashes listados neste relatório.

## Pendências e status

- **PENDENTE — interação real no navegador (3 testes):** a suíte indicou Playwright/navegador não instalado. Permanecem sem execução as verificações interativas de filtros isolados e combinados, seleção sem resultados e limpar; consistência interativa de KPIs, gráficos e tabela; NaN/Infinity na interface; responsividade em telas pequena/grande e uso por teclado. Próximo passo: disponibilizar Playwright com navegador Chromium (ou navegador compatível) e repetir a suíte completa.
- Não foram encontrados defeitos nos 9 testes executados. Nenhuma alteração foi feita no produto ou nos dados.
- Status desta rodada: **BLOQUEADO** para aprovação da interface. **Não é aprovação conjunta**; os testes de navegador continuam pendentes.
