import os
import json
import pandas as pd
from openai import OpenAI

class AIAgent:
    """AI agent for answering questions about financial/invoice data"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
        self.client = OpenAI(api_key=api_key)
        
    def answer_question(self, question, data_context):
        """
        Answer a question about the provided data context
        
        Args:
            question (str): User's question in Portuguese or English
            data_context (dict): Dictionary with filename as key and DataFrame as value
            
        Returns:
            str: AI-generated answer
        """
        try:
            # Prepare data summary for AI context
            data_summary = self._prepare_data_summary(data_context)
            
            # Create system prompt
            system_prompt = self._create_system_prompt(data_summary)
            
            # Create user prompt
            user_prompt = f"""
            User Question: {question}
            
            Please analyze the data and provide a comprehensive answer in the same language as the question.
            If the question is in Portuguese, respond in Portuguese. If in English, respond in English.
            
            Include specific numbers, calculations, and insights where relevant.
            If you need to perform calculations, show the steps.
            Format financial values appropriately (e.g., R$ for Brazilian Real, $ for USD).
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erro ao processar pergunta / Error processing question: {str(e)}"
    
    def _prepare_data_summary(self, data_context):
        """
        Prepare a summary of the data for AI context
        
        Args:
            data_context (dict): Dictionary with filename as key and DataFrame as value
            
        Returns:
            dict: Summary of the data
        """
        summary = {}
        
        for filename, df in data_context.items():
            file_summary = {
                'rows': len(df),
                'columns': list(df.columns),
                'column_types': {col: str(df[col].dtype) for col in df.columns},
                'sample_data': {}
            }
            
            # Add sample data for each column (first 3 non-null values)
            for col in df.columns:
                sample_values = df[col].dropna().head(3).tolist()
                file_summary['sample_data'][col] = sample_values
            
            # Identify financial columns and add statistics
            financial_cols = self._identify_financial_columns(df)
            if financial_cols:
                file_summary['financial_columns'] = {}
                for col in financial_cols:
                    numeric_col = self._convert_to_numeric(df[col])
                    if numeric_col is not None:
                        file_summary['financial_columns'][col] = {
                            'total': float(numeric_col.sum()),
                            'average': float(numeric_col.mean()),
                            'min': float(numeric_col.min()),
                            'max': float(numeric_col.max()),
                            'count': int(numeric_col.notna().sum())
                        }
            
            # Identify date columns and add date ranges
            date_cols = self._identify_date_columns(df)
            if date_cols:
                file_summary['date_columns'] = {}
                for col in date_cols:
                    try:
                        date_col = pd.to_datetime(df[col], errors='coerce')
                        valid_dates = date_col.dropna()
                        if len(valid_dates) > 0:
                            file_summary['date_columns'][col] = {
                                'min_date': valid_dates.min().strftime('%Y-%m-%d'),
                                'max_date': valid_dates.max().strftime('%Y-%m-%d'),
                                'count': len(valid_dates)
                            }
                    except:
                        continue
            
            summary[filename] = file_summary
        
        return summary
    
    def _create_system_prompt(self, data_summary):
        """
        Create system prompt with data context
        
        Args:
            data_summary (dict): Summary of the data
            
        Returns:
            str: System prompt for the AI
        """
        prompt = """
        You are an expert financial data analyst AI assistant. You help users analyze invoice and financial data.
        You can respond in both Portuguese and English, matching the language of the user's question.
        
        You have access to the following data:
        
        """
        
        for filename, summary in data_summary.items():
            prompt += f"\n### File: {filename}\n"
            prompt += f"- Rows: {summary['rows']:,}\n"
            prompt += f"- Columns: {', '.join(summary['columns'])}\n"
            
            if 'financial_columns' in summary:
                prompt += "\n#### Financial Data:\n"
                for col, stats in summary['financial_columns'].items():
                    prompt += f"- {col}: Total: {stats['total']:,.2f}, Average: {stats['average']:,.2f}, Range: {stats['min']:,.2f} - {stats['max']:,.2f}\n"
            
            if 'date_columns' in summary:
                prompt += "\n#### Date Ranges:\n"
                for col, date_info in summary['date_columns'].items():
                    prompt += f"- {col}: {date_info['min_date']} to {date_info['max_date']} ({date_info['count']:,} records)\n"
            
            prompt += "\n#### Sample Data:\n"
            for col, samples in summary['sample_data'].items():
                if samples:
                    prompt += f"- {col}: {', '.join([str(s) for s in samples[:3]])}\n"
        
        prompt += """
        
        Guidelines for responses:
        1. Always be specific and use actual data from the files
        2. Include calculations and show your work when relevant
        3. Format numbers appropriately with commas and currency symbols
        4. Respond in the same language as the question (Portuguese or English)
        5. If you cannot find specific data to answer a question, clearly state what information is missing
        6. For financial data, assume Brazilian Real (R$) unless specified otherwise
        7. When analyzing trends, consider date ranges and seasonal patterns
        8. Provide actionable insights when possible
        """
        
        return prompt
    
    def _identify_financial_columns(self, df):
        """Identify financial columns in DataFrame"""
        financial_keywords = [
            'valor', 'value', 'amount', 'total', 'price', 'preço', 'preco',
            'custo', 'cost', 'receita', 'revenue', 'vendas', 'sales',
            'faturamento', 'billing', 'pagamento', 'payment'
        ]
        
        financial_cols = []
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in financial_keywords):
                if pd.api.types.is_numeric_dtype(df[col]) or self._is_currency_column(df[col]):
                    financial_cols.append(col)
        
        return financial_cols
    
    def _identify_date_columns(self, df):
        """Identify date columns in DataFrame"""
        date_keywords = [
            'data', 'date', 'datetime', 'timestamp', 'created', 'criado',
            'vencimento', 'due', 'emissao', 'issued', 'payment_date'
        ]
        
        date_cols = []
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in date_keywords):
                date_cols.append(col)
            elif self._contains_dates(df[col]):
                date_cols.append(col)
        
        return date_cols
    
    def _is_currency_column(self, series):
        """Check if column contains currency values"""
        if series.dtype == 'object':
            sample = series.dropna().head(10)
            currency_count = 0
            for val in sample:
                if self._is_currency_string(str(val)):
                    currency_count += 1
            return currency_count > len(sample) * 0.7
        return False
    
    def _is_currency_string(self, value_str):
        """Check if string represents a currency value"""
        import re
        cleaned = re.sub(r'[R$€£¥\s,.]', '', str(value_str))
        try:
            float(cleaned)
            return True
        except:
            return False
    
    def _contains_dates(self, series):
        """Check if series contains date-like values"""
        if series.dtype == 'object':
            sample = series.dropna().head(10)
            date_count = 0
            for val in sample:
                try:
                    pd.to_datetime(val)
                    date_count += 1
                except:
                    continue
            return date_count > len(sample) * 0.5
        return False
    
    def _convert_to_numeric(self, series):
        """Convert series to numeric, handling currency formatting"""
        if pd.api.types.is_numeric_dtype(series):
            return series
        
        try:
            return pd.to_numeric(series, errors='coerce')
        except:
            pass
        
        try:
            import re
            cleaned = series.astype(str).str.replace(r'[R$€£¥\s,]', '', regex=True)
            cleaned = cleaned.str.replace(',', '.')
            return pd.to_numeric(cleaned, errors='coerce')
        except:
            return None
