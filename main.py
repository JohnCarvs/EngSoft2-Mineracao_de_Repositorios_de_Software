"""Ponto de entrada da CLI do GitHubRepoAnalytics."""
import argparse

from rich.console import Console

from analyzer.metrics import commits, change_frequency, truck_factor
from analyzer.miner import mine
from analyzer.mocks import mock_change_frequency, mock_truck_factor
from analyzer.report import render
from analyzer.score import combine


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="GitHubRepoAnalytics",
        description="Minera o histórico de um repositório GitHub e ranqueia "
        "os arquivos por risco de manutenção.",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="URL do repositório no GitHub a ser analisado.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Quantidade de arquivos a exibir no ranking (padrão: 10).",
    )
    parser.add_argument(
        "--sort-by",
        choices=["score", "change", "truck", "fix"],
        default="score",
        help="Coluna usada para ordenar a tabela (padrão: score). A posição no "
        "ranking de score é sempre exibida na coluna '# (score)'.",
    )
    parser.add_argument(
        "--miner",
        choices=["git", "pydriller"],
        default="git",
        help="Backend de mineração (padrão: git, mais rápido).",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    console = Console()

    with console.status(
        f"Clonando e minerando {args.repo}... "
        "(pode demorar em repositórios grandes)"
    ):
        mined = mine(args.repo, backend=args.miner)
    console.print(f"[green]OK[/green] - {len(mined.commits)} commits minerados.")

    change_freq = change_frequency.analyze(mined)
    truck = truck_factor.analyze(mined)
    fixes = commits.analyze(mined)

    ranking = combine(change_freq, truck, fixes)
    render(ranking[: args.top], repo_name=mined.name, sort_by=args.sort_by)


if __name__ == "__main__":
    main()
