from pypdf import *
import os
import re

def get_file(file_path):
    try:
        reader = PdfReader(file_path)
    except UnboundLocalError:
        print(f"File at {file_path} not found")
    except:
        print("Unknown error")
    return reader

def find_index_page(reader):
    keywords = [
        'contents',
        'table of contents'
    ]

    n = 0

    while n < len(reader.pages):
        page = reader.pages[n]
        text = page.extract_text()
        text = text.lower()

        for keyword in keywords:
            if keyword in text:
                pattern = r"\w+[\s\.\-]+\d+"
                if re.search(pattern, text):
                    return n + 1

        n += 1

    return None
