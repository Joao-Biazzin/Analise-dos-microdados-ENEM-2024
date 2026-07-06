"""Fixtures: CSVs minúsculos no formato exato do INEP (';', Latin-1, NA='')."""

from pathlib import Path

import duckdb
import pytest

from enem2024.data import create_views

PARTICIPANTES_HEADER = (
    "NU_INSCRICAO;NU_ANO;TP_FAIXA_ETARIA;TP_SEXO;TP_ESTADO_CIVIL;TP_COR_RACA;"
    "TP_NACIONALIDADE;TP_ST_CONCLUSAO;TP_ANO_CONCLUIU;TP_ENSINO;IN_TREINEIRO;"
    "CO_MUNICIPIO_PROVA;NO_MUNICIPIO_PROVA;CO_UF_PROVA;SG_UF_PROVA;"
    "Q001;Q002;Q003;Q004;Q005;Q006;Q007;Q008;Q009;Q010;Q011;Q012;Q013;Q014;"
    "Q015;Q016;Q017;Q018;Q019;Q020;Q021;Q022;Q023"
)

# 6 participantes: 2 em São Paulo/SP (1 renda alta Q007=Q, mãe superior),
# 2 em Aratuba/CE (renda baixa), 1 em Niterói/RJ com campos vazios (TP_ENSINO, Q007),
# 1 treineiro em São Paulo/SP.
PARTICIPANTES_ROWS = [
    "210000000001;2024;3;F;1;1;1;2;0;1;0;3550308;São Paulo;35;SP;E;F;C;D;4;B;Q;A;C;D;C;B;B;A;B;B;B;D;A;B;B;E;A",
    "210000000002;2024;4;M;1;3;1;1;3;;0;3550308;São Paulo;35;SP;E;E;C;D;4;B;C;A;C;D;C;B;B;A;B;B;B;D;A;B;B;E;A",
    "210000000003;2024;2;F;1;2;1;2;0;1;0;2301406;Aratuba;23;CE;B;C;A;B;5;A;B;A;B;B;A;A;B;A;A;A;A;B;A;A;A;C;A",
    "210000000004;2024;5;M;1;3;1;1;5;;0;2301406;Aratuba;23;CE;C;B;B;B;3;B;A;A;B;B;A;A;B;A;A;A;A;B;A;B;A;C;A",
    "210000000005;2024;11;F;2;1;1;1;10;;0;3303302;Niterói;33;RJ;E;E;C;D;2;B;;A;C;C;B;A;B;B;B;B;A;C;A;B;B;D;A",
    "210000000006;2024;1;M;1;3;1;3;0;1;1;3550308;São Paulo;35;SP;F;G;D;D;4;A;H;A;C;D;C;B;B;B;B;B;B;D;B;B;C;E;A",
]

RESULTADOS_HEADER = (
    "NU_SEQUENCIAL;NU_ANO;CO_ESCOLA;CO_MUNICIPIO_ESC;NO_MUNICIPIO_ESC;CO_UF_ESC;"
    "SG_UF_ESC;TP_DEPENDENCIA_ADM_ESC;TP_LOCALIZACAO_ESC;TP_SIT_FUNC_ESC;"
    "CO_MUNICIPIO_PROVA;NO_MUNICIPIO_PROVA;CO_UF_PROVA;SG_UF_PROVA;"
    "TP_PRESENCA_CN;TP_PRESENCA_CH;TP_PRESENCA_LC;TP_PRESENCA_MT;"
    "CO_PROVA_CN;CO_PROVA_CH;CO_PROVA_LC;CO_PROVA_MT;"
    "NU_NOTA_CN;NU_NOTA_CH;NU_NOTA_LC;NU_NOTA_MT;"
    "TX_RESPOSTAS_CN;TX_RESPOSTAS_CH;TX_RESPOSTAS_LC;TX_RESPOSTAS_MT;TP_LINGUA;"
    "TX_GABARITO_CN;TX_GABARITO_CH;TX_GABARITO_LC;TX_GABARITO_MT;"
    "TP_STATUS_REDACAO;NU_NOTA_COMP1;NU_NOTA_COMP2;NU_NOTA_COMP3;NU_NOTA_COMP4;"
    "NU_NOTA_COMP5;NU_NOTA_REDACAO"
)

