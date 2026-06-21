"""Análises mockadas temporárias.

Enquanto as análises reais (change frequency, truck factor e commits) não
existem, estas funções seguem o mesmo contrato
(``analyze(MinedRepo) -> MetricResult``) e produzem valores determinísticos de
exemplo, apenas para que a CLI rode de ponta a ponta.

Para integrar com as análises reais, substitua no ``main.py`` os usos destes
mocks pelos módulos definitivos::

    from analyzer.metrics import change_frequency, truck_factor, commits
    ...
    change_freq = change_frequency.analyze(mined)
    truck = truck_factor.analyze(mined)
    fixes = commits.analyze(mined)

Este arquivo pode então ser removido.
"""
from analyzer.models import MetricResult, MinedRepo


def _arquivos(mined: MinedRepo) -> list[str]:
    """Lista de arquivos distintos do repositório, preservando a ordem."""
    vistos = []
    for commit in mined.commits:
        for arquivo in commit.files:
            if arquivo not in vistos:
                vistos.append(arquivo)
    return vistos


def mock_change_frequency(mined: MinedRepo) -> MetricResult:
    arquivos = _arquivos(mined)
    total = len(arquivos)
    return {arquivo: float(total - i) for i, arquivo in enumerate(arquivos)}


def mock_truck_factor(mined: MinedRepo) -> MetricResult:
    # Cicla entre 0.0, 0.5 e 1.0 só para variar a coluna.
    return {arquivo: (i % 3) / 2 for i, arquivo in enumerate(_arquivos(mined))}


def mock_commits(mined: MinedRepo) -> MetricResult:
    # Cicla entre 0.0, 0.33, 0.67 e 1.0 só para variar a coluna.
    return {arquivo: round((i % 4) / 3, 2) for i, arquivo in enumerate(_arquivos(mined))}
