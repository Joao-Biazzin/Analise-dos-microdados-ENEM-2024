"""Testes da leitura dos CSVs no formato INEP e das agregações."""

import pandas as pd
import pytest

from enem2024.data import AGGREGATES, build_aggregates, load


def test_views_parse_latin1_separator_and_na(con):
    assert con.sql("SELECT count() FROM participantes").fetchone()[0] == 6
    assert con.sql("SELECT count() FROM resultados").fetchone()[0] == 5
    assert con.sql("SELECT count() FROM itens").fetchone()[0] == 3

    # acentos do Latin-1 preservados
    cidades = {
        r[0] for r in con.sql("SELECT DISTINCT NO_MUNICIPIO_PROVA FROM participantes").fetchall()
    }
    assert "São Paulo" in cidades
    assert "Niterói" in cidades

    # string vazia vira NULL (TP_ENSINO vazio em 3 participantes)
    n_null = con.sql("SELECT count() FROM participantes WHERE TP_ENSINO IS NULL").fetchone()[0]
    assert n_null == 3


def test_build_aggregates_writes_every_parquet(con, tmp_path):
    out = tmp_path / "processed"
    written = build_aggregates(con, out_dir=out)
    assert {p.name for p in written} == {f"{n}.parquet" for n in AGGREGATES}
    for path in written:
        assert path.exists()

    df = load("perfil_participantes", processed_dir=out)
    assert df["n"].sum() == 6


def test_load_missing_aggregate_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="build_aggregates"):
        load("perfil_participantes", processed_dir=tmp_path)


def test_participantes_municipio_proportions(con, tmp_path):
    build_aggregates(con, out_dir=tmp_path, names=["participantes_municipio"])
    df = load("participantes_municipio", processed_dir=tmp_path).set_index("municipio")

    sp = df.loc["São Paulo"]
    assert sp["n_inscritos"] == 3
    # rendas em SP: Q, C e H (H = 4–5 SM, abaixo do corte de 5 SM) -> 1/3 com 5+ SM
    assert sp["prop_renda_5sm_mais"] == pytest.approx(1 / 3)
    # mães com superior (F/G) em SP: Q002 = F, E, G -> 2/3
    assert sp["prop_mae_superior"] == pytest.approx(2 / 3)

    # Niterói: o único participante tem Q007 vazio -> proporção desconhecida (NaN),
    # nunca 0 (tratar NULL como "renda baixa" enviesaria a análise ecológica)
    assert pd.isna(df.loc["Niterói", "prop_renda_5sm_mais"])


def test_desempenho_uf_abstencao(con, tmp_path):
    build_aggregates(con, out_dir=tmp_path, names=["desempenho_uf"])
    df = load("desempenho_uf", processed_dir=tmp_path).set_index("uf")

    # CE: 2 resultados, 1 faltou dia 1 (LC=0) e o outro presente -> 50%
    assert df.loc["CE", "abstencao_dia1"] == pytest.approx(0.5)
    # CE: ambos com MT=0 -> 100% de abstenção no dia 2
    assert df.loc["CE", "abstencao_dia2"] == pytest.approx(1.0)
    # SP: todos presentes
    assert df.loc["SP", "abstencao_dia1"] == pytest.approx(0.0)


def test_prop_escola_privada_ignora_sem_escola(con, tmp_path):
    build_aggregates(con, out_dir=tmp_path, names=["resultados_municipio"])
    df = load("resultados_municipio", processed_dir=tmp_path).set_index("municipio")

    # SP: uma escola privada (4) e uma estadual (2) -> 0,5
    assert df.loc["São Paulo", "prop_escola_privada"] == pytest.approx(0.5)
    # Niterói: só estadual -> 0,0
    assert df.loc["Niterói", "prop_escola_privada"] == pytest.approx(0.0)
    # Aratuba: ninguém com escola identificada -> desconhecido (NaN), nunca 0
    assert pd.isna(df.loc["Aratuba", "prop_escola_privada"])


def test_media_geral_conta_apenas_quem_fez_tudo(con, tmp_path):
    build_aggregates(con, out_dir=tmp_path, names=["resultados_municipio"])
    df = load("resultados_municipio", processed_dir=tmp_path).set_index("municipio")

    # Niterói: eliminado em MT (nota NULL) -> ninguém completo
    assert df.loc["Niterói", "n_completos"] == 0
    # São Paulo: 2 completos; média geral = média das somas/5
    sp = df.loc["São Paulo"]
    assert sp["n_completos"] == 2
    esperado = (
        (650.5 + 700.0 + 600.0 + 750.5 + 960) / 5 + (450.5 + 500.0 + 480.0 + 400.5 + 520) / 5
    ) / 2
    assert sp["media_geral"] == pytest.approx(esperado)


def test_presenca_em_formato_longo(con, tmp_path):
    build_aggregates(con, out_dir=tmp_path, names=["presenca"])
    df = load("presenca", processed_dir=tmp_path)

    assert set(df["area"]) == {"CN", "CH", "LC", "MT"}
    # total por área = nº de linhas da base
    assert df.groupby("area")["n"].sum().eq(5).all()
    # MT: 2 presentes, 2 faltas, 1 eliminado
    mt = df[df["area"] == "MT"].set_index("presenca")["n"]
    assert mt.to_dict() == {0: 2, 1: 2, 2: 1}


def test_redacao_status_e_competencias(con, tmp_path):
    build_aggregates(con, out_dir=tmp_path, names=["redacao_status", "redacao_competencias"])
    status = load("redacao_status", processed_dir=tmp_path).set_index("status")["n"]
    assert status.to_dict() == {1: 3, 4: 1}

    comp = load("redacao_competencias", processed_dir=tmp_path)
    # só redações com status 1 entram; 5 competências presentes
    assert set(comp["competencia"]) == {"comp1", "comp2", "comp3", "comp4", "comp5"}
    assert comp.groupby("competencia")["n"].sum().eq(3).all()
