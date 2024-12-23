# rag_cli.py
import os
import random
import argparse
import warnings
from colorama import Fore, Style, init
# from .RAGPipeline import RAGPipeline
# from .Spinner import Spinner
# from .utils import format_answer, clear_terminal, load_environment

from FeynmanAI.RAGPipeline import RAGPipeline
from FeynmanAI.Spinner import Spinner
from FeynmanAI.utils import format_answer, clear_terminal, load_environment

# Initialize colorama
init(autoreset=True)

warnings.filterwarnings("ignore", 
                        category=FutureWarning, 
                        message="The `use_auth_token` argument is deprecated")

def parse_arguments():
    parser = argparse.ArgumentParser(description="RAG Command-Line Tool for Local Documents")
    parser.add_argument("-d", "--document", help="Path to the document file")
    parser.add_argument("-cls","--clear",  action="store_true",  help="Clear screen after each query")
    parser.add_argument("-qz", "--quiz",   action="store_true",  help="Quiz me based on my documents(Quiz Mode)")
    parser.add_argument("-rd", "--read",   action="store_true",  help="Reads the Answer for you")
    parser.add_argument("-v", "--version", action="version",     version="RAG CLI Tool 1.0.0")
    return parser.parse_args()

def interactive_query_loop(rag, clear_screen):
    """Interactive loop for querying the RAG model."""
    while True:
        question = input(f"\n{Fore.GREEN}Enter your question (or 'quit' to exit, 'clear' to clear screen):{Style.RESET_ALL} \n")
        if question.lower() == 'quit':
            break
        elif question.lower() == 'clear':
            clear_terminal()
            continue

        with Spinner("Processing your question"):
            answer = rag.run_pipeline(question, mode="answer")
        
        formatted_answer = format_answer(answer)
        print(f"\n{Fore.BLUE}Answer:{Style.RESET_ALL}")
        print(formatted_answer)

        if clear_screen:
            input(f"{Fore.YELLOW}Press Enter to clear the screen...{Style.RESET_ALL}")
            clear_terminal()

def quiz_mode(rag, clear_screen):
    # Quiz mode for testing User's Knowledge
    print(f"{Fore.CYAN}Entering Quiz Mode. Type 'quit' to exit quiz mode.{Style.RESET_ALL}")

    while True:
        topics = rag.get_document_topics()
        topic = random.choice(topics)

        with Spinner("Generating Questions"):
            question = rag.run_pipeline(topic, mode="quiz")

        print(f"\n{Fore.GREEN}Question:{Style.RESET_ALL} {question}")
        user_answer = input(f"{Fore.YELLOW}Your answer:{Style.RESET_ALL} ")

        if user_answer.lower() == 'quit':
            break

        with Spinner("Evaluating answer"):
            feedback = rag.run_pipeline(f"{question}|||{user_answer}", mode="evaluate")

        print(f"\n{Fore.BLUE}Feedback:{Style.RESET_ALL}")
        print(format_answer(feedback))
        
        if clear_screen:
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            clear_terminal()

def main():
    """Main function to run the script."""
    args = parse_arguments()
    hf_token = load_environment()

    try:
        rag = RAGPipeline(hf_token=hf_token)

        if args.document:
            with Spinner(f"Adding document '{args.document}'"):
                rag.add_document(args.document)

        if args.quiz:
            quiz_mode(rag, args.clear)
        else:
            interactive_query_loop(rag, args.clear)

    except AttributeError as e:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {str(e)}")
        print("This might be due to an incompatibility with the current version of Haystack.")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred:{Style.RESET_ALL} {str(e)}")

if __name__ == "__main__":
    main()
