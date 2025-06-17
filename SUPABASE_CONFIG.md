# 🔧 Configuração Supabase

## Seu Projeto Supabase
**URL**: https://mqvluacwaubcfbsplhpr.supabase.co

## Passo a Passo

### 1. Obter Senha do Banco
1. Acesse: https://mqvluacwaubcfbsplhpr.supabase.co
2. Vá em **Settings** → **Database**
3. Procure por "Database password" ou "Connection string"
4. Copie a senha

### 2. String de Conexão
Com a senha, sua string será:
```
postgresql://postgres:[SUA_SENHA]@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres
```

### 3. Configurar no Streamlit Cloud
Quando fizer deploy, adicione estas variáveis nos **Secrets**:

```toml
DATABASE_URL = "postgresql://postgres:[SUA_SENHA]@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres"
OPENAI_API_KEY = "sua-chave-openai"
PGHOST = "db.mqvluacwaubcfbsplhpr.supabase.co"
PGPORT = "5432"
PGUSER = "postgres"
PGPASSWORD = "[SUA_SENHA]"
PGDATABASE = "postgres"
```

## Teste Local

Para testar localmente:
1. Copie `.env.example` para `.env`
2. Adicione a string de conexão
3. Execute: `streamlit run app.py`

## Deploy Completo

1. **GitHub**: Upload dos arquivos
2. **Streamlit Cloud**: Conectar repositório  
3. **Secrets**: Configurar variáveis acima
4. **Deploy**: Automático após configuração

Precisa da senha do Supabase para continuar?