"""Métrica: Change Frequency — taxa de alteração por arquivo.

"""
from collections import defaultdict
from typing import Dict

from analyzer.models import MinedRepo, MetricResult


def analyze(repo: MinedRepo) -> MetricResult:
    """Calcula o numero de modificações por arquivo.

    Args:
        repo: repositório minerado com histórico de commits.

    Returns:
        dicionário mapeando caminho do arquivo para truck factor (0 a 1).
        Exemplo: {"app.py": 1, "util.py": 5}
    """
    change_count: Dict[str, int] = defaultdict(int)

    for commit in getattr(repo, "commits", []):
        for path in getattr(commit, "files", []):
            change_count[path] += 1

    return change_count
