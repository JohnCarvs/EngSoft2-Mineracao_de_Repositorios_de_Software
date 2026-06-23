"""Testes de Truck Factor"""
import pytest


from analyzer.metrics.truck_factor import analyze


def test_single_author_file(make_repo, make_commit):
    repo = make_repo([
        make_commit(hash="c1", author="bob", message="feat: x", files=["app.py"]),
        make_commit(hash="c2", author="bob", message="fix: y", files=["app.py"]),
        make_commit(hash="c3", author="bob", message="fix: z", files=["app.py"]),
    ])

    res = analyze(repo)
    assert res["app.py"] == 1.

