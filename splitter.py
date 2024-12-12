from pypdf import *
import os

def get_file(file_path):
    try:
        reader = PdfReader(file_path)
    except UnboundLocalError:
        print(f"File at {file_path} not found")
    except:
        print("Unknown error")
    
    return reader
