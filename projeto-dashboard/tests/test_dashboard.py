"""Testes de regressão independentes para a análise e o dashboard da papelaria.

Execute da raiz do repositório com:
    .venv/Scripts/python.exe -m unittest discover -s projeto-dashboard/tests -v

Os cálculos de referência usam apenas csv/decimal da biblioteca padrão, não o
código de preparação do produto. Os testes de navegador são opcionais quando
Playwright e um navegador estão instalados; a ausência deles deve ser reportada
como pendência, nunca como aprovação da interface.
"""

from __future__ import annotations

import csv
import hashlib
import http.server
import json
import os
import re
import shutil
import subprocess
import threading
import unittest
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "projeto-dashboard"
SITE = PROJECT / "site"
RAW_CSV = ROOT / "vendas_papelaria.csv"
CLEAN_CSV = ROOT / "papelaria_limpa.csv"
JSON_DATA = SITE / "dados.json"
INDEX = SITE / "index.html"
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
DOM_IDS = [
    "filtro-cidade",
    "filtro-categoria",
    "limpar-filtros",
    "voltar-visao-geral",
    "alternar-tema",
    "kpi-total",
    "kpi-vendas",
    "kpi-ticket",
    "estado-vazio",
    "corpo-tabela",
    "grafico-categoria",
    "grafico-tempo",
    "legenda-categoria",
    "categoria-ativa",
]
PIPELINE_CANDIDATES = [
    PROJECT / "preparar_dados.py",
    PROJECT / "prepare_data.py",
    PROJECT / "scripts" / "preparar_dados.py",
    PROJECT / "scripts" / "prepare_data.py",
]


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def _expected_clean_rows() -> list[dict[str, str]]:
    """Reproduz as regras documentadas usando registros e Decimal."""
    _, original = _read_csv(RAW_CSV)
    seen: set[tuple[str, ...]] = set()
    expected: list[dict[str, str]] = []
    category_names = {
        "livros": "Livros",
        "papelaria": "Papelaria",
        "acessórios": "Acessórios",
        "acessorios": "Acessórios",
    }
    for source in original:
        exact_record = tuple(source.get(key, "") or "" for key in source)
        if exact_record in seen:
            continue
        seen.add(exact_record)
        row = dict(source)
        row["cidade"] = row["cidade"].strip()
        category_key = row["categoria"].strip().casefold()
        row["categoria"] = category_names.get(category_key, row["categoria"])
        if not row["forma_pagamento"].strip():
            row["forma_pagamento"] = "Não informado"
        quantity = int(row["quantidade"])
        price = Decimal(row["preco_unitario"])
        row["valor_venda"] = format(Decimal(quantity) * price, "f")
        expected.append(row)
    return expected


def _decimal(value: object) -> Decimal:
    return Decimal(str(value))


def _contrast_ratio(foreground: str, background: str) -> float:
    def luminance(color: str) -> float:
        channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def format_integer_pt(value: int) -> str:
    return f"{value:,}".replace(",", ".")


class ProductFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RAW_CSV.is_file():
            raise unittest.SkipTest(f"CSV original ausente: {RAW_CSV}")
        cls.raw_columns, cls.raw_rows = _read_csv(RAW_CSV)
        cls.product_available = CLEAN_CSV.is_file() and JSON_DATA.is_file() and INDEX.is_file()
        cls.clean_columns: list[str] = []
        cls.clean_rows: list[dict[str, str]] = []
        cls.site_rows: list[dict[str, object]] = []
        if cls.product_available:
            cls.clean_columns, cls.clean_rows = _read_csv(CLEAN_CSV)
            cls.site_rows = json.loads(JSON_DATA.read_text(encoding="utf-8"))

    def require_product(self) -> None:
        if not self.product_available:
            self.skipTest("PENDENTE: produto ainda não entregue em projeto-dashboard/")

    def test_preserva_csv_original_e_sua_estrutura(self) -> None:
        self.assertEqual(len(self.raw_rows), 182)
        self.assertEqual(
            self.raw_columns,
            EXPECTED_COLUMNS[:-1],
            "O original deve continuar com as oito colunas de origem",
        )
        self.assertEqual(len({row["id_venda"] for row in self.raw_rows}), 180)
        self.assertEqual(sum(1 for row in self.raw_rows if not row["forma_pagamento"].strip()), 4)

    def test_csv_limpo_confere_com_regras_documentadas(self) -> None:
        self.require_product()
        self.assertEqual(self.clean_columns, EXPECTED_COLUMNS)
        self.assertEqual(len(self.clean_rows), 180)
        self.assertEqual(len({row["id_venda"] for row in self.clean_rows}), 180)
        for row_number, row in enumerate(self.clean_rows, start=2):
            for column in EXPECTED_COLUMNS:
                self.assertTrue(row[column].strip(), f"Campo vazio: {column}, linha {row_number}")
            self.assertGreaterEqual(int(row["quantidade"]), 1)
            self.assertGreaterEqual(_decimal(row["preco_unitario"]), 0)
            self.assertEqual(
                _decimal(row["valor_venda"]),
                int(row["quantidade"]) * _decimal(row["preco_unitario"]),
                f"valor_venda incorreto na linha {row_number}",
            )

        # Compara linha a linha com transformação independente do CSV de origem.
        expected = _expected_clean_rows()
        self.assertEqual(len(expected), len(self.clean_rows))
        expected_by_id = {row["id_venda"]: row for row in expected}
        for actual in self.clean_rows:
            reference = expected_by_id[actual["id_venda"]]
            for column in EXPECTED_COLUMNS:
                self.assertEqual(
                    actual[column],
                    reference[column],
                    f"Divergência em {column}, id {actual['id_venda']}",
                )
        self.assertEqual(Counter(row["forma_pagamento"] for row in self.clean_rows)["Não informado"], 4)

    def test_totais_e_agrupamentos_recalculados_independentemente(self) -> None:
        self.require_product()
        amounts = [_decimal(row["valor_venda"]) for row in self.clean_rows]
        self.assertEqual(sum(amounts, Decimal(0)), Decimal("20059"))
        self.assertEqual(len(amounts), 180)
        by_category: dict[str, Decimal] = defaultdict(Decimal)
        by_city: dict[str, Decimal] = defaultdict(Decimal)
        for row in self.clean_rows:
            by_category[row["categoria"]] += _decimal(row["valor_venda"])
            by_city[row["cidade"]] += _decimal(row["valor_venda"])
        self.assertEqual(
            by_category,
            {"Acessórios": Decimal("10517"), "Livros": Decimal("7438"), "Papelaria": Decimal("2104")},
        )
        self.assertEqual(
            by_city,
            {"Campinas": Decimal("8578"), "Santos": Decimal("6937.5"), "Sorocaba": Decimal("4543.5")},
        )
        self.assertEqual(sum(by_category.values(), Decimal(0)), sum(amounts, Decimal(0)))

    def test_exemplo_pequeno_com_resultado_conhecido(self) -> None:
        # Caso de referência feito à mão; não chama nem replica função do produto.
        example = [(2, Decimal("12.50")), (1, Decimal("8")), (3, Decimal("4"))]
        line_values = [quantity * price for quantity, price in example]
        self.assertEqual(line_values, [Decimal("25.00"), Decimal("8"), Decimal("12")])
        self.assertEqual(sum(line_values), Decimal("45.00"))
        self.assertEqual(len(line_values), 3)
        self.assertEqual(sum(line_values) / len(line_values), Decimal("15.00"))

    def test_json_publicado_corresponde_aos_dados_preparados(self) -> None:
        self.require_product()
        self.assertIsInstance(self.site_rows, list)
        self.assertEqual(len(self.site_rows), len(self.clean_rows))
        self.assertEqual(set(self.site_rows[0]), set(EXPECTED_COLUMNS))
        by_id = {row["id_venda"]: row for row in self.clean_rows}
        for record in self.site_rows:
            self.assertEqual(set(record), set(EXPECTED_COLUMNS))
            source = by_id[record["id_venda"]]
            for column in EXPECTED_COLUMNS:
                if column == "quantidade":
                    self.assertEqual(int(record[column]), int(source[column]))
                elif column in {"preco_unitario", "valor_venda"}:
                    self.assertEqual(_decimal(record[column]), _decimal(source[column]))
                else:
                    self.assertEqual(str(record[column]), source[column])
        self.assertEqual(
            sum((_decimal(row["valor_venda"]) for row in self.site_rows), Decimal(0)),
            Decimal("20059"),
        )

    def test_pipeline_reproduz_dados_e_nao_altera_original(self) -> None:
        self.require_product()
        scripts = [path for path in PIPELINE_CANDIDATES if path.is_file()]
        if not scripts:
            self.skipTest("PENDENTE: nome/caminho do script de preparação não está no contrato")
        original_hash = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
        clean_hash = hashlib.sha256(CLEAN_CSV.read_bytes()).hexdigest()
        completed = subprocess.run(
            [os.fspath(Path(os.environ.get("PYTHON", ROOT / ".venv" / "Scripts" / "python.exe"))), os.fspath(scripts[0])],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + "\n" + completed.stderr)
        self.assertEqual(hashlib.sha256(RAW_CSV.read_bytes()).hexdigest(), original_hash)
        self.assertEqual(hashlib.sha256(CLEAN_CSV.read_bytes()).hexdigest(), clean_hash)
        # Reabre produtos gerados pelo script para não usar o estado em cache.
        _, generated = _read_csv(CLEAN_CSV)
        expected = _expected_clean_rows()
        self.assertEqual(len(generated), len(expected))
        generated_by_id = {row["id_venda"]: row for row in generated}
        for row in expected:
            self.assertEqual(generated_by_id[row["id_venda"]], row)


class StaticSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not INDEX.is_file():
            raise unittest.SkipTest("PENDENTE: site/index.html ainda não foi entregue")
        cls.html = INDEX.read_text(encoding="utf-8")

    def test_contrato_dom_e_rotulos_acessiveis(self) -> None:
        missing = [dom_id for dom_id in DOM_IDS if not re.search(rf'\bid=["\']{re.escape(dom_id)}["\']', self.html)]
        self.assertEqual(missing, [], f"IDs DOM ausentes: {missing}")
        for dom_id in ("filtro-cidade", "filtro-categoria"):
            self.assertRegex(
                self.html,
                rf'<label\b[^>]*for=["\']{dom_id}["\']|id=["\']{dom_id}["\'][^>]*(?:aria-label|title)=',
                f"Filtro {dom_id} deve ter rótulo associado ou nome acessível",
            )

    def test_referencias_locais_existentes_e_javascript_sintaticamente_valido(self) -> None:
        refs = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', self.html, flags=re.I)
        local_refs = [ref for ref in refs if not re.match(r"(?:https?:|data:|#|mailto:|javascript:)", ref, re.I)]
        missing = [ref for ref in local_refs if not (SITE / ref.split("?", 1)[0]).is_file()]
        self.assertEqual(missing, [], f"Arquivos locais ausentes: {missing}")
        self.assertTrue(JSON_DATA.is_file(), "site/dados.json ausente")
        js_files = list(SITE.rglob("*.js"))
        self.assertTrue(js_files, "Nenhum arquivo JavaScript externo encontrado para validar")
        if not shutil.which("node"):
            self.skipTest("PENDENTE: Node.js não instalado para validar sintaxe JavaScript")
        for script in js_files:
            result = subprocess.run(["node", "--check", os.fspath(script)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"Erro sintático em {script}: {result.stderr}")

    def test_dados_embutidos_e_sem_dependencias_de_rede_ou_sintaxe_modular(self) -> None:
        html = INDEX.read_text(encoding="utf-8")
        inline = re.search(
            r'<script\b[^>]*id=["\']dashboard-data["\'][^>]*>(.*?)</script>',
            html,
            flags=re.I | re.S,
        )
        self.assertIsNotNone(inline, "index.html precisa embutir os registros para abrir por file://")
        embedded_rows = json.loads(inline.group(1))
        self.assertEqual(embedded_rows, json.loads(JSON_DATA.read_text(encoding="utf-8")))
        self.assertEqual(len(embedded_rows), 180)
        self.assertNotRegex(html, r'<script\b[^>]*\btype=["\']module["\']')

        javascript = "\n".join(path.read_text(encoding="utf-8") for path in SITE.rglob("*.js"))
        for pattern in (
            r"\bfetch\s*\(",
            r"\bXMLHttpRequest\b",
            r"\bimport\s*\(",
            r"\bexport\s+(?:default|function|const|var)",
            r"\b(?:const|let|async|await)\b",
            r"=>",
            r"`",
        ):
            self.assertNotRegex(javascript, pattern, f"O site não deve depender desta API/sintaxe: {pattern}")
        self.assertNotRegex(html, r'<(?:script|link)\b[^>]*(?:https?:)?//[^>]*', "Referências da página devem ser locais")
        readme = (PROJECT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("duplo clique", readme)
        self.assertIn("file://", readme)

    def test_contrato_itens_vendidos_temas_persistidos_e_contraste(self) -> None:
        html = INDEX.read_text(encoding="utf-8")
        css = (SITE / "estilos.css").read_text(encoding="utf-8")
        javascript = (SITE / "dashboard.js").read_text(encoding="utf-8")
        self.assertIn("Itens vendidos por categoria", html)
        self.assertIn("Itens vendidos por mês", html)
        self.assertIn('id="voltar-visao-geral"', html)
        self.assertIn('id="alternar-tema"', html)
        self.assertIn("quantidade", javascript)
        self.assertIn("localStorage", javascript)
        self.assertRegex(javascript, r"function\s+chooseCategory\s*\(")
        self.assertRegex(css, r"font-family:\s*Georgia,\s*[\"']Times New Roman[\"'],\s*serif")
        for color in ("#3a015c", "#32004f", "#220135", "#190028", "#11001c"):
            self.assertIn(color, css.lower())

        # Contraste normal do tema claro: texto principal, texto secundário e botão roxo.
        self.assertGreaterEqual(_contrast_ratio("#251234", "#f8f5ff"), 4.5)
        self.assertGreaterEqual(_contrast_ratio("#51415f", "#ffffff"), 4.5)
        self.assertGreaterEqual(_contrast_ratio("#ffffff", "#542477"), 4.5)

    def test_site_e_dados_servem_por_http(self) -> None:
        handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(  # noqa: E731
            *args, directory=os.fspath(SITE), **kwargs
        )
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            for path in ("/", "/index.html", "/dados.json"):
                with urlopen(base + path, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    payload = response.read()
                    self.assertTrue(payload)
            with urlopen(base + "/dados.json", timeout=5) as response:
                self.assertIsInstance(json.loads(response.read().decode("utf-8")), list)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except ImportError:
    PlaywrightError = RuntimeError
    sync_playwright = None


@unittest.skipIf(sync_playwright is None, "PENDENTE: Playwright/navegador não instalado; instalar para testes reais de interface")
class BrowserInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not INDEX.is_file() or not JSON_DATA.is_file():
            raise unittest.SkipTest("PENDENTE: site e JSON ainda não entregues")
        cls.records = json.loads(JSON_DATA.read_text(encoding="utf-8"))
        handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(  # noqa: E731
            *args, directory=os.fspath(SITE), **kwargs
        )
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}/"

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "server"):
            cls.server.shutdown()
            cls.server.server_close()
            cls.thread.join(timeout=5)

    def setUp(self) -> None:
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch(headless=True)
        except PlaywrightError as error:
            self.playwright.stop()
            self.skipTest(f"PENDENTE: browser Chromium Playwright indisponível: {error}")
        self.page = self.browser.new_page()
        self.page_errors: list[str] = []
        self.page.on("pageerror", lambda error: self.page_errors.append(str(error)))
        self.responses = []
        self.page.on("response", lambda response: self.responses.append(response.status) if response.status >= 400 else None)
        self.page.goto(self.url, wait_until="networkidle")
        self.page.evaluate("localStorage.removeItem('papelaria-tema')")
        self.page.reload(wait_until="networkidle")
        self.page.wait_for_selector("#filtro-cidade")

    def tearDown(self) -> None:
        if hasattr(self, "browser"):
            self.browser.close()
        if hasattr(self, "playwright"):
            self.playwright.stop()

    def _rows(self) -> int:
        return self.page.locator("#corpo-tabela tr").count()

    def _assert_dashboard_matches(
        self,
        records: list[dict[str, object]],
        donut_records: list[dict[str, object]] | None = None,
    ) -> None:
        total = sum((_decimal(row["valor_venda"]) for row in records), Decimal(0))
        count = len(records)
        expected = self.page.evaluate(
            "([total, count]) => ({"
            "total: new Intl.NumberFormat('pt-BR', {style:'currency',currency:'BRL'}).format(total),"
            "count: new Intl.NumberFormat('pt-BR', {maximumFractionDigits:0}).format(count),"
            "ticket: new Intl.NumberFormat('pt-BR', {style:'currency',currency:'BRL'}).format(count ? total/count : 0)"
            "})",
            [float(total), count],
        )
        self.assertEqual(self.page.locator("#kpi-total").inner_text(), expected["total"])
        self.assertEqual(self.page.locator("#kpi-vendas").inner_text(), expected["count"])
        self.assertEqual(self.page.locator("#kpi-ticket").inner_text(), expected["ticket"])
        self.assertEqual(
            {row.locator("td").nth(1).inner_text() for row in self.page.locator("#corpo-tabela tr").all()},
            {str(row["id_venda"]) for row in records},
            "As linhas da tabela devem corresponder aos registros filtrados",
        )

        if donut_records is None:
            donut_records = records
        by_category: dict[str, int] = defaultdict(int)
        by_month: dict[str, int] = defaultdict(int)
        for row in donut_records:
            by_category[str(row["categoria"])] += int(row["quantidade"])
        for row in records:
            by_month[str(row["data"])[:7]] += int(row["quantidade"])
        category_labels = self.page.locator("#grafico-categoria path.segmento[aria-label]").evaluate_all(
            "nodes => nodes.map(node => node.getAttribute('aria-label'))"
        )
        self.assertCountEqual(
            category_labels,
            [f"{name}: {format_integer_pt(amount)} itens vendidos" for name, amount in by_category.items()],
        )
        time_labels = self.page.locator("#grafico-tempo rect.coluna[aria-label]").evaluate_all(
            "nodes => nodes.map(node => node.getAttribute('aria-label'))"
        )
        expected_time = []
        month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        for month, amount in by_month.items():
            expected_time.append(f"{month_names[int(month[5:7]) - 1]} {month[:4]}: {format_integer_pt(amount)} itens vendidos")
        self.assertCountEqual(time_labels, expected_time)

    def _options(self, selector: str) -> list[str]:
        return self.page.locator(f"{selector} option").evaluate_all(
            "nodes => nodes.map(n => n.value).filter(value => value !== '')"
        )

    def test_filtros_isolados_combinação_sem_resultado_e_limpar(self) -> None:
        self.assertEqual(self._rows(), len(self.records))
        all_count = len(self.records)
        city_values = self._options("#filtro-cidade")
        category_values = self._options("#filtro-categoria")
        self.assertTrue(city_values)
        self.assertTrue(category_values)
        self._assert_dashboard_matches(self.records)
        city = next((v for v in city_values if 0 < sum(r["cidade"] == v for r in self.records) < all_count), None)
        category = next((v for v in category_values if 0 < sum(r["categoria"] == v for r in self.records) < all_count), None)
        self.assertIsNotNone(city, "Filtro cidade não oferece opções úteis")
        self.assertIsNotNone(category, "Filtro categoria não oferece opções úteis")

        city_match = [r for r in self.records if r["cidade"] == city]
        self.page.select_option("#filtro-cidade", city)
        self.assertEqual(self._rows(), len(city_match))
        self._assert_dashboard_matches(city_match)
        self.page.select_option("#filtro-cidade", "")
        category_match = [r for r in self.records if r["categoria"] == category]
        self.page.select_option("#filtro-categoria", category)
        self.assertEqual(self._rows(), len(category_match))
        self._assert_dashboard_matches(category_match, donut_records=self.records)
        self.page.select_option("#filtro-categoria", "")

        pair = next(
            ((c, k) for c in city_values for k in category_values
             if 0 < sum(r["cidade"] == c and r["categoria"] == k for r in self.records) < all_count),
            None,
        )
        self.assertIsNotNone(pair, "Não há combinação restritiva de filtros na base")
        c, k = pair
        expected = [r for r in self.records if r["cidade"] == c and r["categoria"] == k]
        self.page.select_option("#filtro-cidade", c)
        self.page.select_option("#filtro-categoria", k)
        self.assertEqual(self._rows(), len(expected))
        city_donut_match = [r for r in self.records if r["cidade"] == c]
        self._assert_dashboard_matches(expected, donut_records=city_donut_match)

        empty_pair = next(
            ((c, k) for c in city_values for k in category_values
             if not any(r["cidade"] == c and r["categoria"] == k for r in self.records)),
            None,
        )
        self.assertIsNotNone(empty_pair, "A base deve permitir validar uma seleção combinada vazia")
        self.page.select_option("#filtro-cidade", empty_pair[0])
        self.page.select_option("#filtro-categoria", empty_pair[1])
        self.assertEqual(self._rows(), 0)
        self.assertTrue(self.page.locator("#estado-vazio").is_visible())
        empty_city_rows = [r for r in self.records if r["cidade"] == empty_pair[0]]
        self._assert_dashboard_matches([], donut_records=empty_city_rows)
        self.assertNotRegex(self.page.locator("body").inner_text(), r"(?i)\b(?:NaN|Infinity)\b")

        self.page.locator("#limpar-filtros").click()
        self.assertEqual(self._rows(), all_count)
        self._assert_dashboard_matches(self.records)
        self.assertFalse(self.page.locator("#estado-vazio").is_visible())
        self.assertNotRegex(self.page.locator("body").inner_text(), r"(?i)\b(?:NaN|Infinity)\b")

    def test_kpis_conferem_com_registros_iniciais_e_sem_erros(self) -> None:
        self._assert_dashboard_matches(self.records)
        body = self.page.locator("body").inner_text()
        self.assertNotRegex(body, r"(?i)\b(?:NaN|Infinity)\b")
        self.assertEqual(self.page_errors, [])
        self.assertEqual(self.responses, [])

    def test_abre_por_file_url_sem_requisicoes_http(self) -> None:
        network_requests: list[str] = []
        self.page.on(
            "request",
            lambda request: network_requests.append(request.url)
            if request.url.startswith(("http://", "https://")) else None,
        )
        self.page.goto(INDEX.as_uri(), wait_until="load")
        self.page.wait_for_selector("#filtro-cidade")
        self.assertEqual(self._rows(), len(self.records))
        self._assert_dashboard_matches(self.records)
        self.assertEqual(network_requests, [], "A abertura file:// não deve requisitar a rede")
        self.assertEqual(self.page_errors, [])

    def test_responsividade_acessibilidade_basica_e_teclado(self) -> None:
        for width, height in ((390, 844), (1440, 900)):
            self.page.set_viewport_size({"width": width, "height": height})
            self.page.wait_for_timeout(150)
            dimensions = self.page.evaluate("({inner: innerWidth, scroll: document.documentElement.scrollWidth})")
            self.assertLessEqual(dimensions["scroll"], dimensions["inner"] + 1, f"Overflow horizontal em {width}px")
            for selector in ("#filtro-cidade", "#filtro-categoria", "#limpar-filtros"):
                self.assertTrue(self.page.locator(selector).is_visible())
                self.assertGreater(self.page.locator(selector).evaluate("e => e.getBoundingClientRect().height"), 0)
        self.page.keyboard.press("Tab")
        self.assertIn(self.page.evaluate("document.activeElement.id"), DOM_IDS)
        self.assertTrue(self.page.locator("#grafico-categoria").is_visible())
        self.assertTrue(self.page.locator("#grafico-tempo").is_visible())


if __name__ == "__main__":
    unittest.main(verbosity=2)
