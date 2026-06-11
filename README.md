# Sistema de Gestão de Reservas de Hotel

> Permite registar os clientes, consultar quartos disponíveis, gerir as reservas, realizar check-in/check-out e a ocupação no hotel/histórico de reservas.



---

## Informação do Projeto

| Campo            | Detalhe                              |
|------------------|--------------------------------------|
| **Curso**        | UFCD 10790 – Projeto de Programação  |
| **Formando**     | Nelson Proença                       |
| **Formador**     | Carlos Barata                        |
| **Instituição**  | IEFP                                 |
| **Data de início | [03/06/2026]                         |
| **Data de entrega| [19/06/2026]                         |
| **Versão**       | 1.0                                  |

---

## Índice

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Requisitos Técnicos](#requisitos-técnicos)
- [Como Instalar e Executar](#como-instalar-e-executar)
- [Base de Dados](#base-de-dados)
- [Arquitetura](#arquitetura)
- [Documentação](#documentação)
- [Estado do Projeto](#estado-do-projeto)

---

## Descrição

Explica aqui o projeto com um pouco mais de detalhe do que na frase de abertura.

- Qual o problema que resolve?
- Quem são os utilizadores?
- Qual a abordagem técnica (ex: aplicação de consola em Python com base de dados SQLite)?

---

## Funcionalidades

Lista as principais funcionalidades implementadas:

- [ ] Funcionalidade 1 — ex: Registo de utilizador
- [ ] Funcionalidade 2 — ex: Login com autenticação
- [ ] Funcionalidade 3 — ex: Listagem de produtos
- [ ] Funcionalidade 4 — ex: ...

> As checkboxes ficam marcadas (`[x]`) à medida que implementas cada funcionalidade.

---

## Estrutura do Repositório

```
projeto_ufcd10790/
│
├── README.md               ← Este ficheiro — apresentação do projeto
├── .gitignore              ← Ficheiros a ignorar pelo Git
│
├── src/                    ← Código fonte Python
│   ├── main.py             ← Ponto de entrada da aplicação
│   ├── dal/                ← Data Access Layer
│   │   └── ...
│   ├── bll/                ← Business Logic Layer
│   │   └── ...
│   └── ui/                 ← Interface com o utilizador
│       └── ...
│
├── sql/                    ← Scripts SQL (opcional)
│   ├── criar_tabelas.sql   ← DDL — criação do esquema
│   └── dados_exemplo.sql   ← Dados iniciais de teste
│
├── docs/                   ← Toda a documentação do projeto
│   ├── relatorio.docx      ← Relatório final do projeto
│   ├── requisitos.xlsx     ← Levantamento de requisitos (RF e RNF)
│   ├── manual_utilizador.docx  ← Manual de utilização da aplicação
│   └── manual_tecnico.docx     ← Manual de instalação e configuração
│
├── assets/                 ← Recursos visuais e apresentação
│   ├── apresentacao.pptx   ← Apresentação final
│   ├── diagrama_arquitetura.png  ← Diagrama de arquitetura do sistema
│   └── diagrama_bd.png          ← Diagrama da base de dados (se aplicável)
│
└── tests/                  ← Testes (opcional mas recomendado)
    └── test_bll.py         ← Testes à camada de negócio
```

---

## Requisitos Técnicos

- Python 3.10 ou superior
- Bibliotecas necessárias (lista aqui as que usas):
  - `sqlite3` — incluído no Python (não precisa de instalação)
  - *(adiciona outras se necessário, ex: `bcrypt`, `tabulate`)*

Para instalar dependências externas (se houver):

```bash
pip install -r requirements.txt
```

---

## Como Instalar e Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/[teu-utilizador]/[nome-do-repositorio].git
cd [nome-do-repositorio]
```

### 2. (Opcional) Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
cd src
python main.py
```

---

## Base de Dados

> Preenche esta secção se o projeto usa base de dados.

- **Sistema:** SQLite (ficheiro local) / *outro se aplicável*
- **Ficheiro:** `src/database.db` *(criado automaticamente na primeira execução)*
- **Esquema:** ver [`sql/criar_tabelas.sql`](sql/criar_tabelas.sql)

Para inicializar a base de dados manualmente a partir dos scripts SQL:

```bash
sqlite3 database.db < sql/criar_tabelas.sql
sqlite3 database.db < sql/dados_exemplo.sql
```

---

## Arquitetura

O projeto segue uma arquitetura em três camadas:

```
┌─────────────────────────────┐
│     UI — Interface          │  Interação com o utilizador
├─────────────────────────────┤
│     BLL — Lógica de Negócio │  Regras e validações
├─────────────────────────────┤
│     DAL — Acesso a Dados    │  Queries e persistência
├─────────────────────────────┤
│     Base de Dados           │  SQLite / outro
└─────────────────────────────┘
```

O diagrama completo está em [`assets/diagrama_arquitetura.png`](assets/diagrama_arquitetura.png).

---

## Documentação

| Documento                  | Localização                        | Descrição                              |
|----------------------------|------------------------------------|----------------------------------------|
| Relatório do Projeto       | `docs/relatorio.docx`              | Relatório completo do projeto          |
| Levantamento de Requisitos | `docs/requisitos.xlsx`             | Requisitos funcionais e não funcionais |
| Manual do Utilizador       | `docs/manual_utilizador.docx`      | Como usar a aplicação                  |
| Manual Técnico             | `docs/manual_tecnico.docx`         | Instalação e configuração              |
| Apresentação               | `assets/apresentacao.pptx`         | Slides da apresentação final           |

---

## Estado do Projeto

```
Sessão 1 — Requisitos        ✅ Concluído
Sessão 2 — Arquitetura       ✅ Concluído
Sessão 3 — Desenvolvimento 1 🔄 Em curso
Sessão 4 — Desenvolvimento 2 ⏳ Pendente
Sessão 5 — Apresentação      ⏳ Pendente
```

---

*UFCD 10790 – Projeto de Programação | [Ano letivo]*
