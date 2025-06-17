# 📊 CSV Data Analyzer com IA

Sistema inteligente para análise de notas fiscais em formato CSV com assistente IA integrado.

## 🔗 Links do Projeto

- **Repositório GitHub**: https://github.com/trafaon/CSVDataAnalyzer
- **Demo Online**: https://agentcsv-skynet2.streamlit.app

## 🚀 Funcionalidades

- **Upload de ZIP**: Carregamento automático de arquivos CSV de notas fiscais
- **Banco PostgreSQL**: Armazenamento persistente dos dados
- **Resumo Financeiro**: Métricas automáticas de faturamento, ticket médio e totais
- **Assistente IA**: Respostas inteligentes sobre os dados usando OpenAI GPT-4o
- **Interface em Português**: Sistema totalmente localizado

## 📋 Exemplos de Perguntas para o Assistente

- "Qual fornecedor recebeu o maior montante total?"
- "Qual item foi entregue em maior quantidade?"
- "Qual a nota fiscal mais antiga emitida?"
- "Quantas notas fiscais são do tipo NF-e?"
- "Qual o total de faturamento por mês?"

## 🛠️ Tecnologias

- **Frontend**: Streamlit
- **Backend**: Python 3.11
- **Banco de Dados**: PostgreSQL/Supabase
- **IA Framework**: LangChain com OpenAI GPT-4o
- **Processamento**: Pandas, SQLAlchemy
- **Arquitetura**: Sistema de agentes com memória conversacional

## ⚙️ Configuração

### Pré-requisitos

- Python 3.11+
- PostgreSQL
- Chave API da OpenAI

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/trafaon/CSVDataAnalyzer.git
cd CSVDataAnalyzer
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env
OPENAI_API_KEY=sua_chave_openai_aqui
DATABASE_URL=postgresql://usuario:senha@localhost:5432/agente_nf
```

4. Execute o sistema:
```bash
streamlit run app.py
```

## 📂 Estrutura do Projeto

```
agente-nota-fiscal/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências Python
├── .streamlit/
│   └── config.toml       # Configuração Streamlit
├── utils/
│   ├── __init__.py
│   ├── ai_agent.py       # Agente IA com OpenAI
│   ├── csv_processor.py  # Processamento de dados CSV
│   ├── database.py       # Gerenciamento PostgreSQL
│   └── zip_handler.py    # Extração de arquivos ZIP
└── README.md
```

## 🎯 Como Usar

1. **Acesse a aplicação** através do navegador
2. **Envie um arquivo ZIP** contendo CSVs de notas fiscais
3. **Visualize automaticamente** os resumos financeiros
4. **Faça perguntas** para o assistente IA sobre seus dados

## 📊 Dados Suportados

O sistema processa automaticamente:
- **Cabeçalho das NFs**: Dados gerais, emitentes, destinatários, valores
- **Itens das NFs**: Produtos, quantidades, valores unitários e totais
- **Formatos**: CSV com separadores (vírgula, ponto-vírgula, tab)
- **Codificações**: UTF-8, Latin-1, CP1252, ISO-8859-1

## 🔒 Segurança

- Dados armazenados localmente no PostgreSQL
- Chaves API protegidas por variáveis de ambiente
- Processamento local sem exposição de dados sensíveis

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub.