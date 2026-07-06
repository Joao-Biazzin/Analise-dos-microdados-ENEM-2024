"""Testes de consistência dos rótulos com o dicionário oficial do INEP."""

from enem2024 import labels


def test_dominios_completos():
    assert set(labels.RENDA) == set("ABCDEFGHIJKLMNOPQ")
    assert set(labels.ESCOLARIDADE) == set("ABCDEFGH")
    assert set(labels.TIPO_ESCOLA_EM) == set("ABCDEF")
    assert set(labels.FAIXA_ETARIA) == set(range(1, 21))
    assert set(labels.COR_RACA) == set(range(0, 7))
    # status 5 não existe no dicionário de 2024
    assert set(labels.STATUS_REDACAO) == {1, 2, 3, 4, 6, 7, 8, 9}


def test_regioes_cobrem_27_ufs():
    assert len(labels.REGIAO_POR_UF) == 27
    assert set(labels.REGIAO_POR_UF.values()) == {
        "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul",
    }


def test_codigos_ibge_batem_com_siglas():
    assert len(labels.UF_SIGLA_POR_CODIGO) == 27
    assert set(labels.UF_SIGLA_POR_CODIGO.values()) == set(labels.REGIAO_POR_UF)


def test_ordens_consistentes_com_dominios():
    assert labels.ORDEM_RENDA == sorted(labels.RENDA)
    assert labels.ORDEM_ESCOLARIDADE == sorted(labels.ESCOLARIDADE)
    assert labels.ORDEM_FAIXA_ETARIA == sorted(labels.FAIXA_ETARIA)
