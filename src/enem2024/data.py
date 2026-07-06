"""Camada de dados: leitura dos CSVs do INEP com DuckDB e agregações.

Os CSVs brutos (até 1,7 GB) nunca são carregados inteiros no pandas: o DuckDB
lê direto do disco e materializa apenas agregações pequenas em parquet, em
``data/processed/``. Os notebooks consomem só os parquet.

As bases PARTICIPANTES e RESULTADOS não têm chave de ligação (LGPD); o único
cruzamento válido entre elas é agregado por município/UF de prova.
"""

from pathlib import Path

import duckdb
import pandas as pd

from . import config

# Formato oficial dos CSVs do INEP: separador ';', Latin-1, NA = string vazia
CSV_OPTS = "delim=';', encoding='latin-1', header=true, nullstr=''"


def connect() -> duckdb.DuckDBPyConnection:
    """Conexão em memória com views sobre os três CSVs oficiais."""
    con = duckdb.connect()
    create_views(
        con,
        participantes=config.PARTICIPANTES_CSV,
        resultados=config.RESULTADOS_CSV,
        itens=config.ITENS_CSV,
    )
    return con


def create_views(
    con: duckdb.DuckDBPyConnection,
    participantes: Path,
    resultados: Path,
    itens: Path,
) -> None:
    """Cria as views ``participantes``, ``resultados`` e ``itens`` sobre os CSVs."""
    for name, path in [
        ("participantes", participantes),
        ("resultados", resultados),
        ("itens", itens),
    ]:
        csv_path = str(path).replace("'", "''")
        con.execute(
            f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_csv('{csv_path}', {CSV_OPTS})"
        )


# Colunas realmente usadas nas análises. Materializar essas projeções em tabelas
# temporárias evita reler o CSV de 1,7 GB a cada agregação.
_SLIM_TABLES = {
    "participantes_slim": """
        SELECT TP_FAIXA_ETARIA, TP_SEXO, TP_ESTADO_CIVIL, TP_COR_RACA,
               TP_ST_CONCLUSAO, IN_TREINEIRO,
               CO_MUNICIPIO_PROVA, NO_MUNICIPIO_PROVA, SG_UF_PROVA,
               Q001, Q002, Q005, Q006, Q007, Q020, Q021, Q022, Q023
        FROM participantes
    """,
    "resultados_slim": """
        SELECT TP_DEPENDENCIA_ADM_ESC, TP_LOCALIZACAO_ESC,
               CO_MUNICIPIO_PROVA, NO_MUNICIPIO_PROVA, SG_UF_PROVA,
               TP_PRESENCA_CN, TP_PRESENCA_CH, TP_PRESENCA_LC, TP_PRESENCA_MT,
               NU_NOTA_CN, NU_NOTA_CH, NU_NOTA_LC, NU_NOTA_MT,
               TP_LINGUA, TP_STATUS_REDACAO,
               NU_NOTA_COMP1, NU_NOTA_COMP2, NU_NOTA_COMP3, NU_NOTA_COMP4,
               NU_NOTA_COMP5, NU_NOTA_REDACAO
        FROM resultados
    """,
}

