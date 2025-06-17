import streamlit as st
import pandas as pd
import zipfile
import tempfile
import os
from datetime import datetime
import locale
from utils.zip_handler import ZipHandler
from utils.csv_processor import CSVProcessor
from utils.ai_agent import AIAgent
from utils.database import DatabaseManager

# Configure locale for Brazilian number formatting
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass

def main():
    st.set_page_config(
        page_title="AI Invoice Analyzer",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Analisador de Notas Fiscais com IA")
    st.markdown("**Envie arquivos ZIP com dados CSV de notas fiscais e faça perguntas em português**")
    
    # Initialize session state
    if 'csv_data' not in st.session_state:
        st.session_state.csv_data = {}
    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = None
    
    # Initialize database
    try:
        if st.session_state.db_manager is None:
            st.session_state.db_manager = DatabaseManager()
            st.session_state.db_manager.create_tables()
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")
        st.session_state.db_manager = None

    # Check if we have data in database
    has_database_data = False
    db_status = {}
    if st.session_state.db_manager:
        db_status = st.session_state.db_manager.check_database_status()
        has_database_data = db_status['status'] == 'ready'

    # Sidebar for file management
    with st.sidebar:
        st.header("📁 Gerenciamento de Arquivos")
        
        # Database status
        if st.session_state.db_manager:
            if has_database_data:
                st.success(f"🗄️ Banco: {db_status.get('invoice_count', 0)} notas fiscais carregadas")
            else:
                st.info("🗄️ Banco vazio - envie dados para começar")
        
        # ZIP file upload
        st.subheader("📤 Enviar Novo ZIP")
        uploaded_file = st.file_uploader(
            "Arquivo ZIP com dados CSV",
            type=['zip'],
            help="Envie um arquivo ZIP contendo arquivos CSV de notas fiscais"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Extraindo arquivo ZIP..."):
                    zip_handler = ZipHandler()
                    csv_files = zip_handler.extract_csv_files(uploaded_file)
                    
                if csv_files:
                    st.success(f"Encontrados {len(csv_files)} arquivos CSV")
                    
                    # Save to database
                    if st.session_state.db_manager:
                        with st.spinner("Salvando dados no banco..."):
                            try:
                                st.session_state.db_manager.save_csv_data(csv_files)
                                st.success("✅ Dados atualizados no banco")
                                st.rerun()  # Reload to show updated data
                            except Exception as e:
                                st.error(f"Erro ao salvar no banco: {str(e)}")
                    
                else:
                    st.error("Nenhum arquivo CSV encontrado no ZIP")
                    
            except Exception as e:
                st.error(f"Erro ao processar arquivo ZIP: {str(e)}")
        
        # Show instructions only if no data
        if not has_database_data:
            st.markdown("---")
            st.markdown("### 📋 Como usar:")
            st.markdown("1. **Envie um ZIP** com arquivos CSV de notas fiscais")
            st.markdown("2. **Visualize** os resumos financeiros")
            st.markdown("3. **Faça perguntas** para o assistente IA")
    
    # Main content area - Show data if available in database
    if has_database_data:
        
        # Data overview tab
        tab1, tab2, tab3 = st.tabs(["📈 Resumo Financeiro", "🤖 Assistente IA", "🗄️ Análise Detalhada"])
        
        with tab1:
            st.header("💰 Resumo Financeiro")
            
            # Get data from database if available, otherwise use CSV
            if has_database_data and st.session_state.db_manager:
                summary = st.session_state.db_manager.get_invoice_summary()
                
                if summary and summary.get('invoices', {}).get('total_invoices', 0) > 0:
                    inv_data = summary['invoices']
                    items_data = summary['items']
                    
                    # Main financial metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_val = inv_data.get('total_value', 0)
                        st.metric("💰 Faturamento Total", f"R$ {total_val:,.2f}" if total_val else "R$ 0,00")
                    with col2:
                        avg_val = inv_data.get('avg_value', 0)
                        st.metric("📊 Ticket Médio", f"R$ {avg_val:,.2f}" if avg_val else "R$ 0,00")
                    with col3:
                        st.metric("📄 Total de Notas", f"{inv_data.get('total_invoices', 0):,}")
                    
                    st.markdown("---")
                    
                    # Secondary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📦 Total de Itens", f"{items_data.get('total_items', 0):,}")
                    with col2:
                        total_qty = items_data.get('total_quantity', 0)
                        st.metric("📊 Quantidade Total", f"{total_qty:,.0f}" if total_qty else "0")
                    with col3:
                        st.metric("🏢 Empresas Emitentes", f"{inv_data.get('unique_emitters', 0):,}")
                    with col4:
                        st.metric("🎯 Clientes Únicos", f"{inv_data.get('unique_recipients', 0):,}")
                    
                    # Date range
                    min_date = inv_data.get('min_date')
                    max_date = inv_data.get('max_date')
                    if min_date and max_date:
                        st.info(f"📅 **Período:** {min_date} até {max_date}")
                
                else:
                    st.warning("Nenhum dado encontrado no banco de dados.")
            
            else:
                st.warning("Nenhum dado encontrado no banco de dados.")
        
        with tab2:
            st.header("🤖 Assistente IA")
            st.markdown("Faça perguntas sobre seus dados de notas fiscais em português")
            
            # Initialize AI agent
            ai_agent = AIAgent()
            
            # Chat interface
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Faça uma pergunta sobre seus dados..."):
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.write(prompt)
                
                # Generate AI response
                with st.chat_message("assistant"):
                    with st.spinner("Analisando dados e gerando resposta..."):
                        try:
                            # Prepare data context - prioritize database data
                            data_context = {}
                            
                            if has_database_data and st.session_state.db_manager:
                                # Use database data by creating DataFrames from queries
                                import pandas as pd
                                invoices = st.session_state.db_manager.query_invoices()
                                if invoices:
                                    invoices_df = pd.DataFrame(invoices)
                                    data_context["invoices_database"] = invoices_df
                                
                                # Get top products for context
                                products = st.session_state.db_manager.get_top_products(50)
                                if products:
                                    products_df = pd.DataFrame(products)
                                    data_context["products_database"] = products_df
                            
                            # No fallback needed - always use database
                            
                            if data_context:
                                response = ai_agent.answer_question(prompt, data_context)
                                st.write(response)
                                
                                # Add assistant response to chat history
                                st.session_state.chat_history.append({"role": "assistant", "content": response})
                            else:
                                error_msg = "Nenhum dado disponível para análise. Por favor, carregue dados primeiro."
                                st.error(error_msg)
                                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                            
                        except Exception as e:
                            error_msg = f"Erro ao gerar resposta: {str(e)}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            
            # Clear chat button
            if st.button("🗑️ Limpar Histórico"):
                st.session_state.chat_history = []
                st.rerun()
        
        with tab3:
            st.header("🗄️ Análise Detalhada")
            
            if st.session_state.db_manager and has_database_data:
                # Top products
                st.subheader("📦 Principais Produtos por Faturamento")
                top_products = st.session_state.db_manager.get_top_products(10)
                
                if top_products:
                    import pandas as pd
                    products_df = pd.DataFrame(top_products)
                    products_df['total_value'] = products_df['total_value'].apply(lambda x: f"R$ {x:,.2f}")
                    products_df['total_quantity'] = products_df['total_quantity'].apply(lambda x: f"{x:,.2f}")
                    
                    products_df.columns = ['Descrição do Produto', 'Quantidade Total', 'Valor Total', 'Frequência']
                    st.dataframe(products_df, use_container_width=True)
                
                # Query interface
                st.subheader("🔍 Consulta por Período")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Data Inicial", value=None)
                with col2:
                    end_date = st.date_input("Data Final", value=None)
                
                if st.button("Consultar Notas"):
                    query_params = {}
                    if start_date:
                        query_params['start_date'] = start_date
                    if end_date:
                        query_params['end_date'] = end_date
                    
                    results = st.session_state.db_manager.query_invoices(query_params)
                    
                    if results:
                        st.success(f"Encontradas {len(results)} notas fiscais")
                        
                        # Convert to DataFrame for display
                        import pandas as pd
                        results_df = pd.DataFrame(results)
                        
                        # Select key columns for display
                        display_cols = ['chave_acesso', 'data_emissao', 'razao_social_emitente', 
                                      'nome_destinatario', 'valor_nota_fiscal', 'item_count']
                        available_cols = [col for col in display_cols if col in results_df.columns]
                        
                        if available_cols:
                            display_df = results_df[available_cols].copy()
                            display_df.columns = ['Chave NF', 'Data', 'Emitente', 'Destinatário', 'Valor', 'Itens']
                            
                            if 'Valor' in display_df.columns:
                                display_df['Valor'] = [f"R$ {float(x):,.2f}" if pd.notnull(x) and str(x) != 'nan' else "N/A" for x in display_df['Valor']]
                            
                            st.dataframe(display_df, use_container_width=True)
                    else:
                        st.info("Nenhuma nota fiscal encontrada para os critérios selecionados")
            
            else:
                st.info("Carregue dados para ver análises detalhadas.")
    
    else:
        st.info("👈 Envie um arquivo ZIP com dados CSV para começar")
        
        # Display instructions
        st.markdown("""
        ### Como usar esta aplicação:
        
        1. **Envie um arquivo ZIP** contendo seus dados CSV de notas fiscais
        2. **Visualize** os resumos financeiros automáticos
        3. **Faça perguntas** para o assistente IA sobre seus dados
        
        ### Exemplos de perguntas:
        - "Qual é o total de vendas este mês?"
        - "Quais são os 5 principais produtos por faturamento?"
        - "Mostre-me as tendências de vendas por trimestre"
        - "Qual é o valor médio das notas fiscais?"
        - "Quantas empresas diferentes emitiram notas?"
        """)

if __name__ == "__main__":
    main()
