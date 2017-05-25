# Tutorial de uso
## Extrator de informações de repositórios git

Esta ferramenta faz parte de um trabalho de graduação e mestrado e busca facilitar a extração de dados de projetos hospedados em repositórios Git/GitHub.

### Sobre a ferramenta e seu funcionamento

A ferramenta encontra-se escrita em **Python** para extração em projetos escritos em **Java**, mais precisamente **Python  2.7**, a busca pelos dados brutos existente no repositório Git é feita executando scripts **Bash** executados a partir de chamadas Python. Assim, neste momento a ferramenta necessita estar dentro de um repositório Git. Atualmente os dados extraidos devem ser armazendos em arquivo **CSV** para análise dos dados extraidos.

### Pacotes necessários
- [XLWT](https://xlwt.readthedocs.io)

### Arquivos externos necessários

Para execução da ferramenta faz-se necessário duas listas de informações:
1. Lista de imports que fazem referência a API - arquivo **imports.txt**
2. Lista de métodos que buscam - arquivo **log4j.txt**

### Modo de uso

1. A ferramenta deve estar na raiz do projeto que contem um repositório Git
2. Deve ser execução do arquivo main.py
3. A ferramenta irá gerar um arquivo **tuplas_extraidas.cvs**, onde poderão ser vistas as tuplas gerais relacionando os dados extraídos.

### Resultado gerado pela ferramenta

Como resultado poderão ser vistas tuplas relacionando os seguintes dados

- PROJETO
- CODIGO DO COMMITE
- TIMESTAMP DO COMMIT
- DESENVOLVEDOR
- ARQUIVO
- MÉTODO/ATRIBUTO COMMITADO
- QUANTIDADE DE VEZES COMMITADO
