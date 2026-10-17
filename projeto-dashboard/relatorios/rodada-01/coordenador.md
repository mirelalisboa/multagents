# Coordenação — rodada 01

## Base e critérios registrados antes da construção

- Base solicitada: `papelaria_limpa.csv` (180 linhas, 9 colunas segundo `resumo.md` e `verificacao.md`).
- Arquivos anteriores a preservar: `vendas_papelaria.csv`, `papelaria_limpa.csv`, `resumo.md`, `verificacao.md`, `graficos.py`, `categorias.png` e `cidades.png`.
- SHA-256 de referência: `papelaria_limpa.csv` `543C97179CED2CE2C6BFDECA0693D19BC1BD4BA78A7BED7EAC7A33C7F1DD9930`; `vendas_papelaria.csv` `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF`; `resumo.md` `88E8155BCF8DF341FCBC6BCC8FF9866D74B7F33450EB01C7696821F6386AD2A2`; `verificacao.md` `0AD78DF5DF4A7C543900063C7EED05616D3DB916EA87EE2CA8945D7B5666A8AF`; `graficos.py` `8ADD46A542DA318C077B8329F58929A5F6C8CDCAEAE8C33733E493FFB8471F59`.
- Ambiente disponível no início: `.venv/Scripts/python.exe` Python 3.14.7, pandas instalado; módulos Python `playwright` e `selenium` não detectados.
- Os arquivos requeridos em `.agents/skills/explore-data/SKILL.md`, `.agents/skills/data-visualization/SKILL.md` e `.agents/skills/validate-data/SKILL.md` não foram encontrados nesse caminho. A ausência será mantida explícita; não se atribuirá uso desses arquivos locais.

## Critérios de aprovação

1. Criar nova entrega em `projeto-dashboard/` sem alterar base original nem resultados anteriores.
2. Preparar/reproduzir dados com Python e pandas; documentar granularidade, limpeza, métricas calculadas e limitações.
3. Criar dashboard estático com 3 indicadores pertinentes, 2 gráficos, tabela e 2 filtros existentes que atualizem os componentes em conjunto; incluir limpar filtros e estado vazio.
4. Garantir formatação monetária coerente, responsividade e acessibilidade básica, sem apresentar valor vendido como lucro.
5. Incluir README em português simples com comandos reais de preparação, teste e servidor HTTP local, identificando `site/` como pasta publicável.
6. Executar testes obrigatórios de dados, cálculos independentes, filtros, HTTP/JavaScript e interface. Testes não realizados permanecem **PENDENTES**; falta de browser deve ser relatada como bloqueio.
7. Concluir apenas com aprovação convergente de Construtor, Tester e Revisor sobre a mesma versão, sem pendências. Preservar relatórios por rodada e produzir `relatorios/FINAL.md`.

## Estado inicial

Construção e testes delegados a agentes separados. Aprovação final: **PENDENTE**.

## Conferência independente da base de entrada

- Comando: `@' ... '@ | .\\.venv\\Scripts\\python.exe -` com pandas, leitura de `papelaria_limpa.csv` em UTF-8-SIG.
- Resultado: 180 × 9; nenhuma célula ausente, nenhuma duplicata exata, nenhum `id_venda` duplicado; período 2026-01-01 a 2026-03-31.
- Oráculo inicial: 180 vendas; R$ 20.059,00 vendidos; ticket médio R$ 111,438888… (R$ 111,44); cidade: Campinas R$ 8.578,00, Santos R$ 6.937,50, Sorocaba R$ 4.543,50; categoria: Acessórios R$ 10.517,00, Livros R$ 7.438,00, Papelaria R$ 2.104,00.
- Estes valores são referências de conferência, não resultados finais de teste do dashboard.

## Conferência da documentação na entrega do Construtor

- Identifiquei um erro de comando em `README.md`: o comando HTTP está como `\.venv\Scripts\python.exe`; na raiz descrita no README, o caminho correto é `\.\venv\Scripts\python.exe` (PowerShell: `\.\venv` significa pasta `.venv` dentro da pasta atual). O Construtor deve corrigir o comando.
- O Tester também encontrou uma frase desatualizada no README dizendo que a suíte ainda não foi entregue. Correções documentais serão encaminhadas ao Construtor depois da execução da versão-base. Qualquer mudança exige nova suíte completa.
