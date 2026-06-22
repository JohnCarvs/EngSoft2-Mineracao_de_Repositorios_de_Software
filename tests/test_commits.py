import pytest

from analyzer.metrics.commits import classify, analyze


def test_classify_fix():
    assert classify("fix: corrige bug") == "fix"


def test_classify_feat_scope():
    assert classify("feat(api): adiciona endpoint") == "feat"


def test_classify_outro():
    assert classify("mensagem solta") == "outro"
