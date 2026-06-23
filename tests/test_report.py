"""Testes do relatório: tabela, conclusão e renderização."""
from analyzer.models import RiskRow
from analyzer.report import conclusion


def _linha(nome, cf=1.0, tf=0.0, fix=0.0, score=0.0):
    return RiskRow(
        filename=nome, change_frequency=cf, truck_factor=tf,
        fix_ratio=fix, score=score,
    )


def test_conclusion_cita_arquivo_de_maior_score():
    rows = [_linha("core.py", cf=100, tf=0.8, score=2.0), _linha("util.py", score=1.0)]

    texto = conclusion(rows)

    assert "core.py" in texto
    assert "2.00" in texto


def test_conclusion_lista_vazia_retorna_string_vazia():
    assert conclusion([]) == ""


def test_conclusion_menciona_truck_quando_concentrado():
    rows = [_linha("a.py", cf=10, tf=0.9, score=2.0)]

    assert "truck factor" in conclusion(rows)


def test_conclusion_omite_truck_quando_distribuido():
    rows = [_linha("a.py", cf=10, tf=0.2, score=1.0)]

    assert "truck factor" not in conclusion(rows)


def test_conclusion_menciona_fix_quando_positivo():
    rows = [_linha("a.py", cf=10, tf=0.0, fix=0.5, score=1.5)]

    assert "fix ratio" in conclusion(rows)
