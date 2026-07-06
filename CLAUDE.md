# CLAUDE.md — EDA Microdados ENEM 2024

## Objetivo

Análise exploratória dos microdados do ENEM 2024 (INEP) respondendo 6 perguntas definidas
antes de abrir os dados (ver README). Projeto de portfólio: a narrativa e o rigor importam
tanto quanto o código.

## Restrição central dos dados (LGPD)

As bases `PARTICIPANTES_2024` e `RESULTADOS_2024` **não têm chave de ligação** — o INEP
removeu o vínculo individual por causa da LGPD. Qualquer cruzamento entre perfil
socioeconômico e nota só é válido **agregado por município/UF de prova**
(`CO_MUNICIPIO_PROVA` existe nas duas bases). Nunca proponha join individual entre elas.

## Dados

- Local: `D:\microdadosEnem\DADOS\` (fora do repositório; configurável via env `ENEM_DATA_DIR`)
- CSVs com separador `;`, encoding **Latin-1**, NA = string vazia
- `PARTICIPANTES_2024.csv` (462 MB): perfil + questionário socioeconômico Q001–Q023
- `RESULTADOS_2024.csv` (1,7 GB): escola, presença, notas CN/CH/LC/MT, redação
- `ITENS_PROVA_2024.csv`: parâmetros TRI dos itens
- Rótulos das variáveis: `src/enem2024/labels.py` (transcritos dos inputs R oficiais do INEP)

## Arquitetura

- **DuckDB lê os CSVs direto de `D:\`** (nada é copiado para o repo); agregações pequenas
  são materializadas em parquet em `data/processed/`
- Notebooks (`notebooks/01..04`) consomem os agregados e contam a história
- Código reutilizável em `src/enem2024/`; notebooks não devem conter SQL longo inline

## Comandos

- `uv sync` — instala o ambiente
- `uv run pytest` — testes
- `uv run python -m enem2024.build_aggregates` — (re)gera os parquet de `data/processed/`
- `uv run jupyter nbconvert --to notebook --execute --inplace notebooks/XX-*.ipynb` — executa notebook

## Convenções

- Código (nomes de funções/variáveis) em inglês; textos, docstrings e narrativa em PT-BR
- README bilíngue: resumo em inglês no topo, corpo em português
- Figuras finais salvas em `reports/figures/` (versionadas), geradas via `enem2024.plots`
- Commits em **Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`),
  descrição em PT-BR no imperativo, pequenos e temáticos; autor
  `Joao Biazzin <jp.biazzin@hotmail.com>` e **sem** trailer `Co-Authored-By`
  (decisão do autor: só ele aparece como contribuidor)
- `plano-portfolio-data-science.md`, `.agents/`, `.claude/` e `data/` estão no `.gitignore`
  e **nunca** devem ser versionados
