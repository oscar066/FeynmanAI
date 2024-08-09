# utils.py
import os
import platform
import textwrap
import shutil
from dotenv import load_dotenv
from colorama import Fore, Style ,init

init(autoreset=True)

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def get_terminal_size():
    """Get the width and height of the terminal."""
    return shutil.get_terminal_size()

def center_text(text, width):
    """Center a single line of text."""
    return text.center(width)

def format_answer(answer: str) -> str:
    """
    Format the answer for better presentation, adapting to screen size and centering the content.
    
    :param answer: The raw answer string
    :return: Formatted answer string
    """
    terminal_width, terminal_height = get_terminal_size()
    max_width = min(terminal_width - 4, 100)  # Leave some margin and cap at 100 chars

    # Split the answer into paragraphs
    paragraphs = answer.split('\n')
    formatted_paragraphs = []

    for paragraph in paragraphs:
        # Check if the paragraph is a list item
        if paragraph.strip().startswith(('- ', '• ', '* ')):
            # Preserve list formatting
            wrapped = textwrap.fill(paragraph, width=max_width-2, subsequent_indent='  ')
            wrapped_lines = wrapped.split('\n')
            centered_lines = [center_text(line, terminal_width) for line in wrapped_lines]
            formatted_paragraphs.extend(centered_lines)
        else:
            # Wrap normal paragraphs
            wrapped = textwrap.fill(paragraph, width=max_width)
            wrapped_lines = wrapped.split('\n')
            centered_lines = [center_text(line, terminal_width) for line in wrapped_lines]
            formatted_paragraphs.extend(centered_lines)
        
        # Add an empty line between paragraphs
        formatted_paragraphs.append('')

    # Join the formatted paragraphs
    formatted_answer = '\n'.join(formatted_paragraphs)

    # Add a decorative border
    border = center_text('─' * (max_width + 4), terminal_width)
    
    # Combine everything
    final_output = f"\n{border}\n\n{formatted_answer}\n{border}\n"

    return final_output

def load_environment():
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        print(f"{Fore.YELLOW}Huggingface Access token not found.{Style.RESET_ALL}")
        hf_token = input(f"{Fore.CYAN}Please enter your HuggingFace access token: {Style.RESET_ALL}")

        if hf_token:
            save_token = input(f"{Fore.GREEN}Do you want to save this token for future use? (y/n): {Style.RESET_ALL}")
            if save_token.lower() == 'y':
                with open(".env", "a") as f:
                    f.write(f"\nHF_TOKEN={hf_token}")
                print(f"{Fore.GREEN}Token Saved in .env file.{Style.RESET_ALL}")

            else:
                print(f"{Fore.YELLOW}Token not saved. You will need to enter it again next time. {Style.RESET_ALL}")

    else:
        print(f"{Fore.GREEN}Using Huggingface access token from .env file.{Style.RESET_ALL}")

    return hf_token