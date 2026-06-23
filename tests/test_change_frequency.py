"""Testes da métrica Change Frequency."""
import pytest

from analyzer.metrics.change_frequency import analyze


def test_analyze_empty_repo(make_repo, make_commit):
    repo = make_repo([])

    res = analyze(repo)
    assert res == {}


def test_created_file(make_repo, make_commit):
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["app.py"]),
    ])

    res = analyze(repo)
    assert res["app.py"] == 1

def test_created_updated_file(make_repo, make_commit):
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["app.py"]),
        make_commit(hash="c2", author="ana", files=["app.py"]),
    ])

    res = analyze(repo)
    assert res["app.py"] == 2


def test_multifile_commits(make_repo, make_commit):
    repo = make_repo([
        make_commit(hash="c1", author="ana", files=["init.py", "app.py"]),
        make_commit(hash="c2", author="bob", files=["init.py", "config.py"]),
    ])

    res = analyze(repo)
    assert res["config.py"] == 1
    assert res["init.py"] == 2
    assert res["app.py"] == 1


