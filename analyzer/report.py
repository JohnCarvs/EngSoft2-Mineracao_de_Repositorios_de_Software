"""Renderização do relatório de risco de manutenção no terminal.

Recebe o ranking já calculado (lista de :class:`analyzer.models.RiskRow`,
ordenada do maior para o menor risco) e o apresenta como uma tabela. Não faz
cálculo nenhum — apenas exibe o que o score produziu.
"""
from rich.console import Console
from rich.table import Table

from analyzer.models import RiskRow


def build_table(rows: list[RiskRow], repo_name: str = "") -> Table:
    """Monta a tabela do ranking de risco a partir das linhas fornecidas."""
    title = "Risco de manutenção"
    if repo_name:
        title += f" - {repo_name}"

    table = Table(title=title)
    table.add_column("#", justify="right", no_wrap=True)
    table.add_column("Arquivo", overflow="fold")
    table.add_column("Change freq.", justify="right")
    table.add_column("Truck factor", justify="right")
    table.add_column("Fix ratio", justify="right")
    table.add_column("Score", justify="right")

    for position, row in enumerate(rows, start=1):
        table.add_row(
            str(position),
            row.filename,
            f"{row.change_frequency:.0f}",
            f"{row.truck_factor:.2f}",
            f"{row.fix_ratio:.2f}",
            f"{row.score:.2f}",
        )
    return table


def render(rows: list[RiskRow], repo_name: str = "", console: Console = None) -> None:
    """Imprime o ranking de risco no terminal."""
    console = console or Console()
    if not rows:
        console.print("Nenhum arquivo analisado.")
        return
    console.print(build_table(rows, repo_name))
