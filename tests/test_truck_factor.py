"""Testes da métrica Truck Factor."""
import pytest

from analyzer.metrics.truck_factor import analyze


def test_analyze_single_author_vira_1(make_repo, make_commit):
    """Arquivo editado por um único autor tem truck factor = 1.0 (máximo risco)."""
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["app.py"]),
        make_commit(hash="c2", author="ana", files=["app.py"]),
        make_commit(hash="c3", author="ana", files=["app.py"]),
    ])

    res = analyze(repo)
    assert res["app.py"] == 1.0


def test_analyze_two_balanced_authors_vira_0_5(make_repo, make_commit):
    """Arquivo com dois autores equilibrados (50/50) tem truck factor = 0.5."""
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["util.py"]),
        make_commit(hash="c2", author="bob", files=["util.py"]),
    ])

    res = analyze(repo)
    assert res["util.py"] == pytest.approx(0.5)


def test_analyze_empty_repo_retorna_vazio(make_repo):
    """Repositório vazio retorna dicionário vazio."""
    repo = make_repo([])
    assert analyze(repo) == {}


def test_analyze_concentrado_vs_distribuido(make_repo, make_commit):
    """Arquivo concentrado (1 autor) vs distribuído (3 autores)."""
    repo = make_repo([
        # app.py: dominado por ana (2/3)
        make_commit(hash="c1", author="ana", files=["app.py"]),
        make_commit(hash="c2", author="ana", files=["app.py"]),
        make_commit(hash="c3", author="bob", files=["app.py"]),
        # util.py: bem distribuído (3 autores iguais = 1/3 cada)
        make_commit(hash="c4", author="ana", files=["util.py"]),
        make_commit(hash="c5", author="bob", files=["util.py"]),
        make_commit(hash="c6", author="carol", files=["util.py"]),
    ])

    res = analyze(repo)
    assert res["app.py"] == pytest.approx(2.0 / 3)
    assert res["util.py"] == pytest.approx(1.0 / 3)


def test_analyze_arquivo_em_multiplos_commits_diferentes(make_repo, make_commit):
    """Arquivo pode aparecer em múltiplos commits do mesmo autor."""
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["config.py", "app.py"]),
        make_commit(hash="c2", author="ana", files=["config.py"]),
        make_commit(hash="c3", author="bob", files=["config.py"]),
    ])

    res = analyze(repo)
    # config.py: ana 2 commits, bob 1 → 2/3
    assert res["config.py"] == pytest.approx(2.0 / 3)
    # app.py: apenas ana 1 commit → 1.0
    assert res["app.py"] == 1.0


def test_analyze_multiplos_arquivos_por_commit(make_repo, make_commit):
    """Um commit pode tocar vários arquivos; cada um contribui independente."""
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["a.py", "b.py", "c.py"]),
        make_commit(hash="c2", author="bob", files=["a.py", "b.py"]),
        make_commit(hash="c3", author="carol", files=["a.py"]),
    ])

    res = analyze(repo)
    # a.py: 3 commits, cada um de um autor diferente → 1/3
    assert res["a.py"] == pytest.approx(1.0 / 3)
    # b.py: ana 1, bob 1 → 1/2
    assert res["b.py"] == pytest.approx(0.5)
    # c.py: apenas ana → 1.0
    assert res["c.py"] == 1.0
