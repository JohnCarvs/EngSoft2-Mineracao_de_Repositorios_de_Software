

"""Métrica: análise de commits baseada em Conventional Commits.

Implementação incremental através de commits atômicos.
"""

import re
from collections import defaultdict
from typing import Dict

from analyzer.models import MinedRepo, MetricResult


_TYPE_RE = re.compile(r"^\s*([A-Za-z0-9-]+)(?:\([^)]+\))?(!)?\s*:")


def classify(message: str) -> str:
    """Extrai o tipo da mensagem (ex.: 'fix', 'feat').

    Suporta formatos:
    - "tipo: descrição"
    - "tipo(escopo): descrição"

    Retorna 'outro' quando não for possível identificar.
    """
    if not message:
        return "outro"
    m = _TYPE_RE.match(message)
    if not m:
        return "outro"
    # group(1) é o tipo; normalizamos para minúsculas
    return m.group(1).lower()


def analyze(repo: MinedRepo) -> MetricResult:
    """Esqueleto inicial de `analyze`: conta commits por arquivo.

    Contadores básicos (`totals`, `fixes`) serão usados para calcular a
    proporção de `fix` por arquivo em commits posteriores.
    """
    totals: Dict[str, int] = defaultdict(int)
    fixes: Dict[str, int] = defaultdict(int)

    for commit in getattr(repo, "commits", []):
        kind = classify(getattr(commit, "message", ""))
        for path in getattr(commit, "files", []):
            totals[path] += 1
            if kind == "fix":
                fixes[path] += 1

    # calcula proporção de 'fix' por arquivo
    result = {}
    for path, tot in totals.items():
        result[path] = fixes.get(path, 0) / tot

    return result

