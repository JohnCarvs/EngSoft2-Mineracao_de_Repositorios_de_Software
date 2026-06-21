# GitHubRepoAnalytics

Ferramenta de linha de comando que identifica **arquivos com maior risco de manutenção** em um repositório Git, por meio da mineração do histórico de commits.

## Membros do grupo

- Gabriell Laurentino Ferreira Bispo
- João Vitor de Carvalho Silva
- Pedro Henrique Fernandes
- Rafael Castro

## Objetivo da ferramenta

Conforme um projeto evolui, alguns arquivos concentram desproporcionalmente o esforço de manutenção: mudam o tempo todo, dependem de uma única pessoa e acumulam correções de bugs. Esses são os pontos onde o software é mais frágil e mais caro de evoluir.

`GitHubRepoAnalytics` minera o histórico de commits de um repositório e responde a uma única pergunta — **"quais arquivos têm maior risco de manutenção?"** — combinando três lentes complementares sobre o mesmo histórico:

- **Change frequency:** com que frequência cada arquivo foi alterado. Arquivos que mudam demais tendem a concentrar instabilidade e custo de manutenção.
- **Truck factor (autoria):** quão concentrado é o conhecimento de cada arquivo. Um arquivo com um único autor dominante fica órfão se essa pessoa sair do projeto.
- **Análise de Conventional Commits:** quantas das mudanças de um arquivo são correções (`fix`) e o quão aderente o histórico é ao padrão [Conventional Commits](https://www.conventionalcommits.org/). Muitos `fix` sinalizam um arquivo problemático.

Cada lente vira uma coluna; juntas, alimentam um **score de risco combinado** por arquivo. Um arquivo que aparece no topo das três listas ao mesmo tempo é o sinal vermelho mais forte que a ferramenta pode dar.

## Tecnologias utilizadas

- **Python 3** — linguagem da ferramenta.
- **Git** — o backend de mineração padrão usa `git log` nativo, que lista os arquivos modificados por commit sem calcular diffs, tornando a análise muito rápida mesmo em repositórios grandes.
- **[PyDriller](https://pydriller.readthedocs.io/)** — biblioteca de mineração de repositórios disponível como backend alternativo (opção `--miner pydriller`).
- **[Rich](https://rich.readthedocs.io/)** — renderização das tabelas de resultado no terminal.
- **[pytest](https://docs.pytest.org/)** — testes de unidade.
- **GitHub Actions** — execução automática dos testes a cada push e pull request.

A ferramenta recebe a URL de um repositório no GitHub, faz o `git clone` localmente e minera o `.git` — evitando os limites de taxa da API do GitHub e permitindo testes offline e determinísticos.

## Como instalar

Pré-requisitos: **Python 3.10+** e **Git** instalados.

```bash
# clonar o repositório da ferramenta
git clone https://github.com/JohnCarvs/GitHubRepoAnalytics.git
cd GitHubRepoAnalytics

# instalar as dependências
pip install -r requirements.txt
```

## Como utilizar

Passe a URL de um repositório no GitHub:

```bash
python main.py --repo https://github.com/user/repo
```

Opções:

```bash
python main.py --repo <url> --top 20            # nº de arquivos no ranking (padrão: 10)
python main.py --repo <url> --sort-by change    # ordena por outra coluna (score, change, truck, fix)
python main.py --repo <url> --miner pydriller   # usa o backend PyDriller (padrão: git)
```

A saída é uma tabela no terminal com as colunas de change frequency, truck factor, fix ratio e o score combinado de cada arquivo, seguida de uma **conclusão textual** que aponta o arquivo de maior risco e o porquê.

Por padrão a tabela é ordenada pelo score. A opção `--sort-by` permite ordenar por qualquer coluna, mas a coluna `# (score)` sempre mostra a posição do arquivo no ranking de score — assim é possível ver, por exemplo, que o arquivo mais alterado não é necessariamente o de maior risco.

## Como executar os testes localmente

Com as dependências instaladas:

```bash
pytest
```

Os testes rodam contra repositórios Git de fixture criados em tempo de execução, sem depender de rede. Eles também são executados automaticamente no GitHub Actions a cada push e pull request.
