# Dashboard de vendas de papelaria

## Escopo e métricas

Cada linha de `papelaria_limpa.csv` é uma venda identificada por `id_venda`. O painel mantém três KPIs de vendas: valor vendido (`quantidade × preco_unitario` somados), quantidade de vendas (linhas) e ticket médio (valor vendido dividido pelo número de vendas). Os gráficos usam os campos existentes `quantidade` e `data`: donut de **itens vendidos por categoria** e colunas de **itens vendidos por mês**. A legenda/fatia do donut seleciona a categoria e filtra o detalhamento e o gráfico mensal.

**Escopo autorizado:** o pedido anterior de mostrar “não vendidos” foi substituído, com autorização do usuário, por “itens vendidos”, pois este CSV contém somente vendas realizadas. A base não possui registros de não vendidos, estoque ou disponibilidade; nenhum campo foi inventado. Valor vendido não é lucro: custos e despesas não estão disponíveis.

O CSV limpo herda o tratamento documentado em `../resumo.md`: remoção de duas duplicatas exatamente iguais, espaços externos aparados em cidade, categorias padronizadas, quatro pagamentos vazios preenchidos como “Não informado” e cálculo de `valor_venda`. O pipeline pandas valida a base sem alterá-la e gera `site/dados.json` e os dados embutidos em `site/index.html`. São 180 vendas e 548 unidades vendidas, de 2026-01-01 a 2026-03-31.

## Preparar e testar

No PowerShell, na raiz do projeto (a pasta que contém `papelaria_limpa.csv`):

```powershell
.\.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py
.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v
```

Sem `.venv`, substitua `\.venv\Scripts\python.exe` por `python` e instale pandas, se necessário, com `python -m pip install pandas`.

## Abrir ou publicar

Após preparar os dados, abra `projeto-dashboard/site/index.html` com duplo clique no Explorador de Arquivos ou no VS Code. Alternativamente, execute na raiz:

```powershell
Start-Process .\projeto-dashboard\site\index.html
```

O painel abre por `file://`: os dados estão embutidos no HTML e não há `fetch`, XHR, CDN ou módulos. O seletor claro/escuro guarda a preferência em `localStorage` quando o navegador permite armazenamento local. A pasta `projeto-dashboard/site/` é a pasta publicável em hospedagem estática.

Para servir por HTTP local (opcional):

```powershell
.\.venv\Scripts\python.exe -m http.server 8000 --directory .\projeto-dashboard\site
```

Depois abra <http://localhost:8000>. A publicação não faz parte desta etapa.