#: Agregações materializadas em ``data/processed/<nome>.parquet``.
AGGREGATES: dict[str, str] = {
    # --- base PARTICIPANTES ---
    "perfil_participantes": """
        SELECT TP_FAIXA_ETARIA AS faixa_etaria, TP_SEXO AS sexo,
               TP_COR_RACA AS cor_raca, TP_ST_CONCLUSAO AS st_conclusao,
               IN_TREINEIRO AS treineiro, count() AS n
        FROM participantes_slim
        GROUP BY ALL
    """,
    "socio_participantes": """
        SELECT Q001 AS escolaridade_pai, Q002 AS escolaridade_mae,
               Q007 AS renda, Q020 AS wifi, Q021 AS computador,
               Q023 AS tipo_escola_em, count() AS n
        FROM participantes_slim
        GROUP BY ALL
    """,
    "participantes_uf": """
        SELECT SG_UF_PROVA AS uf, TP_SEXO AS sexo, TP_COR_RACA AS cor_raca,
               IN_TREINEIRO AS treineiro, Q007 AS renda, count() AS n
        FROM participantes_slim
        GROUP BY ALL
    """,
    "participantes_municipio": """
        SELECT CO_MUNICIPIO_PROVA AS co_municipio,
               any_value(NO_MUNICIPIO_PROVA) AS municipio,
               any_value(SG_UF_PROVA) AS uf,
               count() AS n_inscritos,
               avg((Q007 IN ('I','J','K','L','M','N','O','P','Q'))::INT) AS prop_renda_5sm_mais,
               avg((Q007 IN ('A','B'))::INT) AS prop_renda_ate_1sm,
               avg((Q002 IN ('F','G'))::INT) AS prop_mae_superior,
               avg((Q020 = 'B')::INT) AS prop_wifi,
               avg((Q021 <> 'A')::INT) AS prop_computador
        FROM participantes_slim
        GROUP BY 1
    """,
    # --- base RESULTADOS ---
    "desempenho_escola": """
        SELECT TP_DEPENDENCIA_ADM_ESC AS dependencia,
               TP_LOCALIZACAO_ESC AS localizacao,
               count() AS n,
               avg(NU_NOTA_CN) AS media_cn, median(NU_NOTA_CN) AS mediana_cn,
               avg(NU_NOTA_CH) AS media_ch, median(NU_NOTA_CH) AS mediana_ch,
               avg(NU_NOTA_LC) AS media_lc, median(NU_NOTA_LC) AS mediana_lc,
               avg(NU_NOTA_MT) AS media_mt, median(NU_NOTA_MT) AS mediana_mt,
               avg(NU_NOTA_REDACAO) AS media_redacao,
               median(NU_NOTA_REDACAO) AS mediana_redacao
        FROM resultados_slim
        GROUP BY ALL
    """,
    "desempenho_uf": """
        SELECT SG_UF_PROVA AS uf, count() AS n,
               avg((TP_PRESENCA_LC = 0)::INT) AS abstencao_dia1,
               avg((TP_PRESENCA_MT = 0)::INT) AS abstencao_dia2,
               avg(NU_NOTA_CN) AS media_cn, avg(NU_NOTA_CH) AS media_ch,
               avg(NU_NOTA_LC) AS media_lc, avg(NU_NOTA_MT) AS media_mt,
               avg(NU_NOTA_REDACAO) AS media_redacao
        FROM resultados_slim
        GROUP BY 1
    """,
    "resultados_municipio": """
        SELECT CO_MUNICIPIO_PROVA AS co_municipio,
               any_value(NO_MUNICIPIO_PROVA) AS municipio,
               any_value(SG_UF_PROVA) AS uf,
               count() AS n,
               avg((TP_PRESENCA_LC = 0)::INT) AS abstencao_dia1,
               avg((TP_PRESENCA_MT = 0)::INT) AS abstencao_dia2,
               avg(NU_NOTA_CN) AS media_cn, avg(NU_NOTA_CH) AS media_ch,
               avg(NU_NOTA_LC) AS media_lc, avg(NU_NOTA_MT) AS media_mt,
               avg(NU_NOTA_REDACAO) AS media_redacao,
               -- fração de escola privada entre quem tem escola identificada no Censo
               avg((TP_DEPENDENCIA_ADM_ESC = 4)::INT) AS prop_escola_privada,
               -- soma é NULL se faltar qualquer nota: média só de quem fez tudo
               count(NU_NOTA_CN + NU_NOTA_CH + NU_NOTA_LC + NU_NOTA_MT
                     + NU_NOTA_REDACAO) AS n_completos,
               avg((NU_NOTA_CN + NU_NOTA_CH + NU_NOTA_LC + NU_NOTA_MT
                    + NU_NOTA_REDACAO) / 5) AS media_geral
        FROM resultados_slim
        GROUP BY 1
    """,
    "presenca": """
        WITH long AS (
            UNPIVOT (
                SELECT TP_PRESENCA_CN AS CN, TP_PRESENCA_CH AS CH,
                       TP_PRESENCA_LC AS LC, TP_PRESENCA_MT AS MT
                FROM resultados_slim
            ) ON CN, CH, LC, MT INTO NAME area VALUE presenca
        )
        SELECT area, presenca, count() AS n
        FROM long
        GROUP BY ALL
    """,
    "notas_hist": """
        WITH long AS (
            UNPIVOT (
                SELECT TP_DEPENDENCIA_ADM_ESC AS dependencia,
                       NU_NOTA_CN AS CN, NU_NOTA_CH AS CH,
                       NU_NOTA_LC AS LC, NU_NOTA_MT AS MT
                FROM resultados_slim
            ) ON CN, CH, LC, MT INTO NAME area VALUE nota
        )
        SELECT area, dependencia, (floor(nota / 10) * 10)::INT AS bin, count() AS n
        FROM long
        WHERE nota IS NOT NULL
        GROUP BY ALL
    """,
    "redacao_status": """
        SELECT TP_STATUS_REDACAO AS status, count() AS n
        FROM resultados_slim
        WHERE TP_STATUS_REDACAO IS NOT NULL
        GROUP BY 1
    """,
    "redacao_dist": """
        SELECT NU_NOTA_REDACAO AS nota, TP_DEPENDENCIA_ADM_ESC AS dependencia,
               count() AS n
        FROM resultados_slim
        WHERE NU_NOTA_REDACAO IS NOT NULL
        GROUP BY ALL
    """,
    "redacao_competencias": """
        WITH long AS (
            UNPIVOT (
                SELECT NU_NOTA_COMP1 AS comp1, NU_NOTA_COMP2 AS comp2,
                       NU_NOTA_COMP3 AS comp3, NU_NOTA_COMP4 AS comp4,
                       NU_NOTA_COMP5 AS comp5
                FROM resultados_slim
                WHERE TP_STATUS_REDACAO = 1
            ) ON comp1, comp2, comp3, comp4, comp5
              INTO NAME competencia VALUE nota
        )
        SELECT competencia, nota, count() AS n
        FROM long
        GROUP BY ALL
    """,
    "lingua": """
        SELECT TP_LINGUA AS lingua, count() AS n,
               avg(NU_NOTA_LC) AS media_lc, median(NU_NOTA_LC) AS mediana_lc
        FROM resultados_slim
        WHERE TP_PRESENCA_LC = 1
        GROUP BY 1
    """,
    "amostra_notas": """
        SELECT *
        FROM (
            SELECT TP_DEPENDENCIA_ADM_ESC AS dependencia,
                   TP_LOCALIZACAO_ESC AS localizacao, TP_LINGUA AS lingua,
                   NU_NOTA_CN AS nota_cn, NU_NOTA_CH AS nota_ch,
                   NU_NOTA_LC AS nota_lc, NU_NOTA_MT AS nota_mt,
                   NU_NOTA_REDACAO AS nota_redacao
            FROM resultados_slim
            WHERE NU_NOTA_LC IS NOT NULL OR NU_NOTA_MT IS NOT NULL
        ) USING SAMPLE 200000 ROWS (reservoir, 42)
    """,
    # --- base ITENS ---
    "itens": """
        SELECT CO_POSICAO, SG_AREA, CO_ITEM, TX_GABARITO, CO_HABILIDADE,
               IN_ITEM_ABAN, NU_PARAM_A, NU_PARAM_B, NU_PARAM_C,
               TX_COR, CO_PROVA, TP_LINGUA, IN_ITEM_ADAPTADO
        FROM itens
    """,
}


def build_aggregates(
    con: duckdb.DuckDBPyConnection,
    out_dir: Path | None = None,
    names: list[str] | None = None,
) -> list[Path]:
    """Materializa as agregações em parquet e devolve os caminhos gerados."""
    out_dir = out_dir or config.PROCESSED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    for table, sql in _SLIM_TABLES.items():
        con.execute(f"CREATE OR REPLACE TEMP TABLE {table} AS {sql}")

    written = []
    for name in names or AGGREGATES:
        out = out_dir / f"{name}.parquet"
        out_sql = str(out).replace("'", "''")
        con.execute(f"COPY ({AGGREGATES[name]}) TO '{out_sql}' (FORMAT PARQUET)")
        written.append(out)
    return written


def load(name: str, processed_dir: Path | None = None) -> pd.DataFrame:
    """Carrega um agregado de ``data/processed`` como DataFrame."""
    processed_dir = processed_dir or config.PROCESSED_DIR
    path = processed_dir / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} não existe. Rode antes: uv run python -m enem2024.build_aggregates"
        )
    return pd.read_parquet(path)
