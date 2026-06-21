"""Combinação das métricas num score de risco por arquivo.

Recebe os três ``MetricResult`` produzidos pelas análises (change frequency,
truck factor e fix ratio), normaliza cada um para a faixa 0–1 (para que nenhuma
métrica domine por estar numa escala maior) e soma com pesos, gerando um
ranking ordenado do maior para o menor risco.
"""
from analyzer.models import MetricResult, RiskRow


def normalize(metric: MetricResult) -> MetricResult:
    """Reescala os valores de uma métrica para a faixa 0–1 (divisão pelo máximo).

    Mantém a ordem relativa entre os arquivos, que é o que importa para o
    ranking. Devolve dicionário vazio se a entrada for vazia, e zeros se todos
    os valores forem zero.
    """
    if not metric:
        return {}
    maximo = max(metric.values())
    if maximo <= 0:
        return {arquivo: 0.0 for arquivo in metric}
    return {arquivo: valor / maximo for arquivo, valor in metric.items()}


def combine(
    change_freq: MetricResult,
    truck: MetricResult,
    fixes: MetricResult,
    weights: tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> list[RiskRow]:
    """Combina as três métricas num ranking de risco por arquivo.

    Os valores exibidos em cada :class:`RiskRow` são os **brutos** (para o
    usuário ver "mudou 8 vezes", "0.67", etc.); a normalização é usada apenas
    para o cálculo do ``score``. O ranking é ordenado por score decrescente,
    com o nome do arquivo como critério de desempate (determinístico).
    """
    arquivos = set(change_freq) | set(truck) | set(fixes)

    norm_cf = normalize(change_freq)
    norm_tf = normalize(truck)
    norm_fx = normalize(fixes)
    peso_cf, peso_tf, peso_fx = weights

    rows = []
    for arquivo in arquivos:
        score = (
            peso_cf * norm_cf.get(arquivo, 0.0)
            + peso_tf * norm_tf.get(arquivo, 0.0)
            + peso_fx * norm_fx.get(arquivo, 0.0)
        )
        rows.append(
            RiskRow(
                filename=arquivo,
                change_frequency=change_freq.get(arquivo, 0.0),
                truck_factor=truck.get(arquivo, 0.0),
                fix_ratio=fixes.get(arquivo, 0.0),
                score=score,
            )
        )

    rows.sort(key=lambda row: (-row.score, row.filename))
    return rows
