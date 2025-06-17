# 📋 Passo a Passo - Publicar Sistema Online

## ETAPA 1: Preparar Arquivos (5 minutos)

### 1.1 Baixar Arquivos do Replit
Baixe estes arquivos na mesma estrutura de pastas:

```
📁 Pasta Principal/
├── 📄 app.py
├── 📄 README.md
├── 📄 requirements_github.txt ⚠️ (renomear depois)
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 LICENSE
├── 📄 setup.py
├── 📄 DEPLOY.md
├── 📁 .streamlit/
│   └── 📄 config.toml
└── 📁 utils/
    ├── 📄 __init__.py
    ├── 📄 ai_agent.py
    ├── 📄 csv_processor.py
    ├── 📄 database.py
    └── 📄 zip_handler.py
```

### 1.2 Renomear Arquivo IMPORTANTE
⚠️ **Renomeie**: `requirements_github.txt` → `requirements.txt`

---

## ETAPA 2: Upload no GitHub (10 minutos)

### 2.1 Acessar Repositório
1. Abra: https://github.com/trafaon/agente-nota-fiscal
2. Faça login na sua conta GitHub

### 2.2 Upload dos Arquivos
1. Clique em **"Add file"** → **"Upload files"**
2. Arraste TODOS os arquivos baixados
3. Mantenha a estrutura de pastas
4. Aguarde upload completo

### 2.3 Fazer Commit
1. Na parte inferior da página
2. **Título**: `Sistema completo de análise de notas fiscais`
3. **Descrição**: `Interface em português, banco Supabase, IA GPT-4o`
4. Clique **"Commit changes"**

---

## ETAPA 3: Deploy no Streamlit Cloud (15 minutos)

### 3.1 Acessar Streamlit Cloud
1. Abra: https://share.streamlit.io
2. Clique **"Sign in with GitHub"**
3. Autorize o acesso

### 3.2 Criar Nova App
1. Clique **"New app"**
2. **Repository**: `trafaon/agente-nota-fiscal`
3. **Branch**: `main`
4. **Main file path**: `app.py`
5. Clique **"Deploy!"**

### 3.3 Configurar Secrets (CRUCIAL)
1. Clique na engrenagem ⚙️ (Settings)
2. Clique **"Secrets"**
3. Cole EXATAMENTE isto:

```toml
DATABASE_URL = "postgresql://postgres:apNi2HmJ'EVt76Vy@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres"
OPENAI_API_KEY = "`OPENAI_API_KEY`"
PGHOST = "db.mqvluacwaubcfbsplhpr.supabase.co"
PGPORT = "5432"
PGUSER = "postgres"
PGPASSWORD = "apNi2HmJ'EVt76Vy"
PGDATABASE = "postgres"
```

4. Clique **"Save"**

---

## ETAPA 4: Aguardar Deploy (5-10 minutos)

### 4.1 Monitorar Status
- Aguarde a mensagem: **"Your app is live!"**
- URL final: `https://agente-nota-fiscal-xxx.streamlit.app`

### 4.2 Teste Final
1. Acesse a URL gerada
2. Verifique se aparece:
   - Interface em português
   - "100 notas fiscais carregadas"
   - "R$ 3.371.446,77"
   - Chat do assistente funcionando

---

## ✅ PRONTO! Sistema Online

### O que você terá:
- ✅ Sistema público na internet
- ✅ URL permanente para compartilhar
- ✅ 100 notas fiscais já carregadas
- ✅ Assistente IA funcionando
- ✅ Interface em português

### Em caso de erro:
1. Verifique se todos os arquivos foram enviados
2. Confirme se `requirements.txt` foi renomeado corretamente
3. Verifique se os secrets foram colados exatamente como mostrado

**Tempo total: 30-40 minutos**

Alguma dessas etapas precisa de mais detalhes?