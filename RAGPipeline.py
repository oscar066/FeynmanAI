import os
from dotenv import load_dotenv
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret
from RAGPreprocessor import RAGPreprocessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from PromptTemplates import PromptTemplates

class RAGPipeline:
    """
    A class that implements Retrieval Augmented Generation (RAG) using Haystack components:

    Args:
        hf_token (str): HuggingFace API token for accessing Language Models

    Methods:
        add_document(file_path): Process and add a document to the pipeline.
        run_pipeline(question, mode): Run the pipeline in specified mode.
        extract_topics(): Extract topics from added documents.
        get_document_topics(): Retrieve extracted topics.

    Returns:
        Answer (str) : Models Response 
    """

    def __init__(self, hf_token):
        self.document_store = InMemoryDocumentStore()
        self.preprocessor = RAGPreprocessor()
        self.embedder = SentenceTransformersDocumentEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2")
        self.embedder.warm_up()

        # Set the HuggingFace API key
        os.environ["HF_TOKEN"] = hf_token

        self.answer_pipeline = self.create_pipeline("answer")
        self.quiz_pipeline = self.create_pipeline("quiz")
        self.evaluation_pipeline = self.create_pipeline("evaluate")

        self.documents = []
        self.topics = []

    def create_pipeline(self, mode):
        text_embedder = SentenceTransformersTextEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2")
        
        retriever = InMemoryEmbeddingRetriever(document_store=self.document_store)    
        if mode == "answer":
            prompt_builder = PromptBuilder(template=PromptTemplates.get_prompt_template())
        elif mode == "quiz":
            prompt_builder = PromptBuilder(template=PromptTemplates.get_quiz_prompt_template())
        elif mode == "evaluate":
            prompt_builder = PromptBuilder(template=PromptTemplates.get_evaluation_prompt_template())
        else:
            raise ValueError(f"Invalid mode: {mode}")

        generator = HuggingFaceAPIGenerator(api_type="serverless_inference_api",
                                            api_params={"model": "meta-llama/Meta-Llama-3-8B-Instruct"},
                                            token=Secret.from_token(os.environ["HF_TOKEN"]))

        pipeline = Pipeline()
        pipeline.add_component("text_embedder", text_embedder)
        pipeline.add_component("retriever", retriever)
        pipeline.add_component("prompt_builder", prompt_builder)
        pipeline.add_component("llm", generator)

        pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        pipeline.connect("retriever", "prompt_builder.documents")
        pipeline.connect("prompt_builder", "llm")

        return pipeline

    def add_document(self, file_path):
        documents = self.preprocessor.process_file(file_path)
        docs_with_embeddings = self.embedder.run(documents)["documents"]
        self.document_store.write_documents(docs_with_embeddings)
        self.documents.extend(documents)
        self.extract_topics()


    def run_pipeline(self, question, mode="answer"):
        if mode == "answer":
            response = self.answer_pipeline.run({"text_embedder": {"text": question}, 
                                                 "prompt_builder": {"question": question}})
        elif mode == "quiz":
            response = self.quiz_pipeline.run({"text_embedder": {"text": question}, 
                                               "prompt_builder": {"topic": question}})
        elif mode == "evaluate":
            question, user_answer = question.split("|||")
            response = self.evaluation_pipeline.run({"text_embedder": {"text": question}, 
                                                     "prompt_builder": {"question": question, "user_answer": user_answer}})
        else:
            raise ValueError(f"Invalid mode: {mode}")

        return response["llm"]["replies"][0]

    def extract_topics(self):
        # Simple topic extraction using LDA
        vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
        doc_term_matrix = vectorizer.fit_transform([doc.content for doc in self.documents])
        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        lda.fit(doc_term_matrix)
        
        feature_names = vectorizer.get_feature_names_out()
        self.topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
            self.topics.append(" ".join(top_words))

    def get_document_topics(self):
        return self.topics