"""Mineração do histórico de um repositório.

Recebe a URL (ou caminho local) de um repositório, percorre seu histórico de
commits com o PyDriller e devolve um ``MinedRepo`` no formato do contrato de
dados. É a única parte da ferramenta que conhece o Git/PyDriller; as análises
de métricas operam apenas sobre o ``MinedRepo`` resultante.
"""
from pydriller import Repository

from analyzer.models import Commit, MinedRepo


def _repo_name(repo_url: str) -> str:
    """Extrai um nome legível a partir da URL/caminho do repositório."""
    name = repo_url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[: -len(".git")]
    return name or repo_url


def _changed_files(commit) -> list[str]:
    """Caminhos dos arquivos modificados em um commit (ignora renomeados nulos)."""
    paths = []
    for mod in commit.modified_files:
        path = mod.new_path or mod.old_path
        if path:
            paths.append(path)
    return paths


def mine(repo_url: str) -> MinedRepo:
    """Minera o repositório em ``repo_url`` e devolve os commits do histórico.

    Os commits seguem do mais antigo para o mais recente, como definido no
    contrato (:class:`analyzer.models.MinedRepo`).
    """
    commits = []
    for commit in Repository(repo_url).traverse_commits():
        commits.append(
            Commit(
                hash=commit.hash,
                author=commit.author.name or commit.author.email or "desconhecido",
                date=commit.author_date,
                message=commit.msg,
                files=_changed_files(commit),
            )
        )
    return MinedRepo(name=_repo_name(repo_url), commits=commits)
