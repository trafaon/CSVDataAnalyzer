#!/usr/bin/env python3
"""
Setup script para configuração inicial do Agente Nota Fiscal
"""

import os
import sys
import subprocess

def create_directories():
    """Criar diretórios necessários"""
    dirs = [
        '.streamlit',
        'data',
        'logs'
    ]
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ Diretório criado: {dir_name}")

def install_dependencies():
    """Instalar dependências Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_github.txt"])
        print("✓ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências")
        return False
    return True

def setup_streamlit_config():
    """Configurar Streamlit"""
    config_content = """[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    print("✓ Configuração do Streamlit criada")

def main():
    print("🚀 Configurando Agente Nota Fiscal...")
    
    # Criar diretórios
    create_directories()
    
    # Configurar Streamlit
    setup_streamlit_config()
    
    # Verificar arquivo .env
    if not os.path.exists('.env'):
        print("\n⚠️  Lembre-se de:")
        print("1. Copiar .env.example para .env")
        print("2. Configurar suas chaves de API")
        print("3. Configurar conexão PostgreSQL")
    
    print("\n✅ Setup concluído!")
    print("\nPara executar:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main()