"""Testes do relatório: tabela, conclusão e renderização."""
from io import StringIO

from rich.console import Console

from analyzer.models import RiskRow
from analyzer.report import build_table, conclusion, render


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


def test_build_table_tem_seis_colunas():
    table = build_table([_linha("a.py", score=1.0)])

    assert len(table.columns) == 6


def test_build_table_uma_linha_por_arquivo():
    rows = [_linha("a.py", score=2.0), _linha("b.py", score=1.0)]

    table = build_table(rows)

    assert len(table.columns[0]._cells) == 2


def test_build_table_marca_coluna_ordenada_com_asterisco():
    table = build_table([_linha("a.py", score=1.0)], sort_by="change")

    headers = [str(c.header) for c in table.columns]
    assert any("*" in h and "Change" in h for h in headers)


def test_build_table_preserva_posicao_no_score_ao_ordenar_por_outra_coluna():
    # 'b' tem o maior score (#1); 'a' tem o maior change.
    rows = [_linha("b.py", cf=1, score=2.0), _linha("a.py", cf=100, score=1.0)]

    table = build_table(rows, sort_by="change")

    # Ordenada por change, 'a' vem primeiro, mas mantém a posição #2 no score.
    assert table.columns[1]._cells[0] == "a.py"
    assert table.columns[0]._cells[0] == "2"


def test_render_imprime_tabela_e_conclusao():
    buf = StringIO()

    render([_linha("app.py", cf=5, score=1.0)], repo_name="proj",
           console=Console(file=buf, width=120))

    saida = buf.getvalue()
    assert "app.py" in saida
    assert "Conclusão" in saida


def test_render_lista_vazia_avisa():
    buf = StringIO()

    render([], console=Console(file=buf, width=120))

    assert "Nenhum arquivo analisado" in buf.getvalue()
