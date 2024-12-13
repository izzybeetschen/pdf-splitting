from pypdf import *
import os
import re

def get_file(file_path):
    """
    Gets the given file

    Args:
        file_path (Str): path to the given file
    
    Returns:
        PdfReader: a variable containing the file 

    Raises:
        UnboundLocalError: raised if the file is not found
    """
    try:
        reader = PdfReader(file_path)
    except UnboundLocalError:
        print(f"File at {file_path} not found")
    except:
        print("Unknown error")
    return reader

def find_index_page(reader):
    """
    Finds the contents page of the textbook

    Args:
        reader (PdfReader): a variable containing the textbook file
    
    Returns:
        int or None: 
            returns the page number containing the contents page or None if no contents page is found

    """
    keywords = [
        'contents',
        'table of contents'
    ]

    n = 0

    while n < len(reader.pages):
        page = reader.pages[n]
        text = page.extract_text()
        text = text.lower()     # sets text to lowercase

        for keyword in keywords:
            if keyword in text:
                pattern = r"\w+[\s\.\-]+\d+"    # checks pattern to ensure contents page
                if re.search(pattern, text):
                    return n + 1

        n += 1

    return None
