import os
import logging
from haystack import Document
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from typing import List, Union, Dict, Any, Optional
from pathlib import Path

from PPTXToDocument import CustomPPTXToDocument
from DOCXToDocument import CustomDOCXToDocument

# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RAGPreprocessor:
    def __init__(self):
        self.converters = {
            '.pdf': PyPDFToDocument(),
            '.docx': CustomDOCXToDocument(),
            '.pptx': CustomPPTXToDocument(),
            '.txt': lambda x: {"documents": [Document(content=open(x, 'r').read())]}
        }
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(split_by="sentence", split_length=3)

    def detect_format(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()

    def process_file(self, file_path: Union[str, Path]) -> List[Document]:
        try:
            file_format = self.detect_format(file_path)
            if file_format not in self.converters:
                raise ValueError(f"Unsupported file format: {file_format}")

            converter = self.converters[file_format]
            logging.info(f"{GREEN}Converting file: {file_path}{RESET}")  
            
            # Use the appropriate converter
            if file_format in ['.docx', '.pptx']:
                converted_docs = converter.run(sources=[file_path])
            else:
                converted_docs = converter.run(sources=[str(file_path)])
            
            documents = converted_docs["documents"]

            logging.info(f"{YELLOW}Cleaning documents{RESET}")  
            cleaned_docs = self.cleaner.run(documents=documents)
            cleaned_documents = cleaned_docs["documents"]

            logging.info(f"{YELLOW}Splitting documents{RESET}")  
            split_docs = self.splitter.run(documents=cleaned_documents)
            split_documents = split_docs["documents"]

            logging.info(f"Processed {len(split_documents)} document chunks")
            return split_documents
        
        except Exception as e:
            logging.error(f"{RED}Error processing file {file_path}: {str(e)}{RESET}")  
            raise

    def process_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        try:
            if metadata is None:
                metadata = {}
            document = Document(content=text, meta=metadata)

            logging.info(f"{YELLOW}Cleaning text document{RESET}")  
            cleaned_docs = self.cleaner.run(documents=[document])
            cleaned_document = cleaned_docs["documents"][0]

            logging.info(f"{YELLOW}Splitting text document{RESET}")  
            split_docs = self.splitter.run(documents=[cleaned_document])
            split_documents = split_docs["documents"]

            logging.info(f"Processed {len(split_documents)} text chunks")
            return split_documents
        
        except Exception as e:
            logging.error(f"{RED}Error processing text: {str(e)}{RESET}")  
            raise
