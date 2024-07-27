# rag_cli.py

import argparse
import os
from dotenv import load_dotenv
from CacheRAG import CachedRAGPipeline
from Spinner import Spinner
from utils import format_answer, clear_terminal

def main():
    parser = argparse.ArgumentParser(description="RAG Command-Line Tool with Caching")
    parser.add_argument("--document", help="Path to the document file")
    parser.add_argument("--list-cache", action="store_true", help="List cached documents")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the document cache")
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Huggingface API key not found. Please set the HF_TOKEN environment variable.")

    try:
        # Create an instance of CachedRAGPipeline
        rag = CachedRAGPipeline(hf_token=hf_token)

        if args.list_cache:
            with Spinner("Fetching cached documents"):
                cached_docs = rag.list_cached_documents()
            if cached_docs:
                print("Cached documents:")
                for doc in cached_docs:
                    print(f"- {doc}")
            else:
                print("No documents in cache.")
            return

        if args.clear_cache:
            with Spinner("Clearing cache"):
                rag.clear_cache()
            return

        if args.document:
            with Spinner(f"Adding document '{args.document}'"):
                rag.add_document(args.document)

        # Interactive query loop
        while True:
            question = input("\nEnter your question (or 'quit' to exit): ")
            if question.lower() == 'quit':
                break

            with Spinner("Processing your question"):
                answer = rag.run_pipeline(question)
            
            formatted_answer = format_answer(answer)
            print("\nAnswer:")
            print(formatted_answer)

    except AttributeError as e:
        print(f"Error: {str(e)}")
        print("This might be due to an incompatibility with the current version of Haystack.")
        print("Please check the documentation or update the Haystack library.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()