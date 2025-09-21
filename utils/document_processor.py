import PyPDF2
import docx
from pathlib import Path
from typing import List, Union
import re

class DocumentProcessor:
    """Handles processing of various document formats into text chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_document(self, file_path: Union[str, Path]) -> List[str]:
        """Process a document and return text chunks"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            text = self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() == '.docx':
            text = self._extract_from_docx(file_path)
        elif file_path.suffix.lower() == '.txt':
            text = self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Clean and chunk the text
        cleaned_text = self._clean_text(text)
        chunks = self._chunk_text(cleaned_text)
        
        return chunks
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        
        return text
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        
        return text
    
    def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep Vietnamese characters
        text = re.sub(r'[^\w\s\u00C0-\u024F\u1E00-\u1EFF\.,!?;:()-]', ' ', text)
        
        return text.strip()
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to end at a sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                last_period = text.rfind('.', start + self.chunk_size - 100, end)
                last_newline = text.rfind('\n', start + self.chunk_size - 100, end)
                
                sentence_end = max(last_period, last_newline)
                if sentence_end > start:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = max(start + self.chunk_size - self.chunk_overlap, end)
        
        return chunks