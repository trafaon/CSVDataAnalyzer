import pandas as pd
import numpy as np
from datetime import datetime
import locale
import re

class CSVProcessor:
    """Processes CSV data and provides financial analysis"""
    
    def __init__(self):
        self.financial_keywords = [
            'valor', 'value', 'amount', 'total', 'price', 'preço', 'preco',
            'custo', 'cost', 'receita', 'revenue', 'vendas', 'sales',
            'faturamento', 'billing', 'pagamento', 'payment'
        ]
        
        self.date_keywords = [
            'data', 'date', 'datetime', 'timestamp', 'created', 'criado',
            'vencimento', 'due', 'emissao', 'issued', 'payment_date'
        ]
    
    def identify_financial_columns(self, df):
        """
        Identify columns that likely contain financial data
        
        Args:
            df: pandas DataFrame
            
        Returns:
            list: List of column names that likely contain financial data
        """
        financial_cols = []
        
        for col in df.columns:
            col_lower = col.lower().strip()
            
            # Check if column name contains financial keywords
            if any(keyword in col_lower for keyword in self.financial_keywords):
                # Check if column contains numeric data
                if pd.api.types.is_numeric_dtype(df[col]):
                    financial_cols.append(col)
                # Check if it's a string that might be formatted currency
                elif df[col].dtype == 'object':
                    # Try to convert sample values to see if they're currency
                    sample_values = df[col].dropna().head(10)
                    numeric_count = 0
                    for val in sample_values:
                        if self._is_currency_string(str(val)):
                            numeric_count += 1
                    
                    if numeric_count > len(sample_values) * 0.7:  # 70% threshold
                        financial_cols.append(col)
        
        return financial_cols
    
    def identify_date_columns(self, df):
        """
        Identify columns that likely contain date data
        
        Args:
            df: pandas DataFrame
            
        Returns:
            list: List of column names that likely contain date data
        """
        date_cols = []
        
        for col in df.columns:
            col_lower = col.lower().strip()
            
            # Check if column name contains date keywords
            if any(keyword in col_lower for keyword in self.date_keywords):
                date_cols.append(col)
            # Check if column contains date-like data
            elif self._contains_dates(df[col]):
                date_cols.append(col)
        
        return date_cols
    
    def get_financial_summary(self, df):
        """
        Generate financial summary from DataFrame
        
        Args:
            df: pandas DataFrame
            
        Returns:
            dict: Dictionary with financial metrics
        """
        financial_cols = self.identify_financial_columns(df)
        
        if not financial_cols:
            return None
        
        summary = {}
        
        for col in financial_cols:
            # Convert to numeric if needed
            numeric_col = self._convert_to_numeric(df[col])
            
            if numeric_col is not None and len(numeric_col.dropna()) > 0:
                total = numeric_col.sum()
                avg = numeric_col.mean()
                count = len(numeric_col.dropna())
                
                # Format numbers with locale
                try:
                    total_formatted = self._format_currency(total)
                    avg_formatted = self._format_currency(avg)
                except:
                    total_formatted = f"{total:,.2f}"
                    avg_formatted = f"{avg:,.2f}"
                
                summary[f"Total {col}"] = total_formatted
                summary[f"Avg {col}"] = avg_formatted
                summary[f"Count {col}"] = f"{count:,}"
        
        return summary if summary else None
    
    def get_column_info(self, df):
        """
        Get detailed information about DataFrame columns
        
        Args:
            df: pandas DataFrame
            
        Returns:
            pandas DataFrame: DataFrame with column information
        """
        info_data = []
        
        for col in df.columns:
            col_data = df[col]
            
            info = {
                'Column': col,
                'Data Type': str(col_data.dtype),
                'Non-Null Count': col_data.notna().sum(),
                'Null Count': col_data.isna().sum(),
                'Unique Values': col_data.nunique(),
            }
            
            # Add sample values
            sample_values = col_data.dropna().head(3).tolist()
            info['Sample Values'] = ', '.join([str(val) for val in sample_values])
            
            # Check if it's a financial column
            if col in self.identify_financial_columns(df):
                info['Type'] = 'Financial'
            elif col in self.identify_date_columns(df):
                info['Type'] = 'Date'
            else:
                info['Type'] = 'Other'
            
            info_data.append(info)
        
        return pd.DataFrame(info_data)
    
    def get_date_range_summary(self, df):
        """
        Get date range summary from DataFrame
        
        Args:
            df: pandas DataFrame
            
        Returns:
            dict: Dictionary with date range information
        """
        date_cols = self.identify_date_columns(df)
        
        if not date_cols:
            return None
        
        summary = {}
        
        for col in date_cols:
            try:
                # Try to convert to datetime
                date_col = pd.to_datetime(df[col], errors='coerce')
                valid_dates = date_col.dropna()
                
                if len(valid_dates) > 0:
                    min_date = valid_dates.min()
                    max_date = valid_dates.max()
                    
                    summary[f"{col} Range"] = f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
                    summary[f"{col} Count"] = len(valid_dates)
            except:
                continue
        
        return summary if summary else None
    
    def _is_currency_string(self, value_str):
        """Check if string represents a currency value"""
        # Remove common currency symbols and separators
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
            # Try direct conversion first
            return pd.to_numeric(series, errors='coerce')
        except:
            pass
        
        # If that fails, try cleaning currency formatting
        try:
            cleaned = series.astype(str).str.replace(r'[R$€£¥\s,]', '', regex=True)
            cleaned = cleaned.str.replace(',', '.')  # Handle decimal comma
            return pd.to_numeric(cleaned, errors='coerce')
        except:
            return None
    
    def _format_currency(self, value):
        """Format number as currency"""
        try:
            return locale.currency(value, grouping=True)
        except:
            return f"R$ {value:,.2f}"
