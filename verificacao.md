# Verificação da análise de vendas de papelaria

## Resultado geral: pronto para compartilhar, com definição da métrica explícita

Recalculei os resultados diretamente de `vendas_papelaria.csv` e `papelaria_limpa.csv` usando `.venv/Scripts/python.exe`, sem usar os totais impressos por `graficos.py` como fonte dos cálculos. Comparei também cada linha limpa com uma transformação independente do original.

## Contagens e total vendido

- Original: **182 linhas de dados** e 8 colunas.
- Cópia limpa: **180 linhas**, 9 colunas e **180 `id_venda` únicos**. Portanto, há 180 vendas após remover as 2 linhas duplicadas exatas.
- Soma da coluna `quantidade` na cópia: **548 unidades**. Esse número conta itens, não vendas; a contagem de vendas é 180.
- Total vendido recalculado na cópia: **R$ 20.059,00**, pela soma de `quantidade × preco_unitario`.
- Como verificação do efeito da deduplicação, o cálculo bruto no original, antes de excluir as duplicatas, seria **R$ 20.066,00**. A diferença de R$ 7,00 não deve ser incluída no total limpo.

## Conferência das agregações

| Categoria | Valor vendido |
|---|---:|
| Acessórios | R$ 10.517,00 |
| Livros | R$ 7.438,00 |
| Papelaria | R$ 2.104,00 |
| **Soma por categoria** | **R$ 20.059,00** |

A soma por categoria coincide exatamente com o total geral (**R$ 20.059,00**). Como conferência adicional, os totais por cidade também somam R$ 20.059,00: Campinas R$ 8.578,00; Santos R$ 6.937,50; Sorocaba R$ 4.543,50.

## Revisão dos arquivos e do método

- `papelaria_limpa.csv`: as 180 linhas correspondem, campo a campo, ao resultado esperado após remover apenas duplicatas exatas, aparar espaços em `cidade`, padronizar as categorias e preencher pagamentos vazios. Recalculei `valor_venda` por linha e não encontrei divergências.
- Duplicatas: as 2 linhas removidas repetiam os IDs `V0010` e `V0020`; não há registros conflitantes com o mesmo ID.
- `resumo.md`: contagens, total de R$ 20.059,00, média de R$ 111,44 por linha e frequências por categoria estão consistentes com o recálculo. A média é o total dividido por 180 vendas.
- `graficos.py`: lê `papelaria_limpa.csv`, converte `valor_venda` em número e soma essa coluna agrupando separadamente por `categoria` e por `cidade`. Os gráficos usam eixo iniciado em zero e rótulos em reais.
- O código e as conclusões descrevem **valor vendido**, não lucro. Não há dados de custos ou despesas para calcular lucro.

## Conclusão

Não encontrei erro nos totais, contagens, agregações ou na base usada pelo código dos gráficos. Para evitar ambiguidade, esta verificação distingue **180 vendas** de **548 unidades vendidas**. O total de R$ 20.059,00 refere-se à cópia deduplicada; o total bruto do original inclui duplicatas exatas.
