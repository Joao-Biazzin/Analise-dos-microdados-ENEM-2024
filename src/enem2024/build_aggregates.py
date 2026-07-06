"""Gera os agregados parquet em data/processed a partir dos CSVs do INEP.

Uso:
    uv run python -m enem2024.build_aggregates
"""

import time

from . import config
from .data import build_aggregates, connect


def main() -> None:
    for csv in (config.PARTICIPANTES_CSV, config.RESULTADOS_CSV, config.ITENS_CSV):
        if not csv.exists():
            raise SystemExit(
                f"Arquivo não encontrado: {csv}\n"
                "Baixe os microdados do ENEM 2024 em "
                "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem "
                "e aponte a variável de ambiente ENEM_DATA_DIR para a pasta descompactada."
            )

    t0 = time.time()
    con = connect()
    written = build_aggregates(con)
    for path in written:
        print(f"ok  {path.name}")
    print(f"{len(written)} agregados gerados em {time.time() - t0:.0f}s -> {config.PROCESSED_DIR}")


if __name__ == "__main__":
    main()
