import os
from dotenv import load_dotenv
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret
from RAGPreprocessor import  RAGPreprocessor

class RAGPipelineServer:
    def __init__(self, hf_token):
        self.document_store = InMemoryDocumentStore()
        self.preprocessor = RAGPreprocessor()
        self.embedder = SentenceTransformersDocumentEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2")
        self.embedder.warm_up()
        self.retriever = InMemoryEmbeddingRetriever(document_store=self.document_store)
        self.text_embedder = SentenceTransformersTextEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2")
        self.prompt_builder = PromptBuilder(template=self.get_prompt_template())

        # Set the HuggingFace API key
        os.environ["HF_TOKEN"] = hf_token
        self.generator = HuggingFaceAPIGenerator(api_type="serverless_inference_api",
                                                 api_params={"model": "meta-llama/Meta-Llama-3-8B-Instruct"},
                                                 token=Secret.from_token(hf_token))

        self.pipeline = Pipeline()
        self.pipeline.add_component("text_embedder", self.text_embedder)
        self.pipeline.add_component("retriever", self.retriever)
        self.pipeline.add_component("prompt_builder", self.prompt_builder)
        self.pipeline.add_component("llm", self.generator)

        self.pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "llm")

    def add_document(self, file_path):
        documents = self.preprocessor.process_file(file_path)
        docs_with_embeddings = self.embedder.run(documents)["documents"]
        self.document_store.write_documents(docs_with_embeddings)

    def get_prompt_template(self):
        return """
        Given the following information, answer the question.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        Answer:
        """

    def run_pipeline(self, question):
        response = self.pipeline.run({"text_embedder": {
            "text": question}, 
            "prompt_builder": {"question": question}
            })
        return response["llm"]["replies"][0]


if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Huggingface API key not found.")
    
    # Create an instance of RAGPipelineServer
    RAG = RAGPipelineServer(hf_token=hf_token)

    # Example of adding a document
    file_path = "path/to/your/document.pdf"  # Change this to the path of your document
    RAG.add_document(file_path)

    # Example of running the pipeline
    question = "What is the main topic of the document?"
    answer = RAG.run_pipeline(question)
    print("Answer:", answer)
