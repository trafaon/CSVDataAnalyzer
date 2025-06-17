# 🚀 Guia de Deploy

## Deploy no GitHub

### 1. Preparar Repositório Local

```bash
# Clonar ou criar repositório
git clone https://github.com/trafaon/agente-nota-fiscal.git
cd agente-nota-fiscal

# Ou inicializar novo repositório
git init
git remote add origin https://github.com/trafaon/agente-nota-fiscal.git
```

### 2. Adicionar Arquivos

Copie todos os arquivos do projeto:

```
agente-nota-fiscal/
├── app.py
├── README.md
├── requirements_github.txt (renomear para requirements.txt)
├── .env.example
├── .gitignore
├── LICENSE
├── setup.py
├── .streamlit/
│   └── config.toml
└── utils/
    ├── __init__.py
    ├── ai_agent.py
    ├── csv_processor.py
    ├── database.py
    └── zip_handler.py
```

### 3. Fazer Push

```bash
git add .
git commit -m "feat: sistema completo de análise de notas fiscais com IA"
git push -u origin main
```

## Deploy no Streamlit Cloud

### 1. Conectar GitHub

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Selecione o repositório `trafaon/agente-nota-fiscal`

### 2. Configurar Secrets

No painel do Streamlit Cloud, adicione:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-sua-chave-aqui"
DATABASE_URL = "postgresql://usuario:senha@host:5432/db"
PGHOST = "seu-host-postgres"
PGPORT = "5432"
PGUSER = "usuario"
PGPASSWORD = "senha"
PGDATABASE = "nome-db"
```

### 3. Deploy

O deploy acontece automaticamente após configurar os secrets.

## Deploy Local

### 1. Instalação

```bash
git clone https://github.com/trafaon/agente-nota-fiscal.git
cd agente-nota-fiscal
pip install -r requirements.txt
```

### 2. Configuração

```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 3. Executar

```bash
streamlit run app.py
```

## Banco de Dados

### PostgreSQL Local

```bash
# Instalar PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Criar banco
sudo -u postgres createdb agente_nf
sudo -u postgres createuser -P usuario_app
```

### PostgreSQL na Nuvem

Recomendados:
- **Supabase** (gratuito até 500MB)
- **Railway** (gratuito com limites)
- **Heroku Postgres** (pago)

## Variáveis de Ambiente

```bash
# Obrigatórias
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...

# PostgreSQL (se usar separado)
PGHOST=localhost
PGPORT=5432
PGUSER=usuario
PGPASSWORD=senha
PGDATABASE=agente_nf
```

## Troubleshooting

### Erro de Conexão PostgreSQL
- Verificar credenciais no .env
- Testar conexão manual: `psql $DATABASE_URL`

### Erro OpenAI API
- Verificar chave válida
- Verificar créditos disponíveis

### Erro Streamlit
- Verificar porta disponível
- Verificar logs: `streamlit run app.py --logger.level debug`