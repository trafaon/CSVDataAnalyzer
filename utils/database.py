import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import logging

class DatabaseManager:
    """Manages PostgreSQL database operations for invoice data"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not found")
        
        self.engine = create_engine(self.database_url)
        
    def create_tables(self):
        """Create tables for invoice data if they don't exist"""
        try:
            with self.engine.connect() as conn:
                # Create invoices table (header data)
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS invoices (
                        id SERIAL PRIMARY KEY,
                        chave_acesso VARCHAR(44) UNIQUE NOT NULL,
                        modelo TEXT,
                        serie VARCHAR(50),
                        numero VARCHAR(50),
                        natureza_operacao TEXT,
                        data_emissao DATE,
                        evento_recente TEXT,
                        data_evento TIMESTAMP,
                        cnpj_emitente VARCHAR(50),
                        razao_social_emitente TEXT,
                        ie_emitente VARCHAR(50),
                        uf_emitente VARCHAR(2),
                        municipio_emitente TEXT,
                        cnpj_destinatario VARCHAR(50),
                        nome_destinatario TEXT,
                        uf_destinatario VARCHAR(2),
                        indicador_ie_destinatario VARCHAR(50),
                        destino_operacao VARCHAR(50),
                        consumidor_final VARCHAR(50),
                        presenca_comprador VARCHAR(50),
                        valor_nota_fiscal DECIMAL(15,2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create invoice items table (line items)
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS invoice_items (
                        id SERIAL PRIMARY KEY,
                        chave_acesso VARCHAR(44) NOT NULL,
                        numero_produto VARCHAR(20),
                        descricao_produto TEXT,
                        codigo_ncm VARCHAR(20),
                        ncm_tipo_produto TEXT,
                        cfop VARCHAR(10),
                        quantidade DECIMAL(15,4),
                        unidade VARCHAR(10),
                        valor_unitario DECIMAL(15,4),
                        valor_total DECIMAL(15,2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (chave_acesso) REFERENCES invoices (chave_acesso)
                    )
                """))
                
                # Create indexes for better performance
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_invoices_data_emissao ON invoices (data_emissao)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_invoices_cnpj_emitente ON invoices (cnpj_emitente)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_invoice_items_chave_acesso ON invoice_items (chave_acesso)"))
                
                conn.commit()
                
        except SQLAlchemyError as e:
            logging.error(f"Error creating tables: {e}")
            raise
    
    def save_csv_data(self, csv_data):
        """
        Save CSV data to database tables
        
        Args:
            csv_data (dict): Dictionary with filename as key and DataFrame as value
        """
        try:
            with self.engine.connect() as conn:
                for filename, df in csv_data.items():
                    if 'cabecalho' in filename.lower() or 'header' in filename.lower():
                        self._save_invoices(df, conn)
                    elif 'itens' in filename.lower() or 'items' in filename.lower():
                        self._save_invoice_items(df, conn)
                
                conn.commit()
                
        except SQLAlchemyError as e:
            logging.error(f"Error saving CSV data: {e}")
            raise
    
    def _save_invoices(self, df, conn):
        """Save invoice header data"""
        # Map CSV columns to database columns
        column_mapping = {
            'CHAVE DE ACESSO': 'chave_acesso',
            'MODELO': 'modelo',
            'SÉRIE': 'serie',
            'NÚMERO': 'numero',
            'NATUREZA DA OPERAÇÃO': 'natureza_operacao',
            'DATA EMISSÃO': 'data_emissao',
            'EVENTO MAIS RECENTE': 'evento_recente',
            'DATA/HORA EVENTO MAIS RECENTE': 'data_evento',
            'CPF/CNPJ Emitente': 'cnpj_emitente',
            'RAZÃO SOCIAL EMITENTE': 'razao_social_emitente',
            'INSCRIÇÃO ESTADUAL EMITENTE': 'ie_emitente',
            'UF EMITENTE': 'uf_emitente',
            'MUNICÍPIO EMITENTE': 'municipio_emitente',
            'CNPJ DESTINATÁRIO': 'cnpj_destinatario',
            'NOME DESTINATÁRIO': 'nome_destinatario',
            'UF DESTINATÁRIO': 'uf_destinatario',
            'INDICADOR IE DESTINATÁRIO': 'indicador_ie_destinatario',
            'DESTINO DA OPERAÇÃO': 'destino_operacao',
            'CONSUMIDOR FINAL': 'consumidor_final',
            'PRESENÇA DO COMPRADOR': 'presenca_comprador',
            'VALOR NOTA FISCAL': 'valor_nota_fiscal'
        }
        
        # Rename columns and clean data
        df_clean = df.copy()
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Convert date columns
        if 'data_emissao' in df_clean.columns:
            df_clean['data_emissao'] = pd.to_datetime(df_clean['data_emissao'], errors='coerce')
        if 'data_evento' in df_clean.columns:
            df_clean['data_evento'] = pd.to_datetime(df_clean['data_evento'], errors='coerce')
        
        # Use upsert to handle duplicates
        for _, row in df_clean.iterrows():
            conn.execute(text("""
                INSERT INTO invoices (chave_acesso, modelo, serie, numero, natureza_operacao, 
                                    data_emissao, evento_recente, data_evento, cnpj_emitente,
                                    razao_social_emitente, ie_emitente, uf_emitente, municipio_emitente,
                                    cnpj_destinatario, nome_destinatario, uf_destinatario,
                                    indicador_ie_destinatario, destino_operacao, consumidor_final,
                                    presenca_comprador, valor_nota_fiscal)
                VALUES (:chave_acesso, :modelo, :serie, :numero, :natureza_operacao,
                        :data_emissao, :evento_recente, :data_evento, :cnpj_emitente,
                        :razao_social_emitente, :ie_emitente, :uf_emitente, :municipio_emitente,
                        :cnpj_destinatario, :nome_destinatario, :uf_destinatario,
                        :indicador_ie_destinatario, :destino_operacao, :consumidor_final,
                        :presenca_comprador, :valor_nota_fiscal)
                ON CONFLICT (chave_acesso) DO UPDATE SET
                    valor_nota_fiscal = EXCLUDED.valor_nota_fiscal,
                    data_emissao = EXCLUDED.data_emissao
            """), row.to_dict())
    
    def _save_invoice_items(self, df, conn):
        """Save invoice line items data"""
        column_mapping = {
            'CHAVE DE ACESSO': 'chave_acesso',
            'NÚMERO PRODUTO': 'numero_produto',
            'DESCRIÇÃO DO PRODUTO/SERVIÇO': 'descricao_produto',
            'CÓDIGO NCM/SH': 'codigo_ncm',
            'NCM/SH (TIPO DE PRODUTO)': 'ncm_tipo_produto',
            'CFOP': 'cfop',
            'QUANTIDADE': 'quantidade',
            'UNIDADE': 'unidade',
            'VALOR UNITÁRIO': 'valor_unitario',
            'VALOR TOTAL': 'valor_total'
        }
        
        df_clean = df.copy()
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Convert numeric columns
        numeric_columns = ['quantidade', 'valor_unitario', 'valor_total']
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Clear existing items for these invoices and insert new ones
        chaves = df_clean['chave_acesso'].unique()
        for chave in chaves:
            conn.execute(text("DELETE FROM invoice_items WHERE chave_acesso = :chave"), {'chave': chave})
        
        # Insert new items
        for _, row in df_clean.iterrows():
            conn.execute(text("""
                INSERT INTO invoice_items (chave_acesso, numero_produto, descricao_produto,
                                         codigo_ncm, ncm_tipo_produto, cfop, quantidade,
                                         unidade, valor_unitario, valor_total)
                VALUES (:chave_acesso, :numero_produto, :descricao_produto,
                        :codigo_ncm, :ncm_tipo_produto, :cfop, :quantidade,
                        :unidade, :valor_unitario, :valor_total)
            """), row.to_dict())
    
    def get_invoice_summary(self):
        """Get summary statistics from the database"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT 
                        COUNT(*) as total_invoices,
                        SUM(valor_nota_fiscal) as total_value,
                        AVG(valor_nota_fiscal) as avg_value,
                        MIN(data_emissao) as min_date,
                        MAX(data_emissao) as max_date,
                        COUNT(DISTINCT cnpj_emitente) as unique_emitters,
                        COUNT(DISTINCT cnpj_destinatario) as unique_recipients
                    FROM invoices
                """)).fetchone()
                
                items_result = conn.execute(text("""
                    SELECT 
                        COUNT(*) as total_items,
                        SUM(quantidade) as total_quantity,
                        SUM(valor_total) as total_items_value
                    FROM invoice_items
                """)).fetchone()
                
                return {
                    'invoices': dict(result._mapping) if result else {},
                    'items': dict(items_result._mapping) if items_result else {}
                }
                
        except SQLAlchemyError as e:
            logging.error(f"Error getting summary: {e}")
            return {}
    
    def query_invoices(self, query_params=None):
        """Query invoices with optional filters"""
        try:
            base_query = """
                SELECT i.*, 
                       COUNT(ii.id) as item_count,
                       SUM(ii.valor_total) as calculated_total
                FROM invoices i
                LEFT JOIN invoice_items ii ON i.chave_acesso = ii.chave_acesso
            """
            
            where_conditions = []
            params = {}
            
            if query_params:
                if 'start_date' in query_params:
                    where_conditions.append("i.data_emissao >= :start_date")
                    params['start_date'] = query_params['start_date']
                
                if 'end_date' in query_params:
                    where_conditions.append("i.data_emissao <= :end_date")
                    params['end_date'] = query_params['end_date']
                
                if 'emitente' in query_params:
                    where_conditions.append("i.cnpj_emitente = :emitente")
                    params['emitente'] = query_params['emitente']
            
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)
            
            base_query += " GROUP BY i.id ORDER BY i.data_emissao DESC"
            
            with self.engine.connect() as conn:
                result = conn.execute(text(base_query), params)
                return [dict(row._mapping) for row in result]
                
        except SQLAlchemyError as e:
            logging.error(f"Error querying invoices: {e}")
            return []
    
    def get_top_products(self, limit=10):
        """Get top products by total value"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT 
                        descricao_produto,
                        SUM(quantidade) as total_quantity,
                        SUM(valor_total) as total_value,
                        COUNT(*) as frequency
                    FROM invoice_items
                    WHERE descricao_produto IS NOT NULL
                    GROUP BY descricao_produto
                    ORDER BY total_value DESC
                    LIMIT :limit
                """), {'limit': limit})
                
                return [dict(row._mapping) for row in result]
                
        except SQLAlchemyError as e:
            logging.error(f"Error getting top products: {e}")
            return []
    
    def check_database_status(self):
        """Check if database is accessible and has data"""
        try:
            with self.engine.connect() as conn:
                # Check if tables exist
                inspector = inspect(self.engine)
                tables = inspector.get_table_names()
                
                if 'invoices' not in tables:
                    return {'status': 'no_tables', 'message': 'Database tables not created'}
                
                # Check if we have data
                result = conn.execute(text("SELECT COUNT(*) FROM invoices")).scalar()
                
                if result == 0:
                    return {'status': 'empty', 'message': 'Database is empty'}
                
                return {
                    'status': 'ready',
                    'message': f'Database ready with {result} invoices',
                    'invoice_count': result
                }
                
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': f'Database error: {str(e)}'}