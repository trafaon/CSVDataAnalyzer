#!/usr/bin/env python3
"""
Script para configurar conexão com Supabase
"""

import os
import psycopg2
from urllib.parse import urlparse

# URL base do Supabase
SUPABASE_URL = "https://mqvluacwaubcfbsplhpr.supabase.co"

def create_connection_string():
    """
    Crie a string de conexão PostgreSQL para Supabase
    
    Formato: postgresql://postgres:[PASSWORD]@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres
    """
    
    print("🔧 Configuração Supabase")
    print("=" * 50)
    print(f"URL do Projeto: {SUPABASE_URL}")
    print("\nPara conectar ao banco PostgreSQL, você precisa:")
    print("1. Senha do banco (encontre em: Project Settings > Database)")
    print("2. A string de conexão será:")
    print("   postgresql://postgres:[SUA_SENHA]@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres")
    
    password = input("\nDigite a senha do banco Supabase: ")
    
    connection_string = f"postgresql://postgres:{password}@db.mqvluacwaubcfbsplhpr.supabase.co:5432/postgres"
    
    return connection_string

def test_connection(connection_string):
    """Testar conexão com o banco"""
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        conn.close()
        print(f"✅ Conexão bem-sucedida! PostgreSQL: {version[0][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def create_env_file(connection_string):
    """Criar arquivo .env com configurações"""
    env_content = f"""# Configuração Supabase
DATABASE_URL={connection_string}
PGHOST=db.mqvluacwaubcfbsplhpr.supabase.co
PGPORT=5432
PGUSER=postgres
PGPASSWORD=<extrair_da_url>
PGDATABASE=postgres

# OpenAI API Key
OPENAI_API_KEY=sua-chave-openai-aqui
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado!")

if __name__ == "__main__":
    connection_string = create_connection_string()
    
    if test_connection(connection_string):
        create_env_file(connection_string)
        print("\n🚀 Configuração concluída!")
        print("\nPróximos passos:")
        print("1. Adicione sua chave OpenAI no arquivo .env")
        print("2. Execute: python app.py")
    else:
        print("\n❌ Verifique a senha e tente novamente")