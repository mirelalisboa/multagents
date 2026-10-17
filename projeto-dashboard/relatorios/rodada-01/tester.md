# Tester — rodada 01

## Versão examinada

Sem commit (pasta não Git). SHA-256 dos arquivos relevantes:

- `vendas_papelaria.csv`: `bf95b7609e30eb7e3e6a30cfc16e43d9fb5bdfc48a410e49148cceb92e2494ff`
- `papelaria_limpa.csv`: `543c97179ced2ce2c6bfdeca0693d19bc1bd4ba78a7bed7eac7a33c7f1dd9930`
- `projeto-dashboard/preparar_dados.py`: `6c8593f138bb003bf23b54e151c992da835764888eba341b5b4f90c7976b68f3`
- `projeto-dashboard/site/index.html`: `4a65103a926c4a4197e22824fff9043ef5cd1d4dda2a99b505683848a9e14993`
- `projeto-dashboard/site/dashboard.js`: `c6300b0699206108993d66634e9fb0e9a1785a9465561acd77b09ed6faf1a117`
- `projeto-dashboard/site/estilos.css`: `b2acfcce41f76a583ada800c724eaf635b2323009c57db8ce33d85dc28277a51`
- `projeto-dashboard/site/dados.json`: `65fe7740872b4820aa0cb93e366b440cea22c1660d6997f384046e7b9d1f421f`
- `projeto-dashboard/tests/test_dashboard.py`: `a36e9c9f427f5f472e262f85a61896b031e34fffaaf1f2c13a8687a254839531`

## Construído e conferido

- Criada a suíte reproduzível `projeto-dashboard/tests/test_dashboard.py`, usando `unittest` e bibliotecas padrão. O oráculo da limpeza é recalculado com `csv` e `Decimal`, sem importar nem chamar o código do Construtor.
- Conferidos: estrutura e preservação dos CSVs; 182 linhas originais, 180 linhas limpas, colunas, vazios, tipos/valores e duplicatas; transformação por registro; totais e agregações por categoria/cidade; exemplo conhecido; correspondência CSV/JSON; execução do pipeline e hashes do original/CSV limpo antes e depois.
- Conferidos no site: IDs acordados, rótulos acessíveis dos filtros, existência de referências locais, sintaxe do JavaScript via Node e resposta HTTP 200 para página e JSON.
- Foram preparados testes Playwright de filtros isolados/combinados, combinação sem dados, limpar, KPIs, tabela, gráficos, NaN/Infinity, dimensões pequena/grande e teclado. Eles **não foram executados**, conforme detalhado abaixo.

## Comandos e resultados

1. `.venv/Scripts/python.exe -m unittest discover -s projeto-dashboard/tests -v`
   - Resultado final: **12 testes descobertos; 9 passaram e 3 foram pulados**. Código de saída 0.
   - Os testes aprovados incluem pipeline, estrutura/limpeza, cálculos independentes, exemplo pequeno, JSON, DOM, referências/sintaxe JS e HTTP. Evidência reproduzível: este arquivo de teste e a saída do comando.
2. O teste HTTP iniciou um servidor local temporário e obteve HTTP 200 para `/`, `/index.html` e `/dados.json`; o JSON servido foi decodificado como array.
3. A execução do pipeline terminou com sucesso e não alterou `vendas_papelaria.csv` nem `papelaria_limpa.csv`. Seus hashes finais coincidem com os hashes-base registrados pelo coordenador.
4. Ambiente: Python 3.14.7, pandas 3.0.6 e Node.js disponível. `pytest`, `playwright` e `selenium` não estão instalados; nenhum executável Chrome, Edge ou Firefox foi encontrado.

## Problemas, pendências e encaminhamento

- **PENDENTE/BLOQUEADO — interface real:** os três testes de navegador foram pulados porque Playwright e um navegador não estão disponíveis. Assim, filtros funcionando no browser, KPIs/gráficos/tabela atualizados juntos, responsividade e teclado não foram verificados em execução real. Próximo passo: disponibilizar Playwright com Chromium (ou outro navegador acessível) e executar novamente a suíte. Não considerar a interface aprovada até lá.
- **Para o Construtor:** em `projeto-dashboard/README.md`, a frase que diz que “a suíte independente do tester” ainda não foi entregue ficou desatualizada; atualizar agora que `tests/test_dashboard.py` existe. Nenhuma alteração foi feita em arquivos de produto.
- As verificações de filtros e de correspondência interativa entre registros, KPIs, gráficos e tabela estão implementadas, mas permanecem **PENDENTES** junto dos testes de browser.

## Status

**BLOQUEADO** para aprovação da rodada: 9 testes automatizados não-browser passaram; 3 verificações obrigatórias de interface permanecem pendentes por falta de navegador. O status não equivale a aprovação conjunta do produto.
