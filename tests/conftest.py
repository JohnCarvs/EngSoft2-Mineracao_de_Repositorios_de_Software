"""Helpers de teste compartilhados.

Expõe fábricas (fixtures) para que cada módulo seja testado sem repetir
código de montagem:

- ``make_commit`` / ``make_repo``: constroem dados em memória no formato do
  contrato. Usados pelas análises de métricas, que não tocam o Git.
- ``build_git_repo``: cria um repositório Git temporário e real, usado para
  testar o minerador de ponta a ponta sem depender de rede.
"""
import os
import subprocess
from datetime import datetime, timedelta

import pytest

from analyzer.models import Commit, MinedRepo


@pytest.fixture
def make_commit():
    """Fábrica de :class:`Commit` com valores padrão sobrescrevíveis."""
    base_date = datetime(2020, 1, 1)

    def _make(hash="c0", author="ana", message="feat: muda algo",
              files=None, date=None):
        return Commit(
            hash=hash,
            author=author,
            date=date or base_date,
            message=message,
            files=list(files or []),
        )

    return _make


@pytest.fixture
def make_repo():
    """Fábrica de :class:`MinedRepo` a partir de uma lista de commits."""

    def _make(commits=None, name="repo-teste"):
        return MinedRepo(name=name, commits=list(commits or []))

    return _make


def _commit(repo, spec, stamp):
    """Cria um commit no repositório, com autor e datas determinísticos."""
    author = spec.get("author", "Ana")
    email = spec.get("email", "ana@example.com")
    env = {**os.environ, "GIT_COMMITTER_DATE": stamp}
    subprocess.run(
        [
            "git",
            "-c", f"user.name={author}",
            "-c", f"user.email={email}",
            "commit",
            "--no-gpg-sign",
            "-m", spec.get("message", "commit"),
            "--date", stamp,
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )


@pytest.fixture
def build_git_repo(tmp_path):
    """Cria um repositório Git real e devolve o caminho.

    Recebe uma lista de commits, cada um descrito por um dicionário::

        {"files": {"app.py": "conteudo"}, "message": "feat: x",
         "author": "Ana", "email": "ana@example.com"}
    """

    def _build(commits, name="repo"):
        repo = tmp_path / name
        repo.mkdir()
        subprocess.run(["git", "init", "-b", "main"], cwd=repo,
                       check=True, capture_output=True)
        base_date = datetime(2020, 1, 1)
        for i, spec in enumerate(commits):
            for path, content in spec.get("files", {}).items():
                file = repo / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(content, encoding="utf-8")
                subprocess.run(["git", "add", path], cwd=repo,
                               check=True, capture_output=True)
            stamp = (base_date + timedelta(days=i)).isoformat()
            _commit(repo, spec, stamp)
        return str(repo)

    return _build
