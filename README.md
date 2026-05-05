 ## nomes dos membros do grupo
 
- Gabriell Laurentino Ferreira Bispo
- João Vitor de Carvalho Silva
- Pedro Henrique Fernandes
- Rafael Castro
 
 ## explicação do sistema 
 
Este projeto consiste no desenvolvimento de uma ferramenta de linha de comando (CLI) capaz de identificar problemas de manutenção em software por meio da mineração de repositórios Git.

A ferramenta analisa diferentes artefatos de um repositório, como commits, histórico de alterações e código-fonte, com o objetivo de extrair e rankear diversas métricas como:
- Automação e qualidade
- -verificar presença e taxa de sucesso de workflows
- -presença de testes
-- proteção de branches

 ## explicação das possíveis tecnologias utilizadas. 

- O usuário fornece o caminho ou URL de um repositório Git
- A ferramenta coleta os dados do repositório
- São aplicadas métricas e heurísticas para análise
- Os resultados são exibidos no terminal

Exemplo de uso:

```bash
python main.py --repo https://github.com/user/repo
