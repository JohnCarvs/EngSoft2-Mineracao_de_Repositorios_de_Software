"""Ponto de entrada da CLI do GitHubRepoAnalytics."""
import argparse


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
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    print(f"Repositório: {args.repo}")
    print(f"Top: {args.top}")
    # A orquestração (minerador -> análises -> score -> relatório)
    # será conectada nas próximas etapas.


if __name__ == "__main__":
    main()
