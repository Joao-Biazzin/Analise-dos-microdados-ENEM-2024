"""Caminhos do projeto e dos microdados.

Os microdados NÃO são versionados. Aponte a variável de ambiente ENEM_DATA_DIR
para a pasta descompactada dos microdados do INEP (a que contém a subpasta DADOS).
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path(os.environ.get("ENEM_DATA_DIR", r"D:\microdadosEnem"))
RAW_DIR = DATA_DIR / "DADOS"

PARTICIPANTES_CSV = RAW_DIR / "PARTICIPANTES_2024.csv"
RESULTADOS_CSV = RAW_DIR / "RESULTADOS_2024.csv"
ITENS_CSV = RAW_DIR / "ITENS_PROVA_2024.csv"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
