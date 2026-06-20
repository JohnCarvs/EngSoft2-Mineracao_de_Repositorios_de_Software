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
- **[PyDriller](https://pydriller.readthedocs.io/)** — biblioteca de mineração de repositórios; abstrai o histórico de commits, arquivos modificados e autoria.
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

Opções úteis:

```bash
python main.py --repo <url> --top 20        # mostra os 20 arquivos de maior risco
```

A saída é uma tabela no terminal, ordenada pelo score de risco, com as colunas de change frequency, truck factor e correções de cada arquivo.

## Como executar os testes localmente

Com as dependências instaladas:

```bash
pytest
```

Os testes rodam contra repositórios Git de fixture criados em tempo de execução, sem depender de rede. Eles também são executados automaticamente no GitHub Actions a cada push e pull request.
