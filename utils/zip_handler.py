import zipfile
import pandas as pd
import tempfile
import os
from io import StringIO
import streamlit as st

class ZipHandler:
    """Handles ZIP file extraction and CSV file identification"""
    
    def __init__(self):
        self.supported_encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    def extract_csv_files(self, uploaded_file):
        """
        Extract CSV files from uploaded ZIP file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            dict: Dictionary with filename as key and pandas DataFrame as value
        """
        csv_files = {}
        
        try:
            # Create temporary file to save uploaded ZIP
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Extract ZIP file
            with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Filter CSV files
                csv_file_names = [f for f in file_list if f.lower().endswith('.csv') and not f.startswith('__MACOSX/')]
                
                for csv_file in csv_file_names:
                    try:
                        # Extract CSV file content
                        with zip_ref.open(csv_file) as file:
                            content = file.read()
                            
                        # Try different encodings to read the CSV
                        df = None
                        for encoding in self.supported_encodings:
                            try:
                                # Decode content with current encoding
                                decoded_content = content.decode(encoding)
                                
                                # Try different separators
                                for sep in [',', ';', '\t', '|']:
                                    try:
                                        df = pd.read_csv(StringIO(decoded_content), sep=sep)
                                        # Check if we got meaningful data (more than 1 column)
                                        if len(df.columns) > 1:
                                            break
                                    except:
                                        continue
                                
                                if df is not None and len(df.columns) > 1:
                                    break
                                    
                            except UnicodeDecodeError:
                                continue
                        
                        if df is not None and len(df.columns) > 1:
                            # Clean column names
                            df.columns = df.columns.str.strip()
                            
                            # Get just the filename without path
                            clean_filename = os.path.basename(csv_file)
                            csv_files[clean_filename] = df
                            
                        else:
                            st.warning(f"Could not properly parse CSV file: {csv_file}")
                            
                    except Exception as e:
                        st.warning(f"Error reading CSV file {csv_file}: {str(e)}")
                        continue
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
        except zipfile.BadZipFile:
            raise Exception("Invalid ZIP file format")
        except Exception as e:
            raise Exception(f"Error extracting ZIP file: {str(e)}")
        
        return csv_files
    
    def get_file_info(self, zip_path):
        """
        Get information about files in the ZIP archive
        
        Args:
            zip_path: Path to ZIP file
            
        Returns:
            list: List of file information dictionaries
        """
        file_info = []
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    if not info.is_dir() and info.filename.lower().endswith('.csv'):
                        file_info.append({
                            'filename': os.path.basename(info.filename),
                            'size': info.file_size,
                            'compressed_size': info.compress_size,
                            'date_modified': info.date_time
                        })
        except Exception as e:
            raise Exception(f"Error reading ZIP file info: {str(e)}")
        
        return file_info
