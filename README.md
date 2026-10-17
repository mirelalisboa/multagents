# Multagents — análise e dashboard de papelaria

Projeto de análise reproduzível e dashboard estático construído a partir de `papelaria_limpa.csv`.

## Conteúdo

- `AGENTS.md`: fluxo de trabalho e critérios do projeto.
- `.opencode/skills/`: skills de exploração, visualização e validação de dados.
- `projeto-dashboard/`: pipeline, site estático, testes e relatórios Markdown.
- `projeto-dashboard/relatorios/`: histórico das rodadas e relatório final.

## Abrir o dashboard

Abra `projeto-dashboard/site/index.html` diretamente no navegador ou sirva a pasta `site/` por HTTP:

```powershell
.\.venv\Scripts\python.exe -m http.server 8000 --directory .\projeto-dashboard\site
```

Depois, acesse <http://localhost:8000>.

## Preparar e testar

```powershell
.\.venv\Scripts\python.exe .\projeto-dashboard\preparar_dados.py
.\.venv\Scripts\python.exe -m unittest discover -s .\projeto-dashboard\tests -v
```

Os relatórios registram as verificações executadas e as pendências de navegador do ambiente original.
