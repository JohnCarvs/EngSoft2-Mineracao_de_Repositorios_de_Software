"""Renderização do relatório de risco de manutenção no terminal.

Recebe o ranking já calculado (lista de :class:`analyzer.models.RiskRow`,
ordenada do maior para o menor risco pelo score) e o apresenta como uma tabela,
seguida de uma conclusão textual. A coluna "#" sempre reflete a posição do
arquivo no ranking de **score** (o padrão), mesmo quando a tabela é ordenada por
outra coluna.
"""
from rich.console import Console
from rich.table import Table

from analyzer.models import RiskRow

# Nome da opção de ordenação -> atributo de RiskRow.
SORT_KEYS = {
    "score": "score",
    "change": "change_frequency",
    "truck": "truck_factor",
    "fix": "fix_ratio",
}

# Atributo -> rótulo da coluna correspondente.
_COLUNA = {
    "change_frequency": "Change freq.",
    "truck_factor": "Truck factor",
    "fix_ratio": "Fix ratio",
    "score": "Score",
}


def build_table(rows: list[RiskRow], repo_name: str = "", sort_by: str = "score") -> Table:
    """Monta a tabela do ranking.

    ``rows`` deve vir ordenada por score (define a posição na coluna "#"). Se
    ``sort_by`` for diferente de "score", as linhas são reordenadas para
    exibição, mas a posição no score é preservada.
    """
    attr_ordenacao = SORT_KEYS.get(sort_by, "score")

    # (posicao_no_score, linha) — posição fixada pela ordem de entrada (score).
    ranqueado = list(enumerate(rows, start=1))
    if attr_ordenacao != "score":
        ranqueado.sort(key=lambda par: (-getattr(par[1], attr_ordenacao), par[1].filename))

    title = "Risco de manutenção"
    if repo_name:
        title += f" - {repo_name}"

    def cabecalho(attr: str) -> str:
        rotulo = _COLUNA[attr]
        return rotulo + " *" if attr == attr_ordenacao else rotulo

    table = Table(title=title)
    table.add_column("# (score)", justify="right", no_wrap=True)
    table.add_column("Arquivo", overflow="fold")
    table.add_column(cabecalho("change_frequency"), justify="right")
    table.add_column(cabecalho("truck_factor"), justify="right")
    table.add_column(cabecalho("fix_ratio"), justify="right")
    table.add_column(cabecalho("score"), justify="right")

    for posicao_score, row in ranqueado:
        table.add_row(
            str(posicao_score),
            row.filename,
            f"{row.change_frequency:.0f}",
            f"{row.truck_factor:.2f}",
            f"{row.fix_ratio:.2f}",
            f"{row.score:.2f}",
        )
    return table


def conclusion(rows: list[RiskRow]) -> str:
    """Frase explicando qual é o arquivo de maior risco e por quê."""
    if not rows:
        return ""
    top = rows[0]
    motivos = [f"foi alterado {top.change_frequency:.0f} vezes (frequência de mudança)"]
    if top.truck_factor >= 0.5:
        motivos.append(f"tem autoria concentrada (truck factor {top.truck_factor:.2f})")
    if top.fix_ratio > 0:
        motivos.append(f"acumula correções (fix ratio {top.fix_ratio:.2f})")

    return (
        f"Conclusão: o arquivo de maior risco de manutenção é '{top.filename}' "
        f"(score {top.score:.2f}). Ele lidera o ranking porque "
        + ", ".join(motivos)
        + "."
    )


def render(rows: list[RiskRow], repo_name: str = "", console: Console = None,
           sort_by: str = "score") -> None:
    """Imprime o ranking de risco e a conclusão no terminal."""
    console = console or Console()
    if not rows:
        console.print("Nenhum arquivo analisado.")
        return
    console.print(build_table(rows, repo_name, sort_by))
    console.print()
    console.print(conclusion(rows))
