"""Gera gráficos de valor vendido por categoria e por cidade."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "papelaria_limpa.csv"


def formatar_reais(
    valor: float, _posicao: int | None = None, *, centavos: bool = False
) -> str:
    """Formata valores no padrão monetário brasileiro."""
    casas_decimais = 2 if centavos else 0
    formatado = f"{valor:,.{casas_decimais}f}"
    formatado = formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatado}"


def criar_grafico(coluna: str, titulo: str, arquivo_saida: str) -> pd.Series:
    totais = dados.groupby(coluna, sort=True)["valor_venda"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    barras = ax.bar(
        totais.index,
        totais.values,
        color="#4C72B0",
        width=0.65,
        zorder=3,
    )

    ax.set_title(titulo, fontsize=15, fontweight="bold", pad=16)
    ax.text(
        0.5,
        1.01,
        "Soma de quantidade × preço unitário; valor vendido não é lucro",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=10,
        color="#4A4A4A",
    )
    ax.set_xlabel(coluna.capitalize(), labelpad=10)
    ax.set_ylabel("Valor total vendido (R$)")
    ax.set_ylim(0, max(totais.values) * 1.18)
    ax.yaxis.set_major_formatter(FuncFormatter(formatar_reais))
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for barra, valor in zip(barras, totais.values):
        ax.annotate(
            formatar_reais(valor, centavos=True),
            (barra.get_x() + barra.get_width() / 2, barra.get_height()),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(BASE_DIR / arquivo_saida, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return totais


dados = pd.read_csv(ARQUIVO_DADOS, encoding="utf-8-sig")
dados["valor_venda"] = pd.to_numeric(dados["valor_venda"], errors="raise")

totais_categoria = criar_grafico(
    "categoria", "Valor total vendido por categoria", "categorias.png"
)
totais_cidade = criar_grafico(
    "cidade", "Valor total vendido por cidade", "cidades.png"
)

print("Totais por categoria (R$):")
print(totais_categoria.to_string())
print("\nTotais por cidade (R$):")
print(totais_cidade.to_string())
print("\nGráficos salvos em categorias.png e cidades.png.")
