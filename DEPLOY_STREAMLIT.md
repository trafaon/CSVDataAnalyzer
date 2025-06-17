# 🚀 Deploy no Streamlit Cloud - Configuração Completa

## Configurações Prontas

### Banco de Dados: Supabase ✅
- **URL**: https://mqvluacwaubcfbsplhpr.supabase.co
- **Dados**: 100 notas fiscais (R$ 3.371.446,77) já carregados
- **Status**: Funcionando perfeitamente

### Secrets para Streamlit Cloud

Copie e cole estas configurações na seção **Secrets** do Streamlit Cloud:

```toml
DATABASE_URL = "postgresql://postgres:apNi2HmJ'EVt76Vy@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres"
OPENAI_API_KEY = "`OPENAI_API_KEY`"
PGHOST = "db.mqvluacwaubcfbsplhpr.supabase.co"
PGPORT = "5432"
PGUSER = "postgres"
PGPASSWORD = "apNi2HmJ'EVt76Vy"
PGDATABASE = "postgres"
```

## Passo a Passo para Deploy

### 1. Upload GitHub
1. Faça download de todos os arquivos do projeto
2. Upload no repositório: `https://github.com/trafaon/agente-nota-fiscal`
3. **IMPORTANTE**: Renomeie `requirements_github.txt` para `requirements.txt`

### 2. Deploy Streamlit Cloud
1. Acesse: **share.streamlit.io**
2. Login com GitHub
3. "New app" → Selecione repositório `trafaon/agente-nota-fiscal`
4. Main file: `app.py`
5. Cole os secrets acima
6. Deploy!

### 3. Resultado Final
Seu app ficará online em:
`https://agente-nota-fiscal-xxx.streamlit.app`

## Sistema Completo
- Interface em português
- 100 notas fiscais carregadas
- Assistente IA funcionando
- Análises automáticas
- Banco Supabase configurado

## Teste Local
```bash
git clone https://github.com/trafaon/agente-nota-fiscal.git
cd agente-nota-fiscal
pip install -r requirements.txt
streamlit run app.py
```

Tudo pronto para deploy online!