import os
from haystack.components.converters.docx import DOCXToDocument
from haystack.components.converters.pdfminer import PDFMinerToDocument
from haystack.components.converters.pypdf import PyPDFToDocument
from haystack.components.converters.pptx import PPTXToDocument
from haystack.components.converters.txt import TextFileToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter

class RAGPreprocessor:
    def __init__(self):
        self.converters = {
            '.pdf': PyPDFToDocument(),
            '.docx': DOCXToDocument(),
            '.pptx': PPTXToDocument(),
            '.txt': TextFileToDocument()
        }
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter()

    def detect_format(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()

    def process_file(self, file_path):
        file_format = self.detect_format(file_path)
        if file_format not in self.converters:
            raise ValueError(f"Unsupported file format: {file_format}")

        converter = self.converters[file_format]
        documents = converter.convert(file_path)
        cleaned_documents = self.cleaner.clean(documents)
        split_documents = self.splitter.split_documents(cleaned_documents)
        return split_documents