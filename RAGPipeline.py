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
        You are an AI assistant tasked with providing accurate and concise answers based on the given context. Follow these guidelines:

        1. Carefully read and analyze all provided context.
        2. Answer the question using ONLY the information from the context.
        3. If the context doesn't contain sufficient information to answer the question fully, state this clearly.
        4. Do not make assumptions or add information beyond what's provided.
        5. If there are contradictions in the context, point them out.
        6. Use direct quotes from the context when appropriate, citing the source.
        7. Aim for clarity and brevity, limiting your answer to about 100 words.

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
