"""Combinação das métricas num score de risco por arquivo.

O risco é guiado pela **change frequency**: um arquivo que quase não muda não é
um problema de manutenção, por mais concentrada que seja sua autoria. Por isso
ela é a *base* do score, normalizada de forma logarítmica (robusta a outliers —
um arquivo com churn altíssimo não esmaga todos os demais). O truck factor e o
fix ratio entram como *amplificadores*: elevam o risco de arquivos que já mudam
muito, mas não promovem arquivos triviais.

    score = change_freq_norm * (1 + truck_weight * truck + fix_weight * fix)
"""
import math

from analyzer.models import MetricResult, RiskRow


def normalize(metric: MetricResult) -> MetricResult:
    """Normaliza os valores para a faixa 0–1 de forma logarítmica.

    Aplica ``log(1 + valor)`` antes de dividir pelo máximo, comprimindo caudas
    longas. Mantém a ordem relativa entre os arquivos. Devolve dicionário vazio
    se a entrada for vazia, e zeros se todos os valores forem zero.
    """
    if not metric:
        return {}
    log_valores = {arquivo: math.log1p(valor) for arquivo, valor in metric.items()}
    maximo = max(log_valores.values())
    if maximo <= 0:
        return {arquivo: 0.0 for arquivo in metric}
    return {arquivo: valor / maximo for arquivo, valor in log_valores.items()}


def combine(
    change_freq: MetricResult,
    truck: MetricResult,
    fixes: MetricResult,
    truck_weight: float = 1.0,
    fix_weight: float = 1.0,
) -> list[RiskRow]:
    """Combina as três métricas num ranking de risco por arquivo.

    A change frequency é normalizada e serve de base; truck factor e fix ratio
    (já naturalmente na faixa 0–1) entram como amplificadores. Os valores
    exibidos em cada :class:`RiskRow` são os **brutos**; a normalização é usada
    apenas no cálculo do ``score``. O ranking é ordenado por score decrescente,
    com o nome do arquivo como critério de desempate (determinístico).
    """
    arquivos = set(change_freq) | set(truck) | set(fixes)
    change_freq_norm = normalize(change_freq)

    rows = []
    for arquivo in arquivos:
        base = change_freq_norm.get(arquivo, 0.0)
        valor_truck = truck.get(arquivo, 0.0)
        valor_fix = fixes.get(arquivo, 0.0)
        score = base * (1 + truck_weight * valor_truck + fix_weight * valor_fix)
        rows.append(
            RiskRow(
                filename=arquivo,
                change_frequency=change_freq.get(arquivo, 0.0),
                truck_factor=valor_truck,
                fix_ratio=valor_fix,
                score=score,
            )
        )

    rows.sort(key=lambda row: (-row.score, row.filename))
    return rows
