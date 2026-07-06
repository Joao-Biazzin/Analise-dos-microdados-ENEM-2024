"""Rótulos das variáveis categóricas dos microdados do ENEM 2024.

Transcritos do Dicionário oficial (Dicionário_Microdados_Enem_2024.xlsx) e dos
inputs R do INEP. Rótulos longos foram encurtados para uso em gráficos; o texto
integral das perguntas está no dicionário.

Atenção: o questionário de 2024 difere de edições anteriores — a renda familiar
é a Q007 (não a Q006) e o acesso à internet (wi-fi) é a Q020.
"""

FAIXA_ETARIA = {
    1: "Menor de 17",
    2: "17 anos",
    3: "18 anos",
    4: "19 anos",
    5: "20 anos",
    6: "21 anos",
    7: "22 anos",
    8: "23 anos",
    9: "24 anos",
    10: "25 anos",
    11: "26 a 30",
    12: "31 a 35",
    13: "36 a 40",
    14: "41 a 45",
    15: "46 a 50",
    16: "51 a 55",
    17: "56 a 60",
    18: "61 a 65",
    19: "66 a 70",
    20: "Mais de 70",
}

SEXO = {"M": "Masculino", "F": "Feminino"}

COR_RACA = {
    0: "Não declarado",
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena",
    6: "Sem informação",
}

ESTADO_CIVIL = {
    0: "Não informado",
    1: "Solteiro(a)",
    2: "Casado(a)/união estável",
    3: "Divorciado(a)/separado(a)",
    4: "Viúvo(a)",
}

ST_CONCLUSAO = {
    1: "Já concluiu o EM",
    2: "Concluirá o EM em 2024",
    3: "Concluirá o EM após 2024",
    4: "Não cursa nem concluiu o EM",
}

TREINEIRO = {0: "Não", 1: "Sim"}

# Escolaridade do pai (Q001) e da mãe (Q002)
ESCOLARIDADE = {
    "A": "Nunca estudou",
    "B": "Fund. I incompleto",
    "C": "Fund. II incompleto",
    "D": "Médio incompleto",
    "E": "Médio completo",
    "F": "Superior completo",
    "G": "Pós-graduação",
    "H": "Não sabe",
}

# Q007 — renda mensal familiar. Faixas em múltiplos do salário mínimo de 2024
# (R$ 1.412,00), que é como o INEP construiu as alternativas.
RENDA = {
    "A": "Nenhuma renda",
    "B": "Até 1 SM",
    "C": "1 a 1,5 SM",
    "D": "1,5 a 2 SM",
    "E": "2 a 2,5 SM",
    "F": "2,5 a 3 SM",
    "G": "3 a 4 SM",
    "H": "4 a 5 SM",
    "I": "5 a 6 SM",
    "J": "6 a 7 SM",
    "K": "7 a 8 SM",
    "L": "8 a 9 SM",
    "M": "9 a 10 SM",
    "N": "10 a 12 SM",
    "O": "12 a 15 SM",
    "P": "15 a 20 SM",
    "Q": "Mais de 20 SM",
}

# Q023 — tipo de escola frequentada no Ensino Médio (autodeclarado)
TIPO_ESCOLA_EM = {
    "A": "Só pública",
    "B": "Mista, privada sem bolsa",
    "C": "Mista, privada com bolsa",
    "D": "Só privada sem bolsa",
    "E": "Só privada com bolsa",
    "F": "Não frequentou o EM",
}

SIM_NAO_AB = {"A": "Não", "B": "Sim"}

# --- RESULTADOS_2024 ---

DEPENDENCIA_ADM = {
    1: "Federal",
    2: "Estadual",
    3: "Municipal",
    4: "Privada",
}

LOCALIZACAO = {1: "Urbana", 2: "Rural"}

PRESENCA = {0: "Faltou", 1: "Presente", 2: "Eliminado"}

LINGUA = {0: "Inglês", 1: "Espanhol"}

STATUS_REDACAO = {
    1: "Sem problemas",
    2: "Anulada",
    3: "Cópia do texto motivador",
    4: "Em branco",
    6: "Fuga ao tema",
    7: "Não atendeu ao tipo textual",
    8: "Texto insuficiente",
    9: "Parte desconectada",
}

COMPETENCIAS_REDACAO = {
    "comp1": "C1 · Norma culta",
    "comp2": "C2 · Compreensão do tema",
    "comp3": "C3 · Argumentação",
    "comp4": "C4 · Coesão",
    "comp5": "C5 · Proposta de intervenção",
}

AREAS = {
    "CN": "Ciências da Natureza",
    "CH": "Ciências Humanas",
    "LC": "Linguagens e Códigos",
    "MT": "Matemática",
    "REDACAO": "Redação",
}

REGIAO_POR_UF = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte",
    "RO": "Norte", "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste",
    "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}

# Código IBGE da UF -> sigla (para cruzar com as malhas do IBGE)
UF_SIGLA_POR_CODIGO = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP",
    "17": "TO", "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB",
    "26": "PE", "27": "AL", "28": "SE", "29": "BA", "31": "MG", "32": "ES",
    "33": "RJ", "35": "SP", "41": "PR", "42": "SC", "43": "RS", "50": "MS",
    "51": "MT", "52": "GO", "53": "DF",
}

# Ordens canônicas para eixos de gráficos
ORDEM_RENDA = list("ABCDEFGHIJKLMNOPQ")
ORDEM_ESCOLARIDADE = list("ABCDEFGH")
ORDEM_FAIXA_ETARIA = list(range(1, 21))
