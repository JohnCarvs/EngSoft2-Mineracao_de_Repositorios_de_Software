"""Testes do score combinado, usando MetricResult mockados."""
from analyzer.score import combine, normalize


def test_normalize_entrada_vazia():
    assert normalize({}) == {}


def test_normalize_valor_unico_vira_1():
    assert normalize({"a": 5}) == {"a": 1.0}


def test_normalize_todos_zeros():
    assert normalize({"a": 0, "b": 0}) == {"a": 0.0, "b": 0.0}


def test_normalize_comprime_outliers_preservando_ordem():
    # O maior valor vira 1.0; o menor fica entre 0 e 1, mantendo a ordem.
    resultado = normalize({"pequeno": 1, "enorme": 100})
    assert resultado["enorme"] == 1.0
    assert 0 < resultado["pequeno"] < resultado["enorme"]


def test_combine_ordena_por_score_decrescente():
    rows = combine({"alto.py": 10, "baixo.py": 1}, {"alto.py": 1.0}, {"alto.py": 1.0})

    assert [r.filename for r in rows] == ["alto.py", "baixo.py"]
    assert rows[0].score >= rows[1].score


def test_combine_preserva_valores_brutos():
    rows = combine({"a.py": 8}, {"a.py": 0.67}, {"a.py": 0.25})

    linha = rows[0]
    assert linha.change_frequency == 8
    assert linha.truck_factor == 0.67
    assert linha.fix_ratio == 0.25


def test_combine_une_arquivos_de_metricas_diferentes():
    rows = combine({"a.py": 1}, {"b.py": 1.0}, {"c.py": 1.0})

    assert {r.filename for r in rows} == {"a.py", "b.py", "c.py"}


def test_combine_entrada_vazia_retorna_lista_vazia():
    assert combine({}, {}, {}) == []


def test_combine_desempate_por_nome_e_deterministico():
    rows = combine({"b.py": 1, "a.py": 1}, {}, {})

    assert [r.filename for r in rows] == ["a.py", "b.py"]


def test_combine_arquivo_sem_churn_tem_score_zero():
    # Arquivo presente só no truck factor: sem churn, não é risco.
    rows = combine({}, {"x.py": 1.0}, {})

    assert rows[0].score == 0.0


def test_combine_churn_alto_supera_arquivo_trivial():
    # O problema do ranking: um arquivo muito alterado (mesmo com truck baixo)
    # deve superar um arquivo trivial de autor único (truck = 1.0).
    rows = combine(
        {"core.py": 100, "trivial.py": 1},
        {"core.py": 0.3, "trivial.py": 1.0},
        {},
    )

    assert rows[0].filename == "core.py"


def test_combine_amplificador_eleva_arquivo_com_truck_maior():
    # Mesmo churn; o de maior truck factor deve pontuar mais.
    rows = combine({"a.py": 10, "b.py": 10}, {"a.py": 1.0, "b.py": 0.0}, {})

    assert rows[0].filename == "a.py"


def test_combine_pesos_zerados_usam_apenas_change_frequency():
    rows = combine(
        {"a.py": 10}, {"a.py": 1.0}, {"a.py": 1.0},
        truck_weight=0.0, fix_weight=0.0,
    )

    # Único arquivo -> change_freq_norm = 1.0; sem amplificadores, score = 1.0.
    assert rows[0].score == 1.0
