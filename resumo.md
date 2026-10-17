# Análise e tratamento — vendas de papelaria

## Estrutura do arquivo original
- Linhas de dados: **182** (mais o cabeçalho).
- Colunas: **8** — id_venda, data, cidade, categoria, produto, quantidade, preco_unitario, forma_pagamento.
- Granularidade: uma linha por venda; `id_venda` identifica a venda.
- Período em `data`: **2026-01-01 a 2026-03-31**.
- Codificação da origem: UTF-8; a cópia foi gravada em UTF-8 com BOM.

## Problemas encontrados

- 2 linhas duplicadas exatamente (todos os campos iguais); excluídas somente da cópia limpa.
- 6 cidades com espaços no início/fim; removidos na cópia.
- Variação de maiúsculas/minúsculas em categoria: Acessórios (62), Livros (54), Papelaria (63), acessórios (3)
- 4 pagamentos vazios; preenchidos com “Não informado” na cópia.
- 2 id(s) repetidos no original, todos explicados por duplicatas exatas; não há conflitos de conteúdo por id.

### Perfil de completude do original

| Coluna | Vazios/em branco | Valores distintos |
|---|---:|---:|
| `id_venda` | 0 | 180 |
| `data` | 0 | 90 |
| `cidade` | 0 | 6 |
| `categoria` | 0 | 4 |
| `produto` | 0 | 6 |
| `quantidade` | 0 | 5 |
| `preco_unitario` | 0 | 6 |
| `forma_pagamento` | 4 | 4 |

## Tratamento aplicado em `papelaria_limpa.csv`

- O original `vendas_papelaria.csv` foi preservado.
- Removidas **2** duplicatas exatas, comparando os valores em todas as 8 colunas originais. Registros com mesmo `id_venda` e conteúdo distinto seriam mantidos; não foram encontrados conflitos desse tipo.
- Removidos espaços no início/fim dos valores de `cidade`.
- Padronizadas categorias para `Livros`, `Papelaria` e `Acessórios` (valores inesperados, se existentes, são preservados).
- Substituídos 4 valores vazios de `forma_pagamento` por `Não informado`.
- Adicionada `valor_venda`, calculada como `quantidade * preco_unitario` com aritmética decimal.
- Resultado: **180 linhas e 9 colunas**.

## Resumo após o tratamento

- Soma de `valor_venda`: **20059.0**.
- Média de `valor_venda` por venda/linha: **111.44**.
- Quantidade por categoria:
  - Acessórios: 65
  - Livros: 54
  - Papelaria: 61

## Escopo

- Usado somente o CSV local e o interpretador `.venv/Scripts/python.exe`; nenhuma integração com banco de dados foi utilizada.
