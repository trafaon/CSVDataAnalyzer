# 📦 Instruções para Upload no GitHub

## Arquivos Preparados para Upload

Todos os arquivos estão prontos para serem enviados ao repositório `https://github.com/trafaon/agente-nota-fiscal`:

### Estrutura Completa:
```
📁 agente-nota-fiscal/
├── 📄 app.py                    # Aplicação principal Streamlit
├── 📄 README.md                 # Documentação completa
├── 📄 requirements_github.txt   # Dependências (renomear para requirements.txt)
├── 📄 .env.example             # Exemplo de configuração
├── 📄 .gitignore               # Arquivos a ignorar
├── 📄 LICENSE                  # Licença MIT
├── 📄 setup.py                 # Script de configuração
├── 📄 DEPLOY.md                # Guia de deploy
├── 📁 .streamlit/
│   └── 📄 config.toml          # Configuração Streamlit
└── 📁 utils/
    ├── 📄 __init__.py
    ├── 📄 ai_agent.py          # Agente IA
    ├── 📄 csv_processor.py     # Processamento CSV
    ├── 📄 database.py          # Gerenciamento PostgreSQL
    └── 📄 zip_handler.py       # Extração ZIP
```

## Passo a Passo para Upload

### 1. Baixar Arquivos do Replit
- Baixe todos os arquivos listados acima
- Mantenha a estrutura de pastas

### 2. Preparar Repositório GitHub
```bash
git clone https://github.com/trafaon/agente-nota-fiscal.git
cd agente-nota-fiscal
```

### 3. Copiar Arquivos
- Copie todos os arquivos baixados para a pasta do repositório
- **IMPORTANTE**: Renomeie `requirements_github.txt` para `requirements.txt`

### 4. Fazer Commit
```bash
git add .
git commit -m "feat: sistema completo de análise de notas fiscais com IA

- Interface em português com Streamlit
- Banco PostgreSQL para persistência
- Assistente IA com OpenAI GPT-4o
- Processamento automático de ZIP/CSV
- Análises financeiras automáticas"

git push origin main
```

## Configuração Pós-Upload

### Para Deploy no Streamlit Cloud:
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte o repositório GitHub
3. Configure os secrets:
   ```
   OPENAI_API_KEY = "sua-chave-openai"
   DATABASE_URL = "postgresql://..."
   ```

### Para Uso Local:
1. `git clone https://github.com/trafaon/agente-nota-fiscal.git`
2. `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e configure
4. `streamlit run app.py`

## Sistema Funcional

O projeto está 100% funcional com:
- ✅ 100 notas fiscais carregadas (R$ 3,37M)
- ✅ Interface em português
- ✅ Assistente IA operacional
- ✅ Banco PostgreSQL configurado
- ✅ Análises automáticas

Todos os arquivos necessários estão preparados para upload imediato.