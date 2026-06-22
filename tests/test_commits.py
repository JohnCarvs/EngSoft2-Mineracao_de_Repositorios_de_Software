import pytest

from analyzer.metrics.commits import classify, analyze


def test_classify_fix():
    assert classify("fix: corrige bug") == "fix"


def test_classify_feat_scope():
    assert classify("feat(api): adiciona endpoint") == "feat"


def test_classify_outro():
    assert classify("mensagem solta") == "outro"


def test_analyze_fix_ratio(make_repo, make_commit):
    repo = make_repo([
        make_commit(hash="c1", author="ana", message="feat: x", files=["app.py"]),
        make_commit(hash="c2", author="bob", message="fix: y", files=["app.py"]),
        make_commit(hash="c3", author="bob", message="fix: z", files=["app.py", "util.py"]),
        make_commit(hash="c4", author="bob", message="chore: w", files=["util.py"]),
    ])

    res = analyze(repo)
    assert res["app.py"] == pytest.approx(2 / 3)
    assert res["util.py"] == pytest.approx(1 / 2)
