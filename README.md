
# EstagiUp

## 📖 Sobre o Projeto
O **EstagiUp** é uma aplicação web desenvolvida com o framework **Django**, funcionando como um sistema completo de gestão de estágios. A plataforma permite que instituições ofereçam vagas, alunos se candidatem e supervisores/orientadores acompanhem o progresso dos estágios.

O projeto foi concebido para gerenciar todo o ciclo de vida de estágios, com uma arquitetura de modelo de dados robusta e um sistema de permissões bem definio.

---

## ✨ Funcionalidades Principais

- **Gestão de Perfis de Usuário:** Cada usuário possui um perfil que o identifica como Aluno, Supervisor, Orientador ou Responsável da Instituição.
- **Gestão de Vagas:** Instituições podem criar e gerenciar vagas de estágio.
- **Gestão de Estágios:** Acompanhamento do progresso de cada estágio, incluindo data de início, data de fim, status e nota.
- **Controle de Acesso:** Sistema de grupos e permissões (CRUD) garantindo que cada tipo de usuário acesse apenas as funcionalidades necessárias.
- **Automação de Configuração:** Ferramenta em **GoLang** para automatizar a criação de grupos e permissões no banco de dados.

---

## ⚙️ Modelagem de Dados
A arquitetura do projeto é baseada em um **diagrama de classes (UML)**, gerado com `django-extensions` e `pygraphviz`.

Principais entidades:

- **PerfilUsuario:** Extende o modelo `User` do Django com dados personalizados (endereço, telefone).
- **Instituicao:** Armazena dados das instituições, com relação N:N com `PerfilUsuario` (para responsáveis).
- **Vaga:** Modelo principal para vagas, com relações para `Instituicao` e `Curso`.
- **Estagio:** Conecta `Usuario`, `Vaga`, `Supervisor` e `Orientador`, representando um estágio em progresso.

## 🚀 Como Começar

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes do Python)
- Graphviz (para gerar diagramas de modelos)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/estagiup.git
   cd estagiup
    ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências do Python:

   ```bash
   pip install Django django-extensions pygraphviz Pillow
   ```

4. Instale o Graphviz no seu sistema:

   ```bash
   sudo apt-get update && sudo apt-get install -y graphviz libgraphviz-dev
   ```

5. Aplique as migrações no banco de dados:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Crie um superusuário para acessar o admin:

   ```bash
   python manage.py createsuperuser
   ```

7. Automatize a criação de grupos e permissões (opcional):

   ```bash
   python manage.py create_permissions
   ```

8. Execute o projeto:

   ```bash
   python manage.py runserver
   ```

A aplicação estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).


## 🛠️ Tecnologias Utilizadas

* **Backend:** Django
* **Banco de Dados:** SQLite (padrão)
* **Ferramentas:** django-extensions, pygraphviz
* **Automação:** GoLang (ferramenta externa)

## 👥 Participantes do Projeto

* **Guilherme Nunes:** Desenvolvedor Full-stack
* **Eduardo Guimarães:** Desenvolvedor Front-end
* **Yasmin Schultz:** Contribuidora e diagramadora

## 🛡️ Permissões de CRUD

| Modelo            | Alunos                 | Responsáveis                 | Supervisores           | Orientadores   | Administradores              |
| ----------------- | ---------------------- | ---------------------------- | ---------------------- | -------------- | ---------------------------- |
| **Instituicao**   | Read                   | Create, Read, Update         | -                      | -              | Create, Read, Update, Delete |
| **Vaga**          | Read                   | Create, Read, Update, Delete | -                      | -              | Create, Read, Update, Delete |
| **Curso**         | Read                   | Read                         | -                      | -              | Create, Read, Update, Delete |
| **Estagio**       | Create, Read (próprio) | Read                         | Read, Update (próprio) | Read (próprio) | Create, Read, Update, Delete |
| **PerfilUsuario** | Read, Update (próprio) | Read                         | Read                   | Read           | Create, Read, Update, Delete |
