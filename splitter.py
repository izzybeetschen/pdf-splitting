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
                    return n

        n += 1

    return None

def get_page_offset(reader):
    """
    Calculates the difference between pypdf page numbers and page numbers on textbook pages

    Args:
        reader (PdfReader): a variable containing the textbook file

    Returns:
        int or None:
            returns the offset value or None if it cannot be found
    
    Raises:
        IndexError: raised if no text is found on the given page
    """
    offset = None
    for n in range(len(reader.pages)):
        page = reader.pages[n]
        page_text = page.extract_text()
        lines = page_text.splitlines()

        try:
            bottom_text = lines[-1].strip()
        except IndexError:
            bottom_text = "No text found"
        
        if bottom_text == "1":
            offset = n
            return offset
        elif bottom_text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            offset = n - int(bottom_text)
            return offset
        
        try:
            top_text = next((line.strip() for line in lines if line.strip() != "ptg8286261"), "None")
        except IndexError:
            top_text = "No text found"
        if top_text == "1":
            offset = n
            return offset
        elif top_text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            offset = n - (int(top_text) - 1)
            return offset
    return offset
