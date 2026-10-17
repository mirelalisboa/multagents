# Tester — rodada 04

## Versão examinada

Sem commit (diretório não Git). SHA-256 conferidos após executar a suíte:

- `vendas_papelaria.csv`: `bf95b7609e30eb7e3e6a30cfc16e43d9fb5bdfc48a410e49148cceb92e2494ff`
- `papelaria_limpa.csv`: `543c97179ced2ce2c6bfdeca0693d19bc1bd4ba78a7bed7eac7a33c7f1dd9930`
- `projeto-dashboard/README.md`: `41ff68f4acb6d2ba3d45995fb2f73d4b86ad97cfd38a5ee66b3a673284571dd9`
- `projeto-dashboard/preparar_dados.py`: `030680e4bab5b65998bf7d124f47db5e1b7709c726ef4c8da7be287d3b21dc41`
- `projeto-dashboard/site/index.html`: `2e5207e5607048a91626cba18c8331483ae14b7d950d7ad98fd906332de88a08`
- `projeto-dashboard/site/estilos.css`: `01699c2c21144c7c302850a7ff324c56c06ce4c9c5bcb2f8d028adfb6b20f4cc`
- `projeto-dashboard/site/dashboard.js`: `2279f2050dd2ba52c8c6480a7ec9def4a0affeaa136bc0bb3f184e85ff432de4`
- `projeto-dashboard/site/dados.json`: `0cc873ce9c6e13a6f9dc1d4653c2ee22b5b444e471b07cebb98eaaf86a66d694`
- `projeto-dashboard/tests/test_dashboard.py`: `72b65821d54804a8b0f1371b4333a317a7b77d80c08a00588c85e18fdd922508`

Os hashes dos CSVs conferem com os da rodada anterior e com a referência registrada pelo Construtor. O teste do pipeline também confirmou que os arquivos de origem não mudam durante a preparação.

## Comandos, resultados e evidências

Executado da raiz do projeto:

```powershell
.venv/Scripts/python.exe -m unittest discover -s projeto-dashboard/tests -v
```

Resultado: **14 testes descobertos; 10 passaram e 4 foram pulados**. A execução terminou com código de saída 0. Os quatro pulos são os testes que requerem browser; estão pendentes, não aprovados.

Conferências cobertas pelos testes que passaram:

- preservação e estrutura dos CSVs, regras de limpeza, tipos, valores ausentes e duplicatas;
- recálculos independentes de totais/agrupamentos e exemplo pequeno conhecido;
- execução do pipeline e correspondência do JSON com o CSV, inclusive payload embutido no HTML;
- HTML autocontido e sem dependências de rede/recursos incompatíveis com abertura local;
- contrato DOM e referências de arquivos locais;
- carregamento por HTTP; `/`, `/index.html` e `/dados.json` responderam HTTP 200 e o JSON foi decodificado;
- sintaxe de `dashboard.js`.

Verificação adicional executada:

```powershell
node --check projeto-dashboard/site/dashboard.js
```

Resultado: passou, sem erro sintático (Node.js v24.21.0). Evidências reproduzíveis: `projeto-dashboard/tests/test_dashboard.py`, saída dos comandos acima e hashes registrados neste relatório.

## Pendências e status

- **PENDENTE/BLOQUEADO — 4 testes de browser:** abertura real via `file://`, filtros e atualização interativa de KPIs/gráficos/tabela, responsividade e navegação por teclado não foram executados. O ambiente não tem módulos Python Playwright/Selenium e não tem `chrome`, `chromium`, `msedge` ou `firefox` no PATH. Próximo passo: disponibilizar Playwright com Chromium (ou navegador compatível) e repetir a suíte completa.
- Não foram encontrados defeitos nos 10 testes executados. Nenhuma alteração foi feita em produto ou CSVs; relatórios anteriores não foram editados.
- Status do Tester: **BLOQUEADO** para aprovação. As verificações estáticas/HTTP passaram, mas a validação real da interface permanece pendente. **Não é aprovação conjunta.**
