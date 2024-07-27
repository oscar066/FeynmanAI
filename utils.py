# utils.py
import os
import platform
import textwrap

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def format_answer(answer: str, max_width: int = 80) -> str:
    """
    Format the answer for better presentation.
    
    :param answer: The raw answer string
    :param max_width: Maximum width of each line
    :return: Formatted answer string
    """
    # Split the answer into paragraphs
    paragraphs = answer.split('\n')
    formatted_paragraphs = []

    for paragraph in paragraphs:
        # Check if the paragraph is a list item
        if paragraph.strip().startswith(('- ', '• ', '* ')):
            # Preserve list formatting
            wrapped = textwrap.fill(paragraph, width=max_width-2, subsequent_indent='  ')
            formatted_paragraphs.append(wrapped)
        else:
            # Wrap normal paragraphs
            wrapped = textwrap.fill(paragraph, width=max_width)
            formatted_paragraphs.append(wrapped)

    # Join the formatted paragraphs
    formatted_answer = '\n\n'.join(formatted_paragraphs)

    # Add a decorative border
    border = '─' * max_width
    return f"{border}\n{formatted_answer}\n{border}"