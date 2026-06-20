"""Contratos de dados que circulam entre os módulos da ferramenta.

Estas estruturas são a interface estável do projeto: o minerador as produz,
as análises de métricas as consomem, e o score/relatório as combinam. Manter
compatibilidade ao evoluir (preferir adicionar campos a renomear/remover).
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Commit:
    """Um commit do histórico, já reduzido ao que as análises precisam."""

    hash: str
    author: str  # nome ou e-mail do autor
    date: datetime
    message: str  # mensagem completa do commit
    files: list[str] = field(default_factory=list)  # caminhos modificados


@dataclass
class MinedRepo:
    """Resultado da mineração de um repositório.

    `commits` segue do mais antigo para o mais recente.
    """

    name: str
    commits: list[Commit] = field(default_factory=list)


# Saída de cada análise de métrica: mapeia caminho do arquivo -> valor numérico.
# Ex.: {"src/app.py": 42.0, "src/util.py": 7.0}
MetricResult = dict[str, float]


@dataclass
class RiskRow:
    """Uma linha do ranking final, produzida pelo score combinado."""

    filename: str
    change_frequency: float
    truck_factor: float
    fix_ratio: float
    score: float
