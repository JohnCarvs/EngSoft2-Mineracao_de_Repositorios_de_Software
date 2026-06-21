"""Testes do score combinado, usando MetricResult mockados."""
from analyzer.score import combine, normalize


def test_normalize_reescala_para_faixa_0_1():
    assert normalize({"a": 2, "b": 4}) == {"a": 0.5, "b": 1.0}


def test_normalize_entrada_vazia():
    assert normalize({}) == {}


def test_normalize_todos_zeros():
    assert normalize({"a": 0, "b": 0}) == {"a": 0.0, "b": 0.0}


def test_combine_ordena_por_score_decrescente():
    change_freq = {"alto.py": 10, "baixo.py": 1}
    truck = {"alto.py": 1.0, "baixo.py": 0.0}
    fixes = {"alto.py": 1.0, "baixo.py": 0.0}

    rows = combine(change_freq, truck, fixes)

    assert [r.filename for r in rows] == ["alto.py", "baixo.py"]
    assert rows[0].score >= rows[1].score


def test_combine_preserva_valores_brutos():
    rows = combine({"a.py": 8}, {"a.py": 0.67}, {"a.py": 0.25})

    linha = rows[0]
    assert linha.change_frequency == 8
    assert linha.truck_factor == 0.67
    assert linha.fix_ratio == 0.25


def test_combine_une_arquivos_de_metricas_diferentes():
    # Cada métrica conhece arquivos diferentes; todos devem aparecer.
    rows = combine({"a.py": 1}, {"b.py": 1.0}, {"c.py": 1.0})

    assert {r.filename for r in rows} == {"a.py", "b.py", "c.py"}


def test_combine_entrada_vazia_retorna_lista_vazia():
    assert combine({}, {}, {}) == []


def test_combine_desempate_por_nome_e_deterministico():
    # Mesmos valores -> mesmo score; ordena por nome do arquivo.
    rows = combine({"b.py": 1, "a.py": 1}, {}, {})

    assert [r.filename for r in rows] == ["a.py", "b.py"]


def test_combine_respeita_pesos():
    # Zerando os pesos de truck e fixes, só change frequency conta.
    change_freq = {"x.py": 10, "y.py": 1}
    rows = combine(change_freq, {"y.py": 1.0}, {"y.py": 1.0}, weights=(1.0, 0.0, 0.0))

    assert rows[0].filename == "x.py"
