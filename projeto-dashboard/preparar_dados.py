"""Valida o CSV limpo e atualiza os dados estáticos do dashboard."""

from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "papelaria_limpa.csv"
SITE = ROOT / "site"
JSON_DESTINATION = SITE / "dados.json"
HTML_DESTINATION = SITE / "index.html"
EXPECTED_COLUMNS = [
    "id_venda",
    "data",
    "cidade",
    "categoria",
    "produto",
    "quantidade",
    "preco_unitario",
    "forma_pagamento",
    "valor_venda",
]
START_MARKER = "<!-- INLINE_DATA_START -->"
END_MARKER = "<!-- INLINE_DATA_END -->"


def write_atomically(destination: Path, content: str) -> None:
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=destination.parent,
        prefix=destination.stem + "-",
        suffix=".tmp",
        delete=False,
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)
    try:
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def prepare() -> int:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"CSV limpo não encontrado: {SOURCE}")
    if not HTML_DESTINATION.is_file():
        raise FileNotFoundError(f"Modelo HTML não encontrado: {HTML_DESTINATION}")

    data = pd.read_csv(SOURCE, encoding="utf-8-sig")
    if list(data.columns) != EXPECTED_COLUMNS:
        raise ValueError(f"Colunas inesperadas: {list(data.columns)}")
    if data.empty:
        raise ValueError("O CSV limpo não contém vendas.")
    if data[EXPECTED_COLUMNS].isna().any().any():
        raise ValueError("O CSV contém valores ausentes em colunas obrigatórias.")

    text_columns = ["id_venda", "cidade", "categoria", "produto", "forma_pagamento"]
    for column in text_columns:
        if data[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"A coluna {column} contém texto vazio.")
    if data["id_venda"].duplicated().any():
        raise ValueError("Há id_venda repetido no CSV limpo.")

    data["data"] = pd.to_datetime(data["data"], format="%Y-%m-%d", errors="raise")
    for column in ("quantidade", "preco_unitario", "valor_venda"):
        data[column] = pd.to_numeric(data[column], errors="raise")
        if not data[column].map(math.isfinite).all():
            raise ValueError(f"A coluna {column} contém número não finito.")
    if not (data["quantidade"] % 1 == 0).all() or (data["quantidade"] <= 0).any():
        raise ValueError("Quantidade deve ser um inteiro positivo.")
    if (data["preco_unitario"] < 0).any():
        raise ValueError("Preço unitário não pode ser negativo.")
    if not (data["valor_venda"] == data["quantidade"] * data["preco_unitario"]).all():
        raise ValueError("valor_venda deve ser igual a quantidade × preco_unitario.")

    data["data"] = data["data"].dt.strftime("%Y-%m-%d")
    data["quantidade"] = data["quantidade"].astype("int64")
    records = data[EXPECTED_COLUMNS].to_dict(orient="records")
    json_text = json.dumps(records, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    # Escapa caracteres especiais de HTML raw-text sem alterar o conteúdo do JSON.
    inline_json = (
        json.dumps(records, ensure_ascii=False, indent=2, allow_nan=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )

    html = HTML_DESTINATION.read_text(encoding="utf-8")
    if html.count(START_MARKER) != 1 or html.count(END_MARKER) != 1:
        raise ValueError("O HTML precisa conter exatamente os dois marcadores de dados inline.")
    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    replacement = (
        START_MARKER
        + '\n  <script type="application/json" id="dashboard-data">\n'
        + inline_json
        + "\n  </script>\n"
        + END_MARKER
    )
    html, replacements = re.subn(pattern, lambda _: replacement, html, count=1, flags=re.DOTALL)
    if replacements != 1:
        raise ValueError("Não foi possível atualizar os dados inline do HTML.")

    # Mantém dados.json como saída útil para conferência e outras ferramentas;
    # o dashboard não o requisita e funciona mesmo quando aberto por file://.
    write_atomically(JSON_DESTINATION, json_text)
    write_atomically(HTML_DESTINATION, html)
    print(f"Atualizados {len(records)} registros em dados.json e index.html (dados embutidos).")
    return len(records)


if __name__ == "__main__":
    prepare()