_RESP = "A" * 45
_GAB = "B" * 45
_GAB_LC = "B" * 50

# 5 resultados: 2 presentes em SP (1 escola privada urbana, 1 estadual rural),
# 1 ausente nos 2 dias em Aratuba/CE, 1 presente só no dia 1 (LC/CH) sem escola,
# 1 eliminado no dia 2 com redação em branco.
RESULTADOS_ROWS = [
    f"1;2024;35000001;3550308;São Paulo;35;SP;4;1;1;3550308;São Paulo;35;SP;1;1;1;1;1419;1383;1395;1407;650.5;700.0;600.0;750.5;{_RESP};{_RESP};{_RESP};{_RESP};0;{_GAB};{_GAB};{_GAB_LC};{_GAB};1;200;200;200;200;160;960",
    f"2;2024;35000002;3550308;São Paulo;35;SP;2;2;1;3550308;São Paulo;35;SP;1;1;1;1;1419;1383;1395;1407;450.5;500.0;480.0;400.5;{_RESP};{_RESP};{_RESP};{_RESP};1;{_GAB};{_GAB};{_GAB_LC};{_GAB};1;120;120;120;120;40;520",
    "3;2024;;;;;;;;;2301406;Aratuba;23;CE;0;0;0;0;;;;;;;;;;;;;;;;;;;;;;;;",
    f"4;2024;;;;;;;;;2301406;Aratuba;23;CE;0;0;1;0;;;1395;;;;550.0;;;;{_RESP};;0;;;{_GAB_LC};;1;100;100;100;100;0;400",
    f"5;2024;33000001;3303302;Niterói;33;RJ;2;1;1;3303302;Niterói;33;RJ;1;1;1;2;1419;1383;1395;1407;500.0;520.0;510.0;;{_RESP};{_RESP};{_RESP};;0;{_GAB};{_GAB};{_GAB_LC};;4;0;0;0;0;0;0",
]

ITENS_HEADER = (
    "CO_POSICAO;SG_AREA;CO_ITEM;TX_GABARITO;CO_HABILIDADE;IN_ITEM_ABAN;"
    "TX_MOTIVO_ABAN;NU_PARAM_A;NU_PARAM_B;NU_PARAM_C;TX_COR;CO_PROVA;TP_LINGUA;"
    "IN_ITEM_ADAPTADO"
)

ITENS_ROWS = [
    "6;LC;150678;E;20;0;;3.15898;0.16783;0.17207;AZUL;1395;;0",
    "7;LC;14475;D;1;0;;2.3698;-0.23487;0.12324;AZUL;1395;;0",
    "1;MT;99999;X;5;1;Anulado;1.5;3.5;0.2;AZUL;1407;;0",
]


def _write_csv(path: Path, header: str, rows: list[str]) -> Path:
    path.write_text("\n".join([header, *rows]) + "\n", encoding="latin-1")
    return path


@pytest.fixture
def con(tmp_path):
    """Conexão DuckDB com views sobre os CSVs sintéticos."""
    connection = duckdb.connect()
    create_views(
        connection,
        participantes=_write_csv(
            tmp_path / "PARTICIPANTES_2024.csv", PARTICIPANTES_HEADER, PARTICIPANTES_ROWS
        ),
        resultados=_write_csv(
            tmp_path / "RESULTADOS_2024.csv", RESULTADOS_HEADER, RESULTADOS_ROWS
        ),
        itens=_write_csv(tmp_path / "ITENS_PROVA_2024.csv", ITENS_HEADER, ITENS_ROWS),
    )
    yield connection
    connection.close()
