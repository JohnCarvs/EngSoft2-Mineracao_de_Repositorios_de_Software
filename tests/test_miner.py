"""Testes do minerador: mina repositórios Git reais e temporários."""
from analyzer.miner import mine


def test_mine_conta_todos_os_commits(build_git_repo):
    repo = build_git_repo([
        {"files": {"app.py": "v1"}, "message": "feat: cria app"},
        {"files": {"app.py": "v2"}, "message": "fix: corrige app"},
    ])

    mined = mine(repo)

    assert len(mined.commits) == 2


def test_mine_preserva_ordem_cronologica(build_git_repo):
    repo = build_git_repo([
        {"files": {"a.py": "1"}, "message": "feat: primeiro"},
        {"files": {"a.py": "2"}, "message": "feat: segundo"},
    ])

    mined = mine(repo)

    assert mined.commits[0].message == "feat: primeiro"
    assert mined.commits[1].message == "feat: segundo"
    assert mined.commits[0].date <= mined.commits[1].date


def test_mine_captura_arquivos_modificados(build_git_repo):
    repo = build_git_repo([
        {"files": {"src/app.py": "x", "README.md": "y"}, "message": "feat: dois arquivos"},
    ])

    mined = mine(repo)

    assert set(mined.commits[0].files) == {"src/app.py", "README.md"}


def test_mine_captura_autor(build_git_repo):
    repo = build_git_repo([
        {"files": {"a.py": "1"}, "message": "feat: x",
         "author": "Joao", "email": "joao@example.com"},
    ])

    mined = mine(repo)

    assert mined.commits[0].author == "Joao"


def test_mine_deriva_nome_do_repositorio(build_git_repo):
    repo = build_git_repo(
        [{"files": {"a.py": "1"}, "message": "feat: x"}],
        name="meu-projeto",
    )

    mined = mine(repo)

    assert mined.name == "meu-projeto"
