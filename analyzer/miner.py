"""Mineração do histórico de um repositório.

Recebe a URL (ou caminho local) de um repositório e devolve um ``MinedRepo`` no
formato do contrato de dados. Há dois backends:

- ``git`` (padrão): roda ``git log`` nativo. Rápido, pois não calcula diffs —
  apenas lista os arquivos modificados por commit.
- ``pydriller``: usa a biblioteca PyDriller. Mais lento em repositórios grandes
  (calcula o diff de cada commit), mantido como alternativa.

Esta é a única parte da ferramenta que conhece o Git; as análises de métricas
operam apenas sobre o ``MinedRepo`` resultante.
"""
import re
import shutil
import subprocess
import tempfile
from datetime import datetime

from analyzer.models import Commit, MinedRepo

_REMOTO = re.compile(r"^(https?://|git@|ssh://|git://)")
_MARCADOR = "@@C@@"


def _repo_name(repo_url: str) -> str:
    """Extrai um nome legível a partir da URL/caminho do repositório."""
    name = repo_url.replace("\\", "/").rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[: -len(".git")]
    return name or repo_url


def _e_remoto(repo_url: str) -> bool:
    return bool(_REMOTO.match(repo_url))


def mine(repo_url: str, backend: str = "git") -> MinedRepo:
    """Minera o repositório em ``repo_url`` usando o backend escolhido.

    Os commits seguem do mais antigo para o mais recente, como definido no
    contrato (:class:`analyzer.models.MinedRepo`).
    """
    if backend == "pydriller":
        return _mine_pydriller(repo_url)
    return _mine_git(repo_url)


# --------------------------------------------------------------------------- #
# Backend git (padrão)
# --------------------------------------------------------------------------- #
def _mine_git(repo_url: str) -> MinedRepo:
    tmp = None
    try:
        if _e_remoto(repo_url):
            tmp = tempfile.mkdtemp(prefix="gra_")
            subprocess.run(
                ["git", "clone", "--quiet", repo_url, tmp],
                check=True, capture_output=True,
            )
            path = tmp
        else:
            path = repo_url
        commits = _parse_git_log(path)
        return MinedRepo(name=_repo_name(repo_url), commits=commits)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def _parse_date(texto: str) -> datetime:
    try:
        return datetime.fromisoformat(texto)
    except ValueError:
        return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def _parse_git_log(path: str) -> list[Commit]:
    formato = _MARCADOR + "%H\x1f%an\x1f%aI\x1f%s"
    resultado = subprocess.run(
        [
            "git", "-c", "core.quotepath=false", "-C", path, "log",
            "--reverse", "--name-only", "--pretty=format:" + formato,
        ],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )

    commits: list[Commit] = []
    atual: Commit | None = None
    for linha in resultado.stdout.split("\n"):
        if linha.startswith(_MARCADOR):
            if atual is not None:
                commits.append(atual)
            hash_, autor, data, assunto = linha[len(_MARCADOR):].split("\x1f")
            atual = Commit(
                hash=hash_,
                author=autor or "desconhecido",
                date=_parse_date(data),
                message=assunto,
                files=[],
            )
        elif linha.strip() and atual is not None:
            atual.files.append(linha.replace("\\", "/"))
    if atual is not None:
        commits.append(atual)
    return commits


# --------------------------------------------------------------------------- #
# Backend PyDriller (opcional)
# --------------------------------------------------------------------------- #
def _changed_files(commit) -> list[str]:
    paths = []
    for mod in commit.modified_files:
        path = mod.new_path or mod.old_path
        if path:
            paths.append(path.replace("\\", "/"))
    return paths


def _mine_pydriller(repo_url: str) -> MinedRepo:
    from pydriller import Repository  # importado sob demanda

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
