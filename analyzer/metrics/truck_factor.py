"""Métrica: Truck Factor — concentração de conhecimento por arquivo.

O truck factor mede o quão dependente um arquivo é de um único autor.
Um arquivo onde 90% dos commits vêm de uma pessoa tem truck factor = 0.9
(muito concentrado = muito risco). Um arquivo equilibrado entre dois autores
tem truck factor = 0.5 (menor risco).

Lógica: para cada arquivo, encontra o autor que fez mais commits e calcula
a proporção: commits do dominante ÷ total de commits naquele arquivo.
Resultado: valor entre 0 (distribuído) e 1 (monopolizado).
"""
from collections import defaultdict
from typing import Dict

from analyzer.models import MinedRepo, MetricResult


def analyze(repo: MinedRepo) -> MetricResult:
    """Calcula o truck factor (concentração de autoria) por arquivo.

    Args:
        repo: repositório minerado com histórico de commits.

    Returns:
        dicionário mapeando caminho do arquivo para truck factor (0 a 1).
        Exemplo: {"app.py": 0.67, "util.py": 0.5}
    """
    # Para cada arquivo, contar commits por autor
    # arquivo -> {autor -> count}
    author_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for commit in getattr(repo, "commits", []):
        author = getattr(commit, "author", "unknown")
        for path in getattr(commit, "files", []):
            author_counts[path][author] += 1

    # Calcular truck factor: maior count ÷ total
    result = {}
    for path, authors in author_counts.items():
        total = sum(authors.values())
        if total > 0:
            max_commits = max(authors.values())
            result[path] = max_commits / total
        else:
            result[path] = 0.0

    return result
