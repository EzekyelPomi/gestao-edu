# Gestão Edu — Sistema de Gestão Escolar

Projeto de desenvolvimento de um sistema de gestão escolar com foco na organização de informações acadêmicas e na análise de desempenho dos estudantes.

A proposta é integrar conceitos de desenvolvimento de sistemas, modelagem de banco de dados, APIs REST e análise de dados em uma única aplicação.

> **Status:** Em desenvolvimento.

## Objetivos

- Desenvolver uma aplicação para organizar informações escolares.
- Implementar operações de cadastro, consulta, atualização e exclusão de registros.
- Estruturar um banco de dados relacional para armazenar as informações.
- Criar uma API REST para comunicação entre o sistema e seus dados.
- Explorar a análise do desempenho acadêmico por estudante, turma e período.
- Aplicar boas práticas de organização, versionamento e documentação de código.

## Funcionalidades planejadas

- Cadastro e consulta de estudantes.
- Organização de turmas e disciplinas.
- Registro de notas e resultados acadêmicos.
- API REST para acesso e gerenciamento dos dados.
- Relatórios de desempenho individual e por turma.
- Indicadores e visualizações para apoiar a análise dos resultados.

## Tecnologias

- **Python:** linguagem principal do projeto.
- **Flask:** framework para desenvolvimento da aplicação e da API.
- **HTML e CSS:** interface web.
- **SQL:** consultas e manipulação de dados.
- **Banco de dados relacional:** armazenamento das informações.
- **Git e GitHub:** versionamento e documentação do projeto.

## Arquitetura prevista

A aplicação será organizada em componentes com responsabilidades distintas:

1. **Interface:** páginas utilizadas pelo usuário para interagir com o sistema.
2. **Backend:** processamento das regras de negócio utilizando Python e Flask.
3. **API REST:** endpoints para consultar e manipular os dados por meio de requisições HTTP.
4. **Banco de dados:** armazenamento persistente das informações escolares.
5. **Análise de dados:** processamento dos registros para gerar indicadores e relatórios acadêmicos.

## Objetivo de aprendizado

Este projeto faz parte do meu portfólio de desenvolvimento em tecnologia, com o objetivo de integrar conhecimentos de Análise e Desenvolvimento de Sistemas e Matemática, explorando a relação entre desenvolvimento de software, organização de dados e interpretação de indicadores educacionais.


## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/EzekyelPomi/gestao-edu.git
```

### 2. Acesse a pasta do projeto

```bash
cd gestao-edu
```

### 3. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a aplicação

```bash
python app.py
```

### 7. Acesse no navegador

Após iniciar a aplicação, acesse:

http://127.0.0.1:5000


## Observação sobre os dados

O projeto utilizará dados fictícios para demonstração. Não serão publicados dados pessoais ou registros reais de estudantes.
