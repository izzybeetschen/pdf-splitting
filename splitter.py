from pypdf import *
from pypdf.errors import *
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
    reader = None

    try:
        reader = PdfReader(file_path)
    except UnboundLocalError:
        print(f"File at {file_path} not found")
    except PdfReadError:
        print("Invalid PDF file")
    except:
        print("Unknown error")

    if not reader:
        raise PdfReadError
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

        n += 1      #increment n

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
            continue
        
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

def find_chapter_pages(reader, contents, offset):
    """
    Finds the page number for the start of each chapter in the textbook

    Args: 
        reader (PdfReader): a variable containing the textbook file
        contents (int): a variable containing the page number of the index file
        offset (int): a variable representing the difference between the PDF page numbers and actual page numbers

    Returns:
        dict: a dictionary containing each chapter and the corresponding page number
    """
    chapters = {}
    current_page = contents
    pattern = r"^(?:Chapter\s*)?(\d+)[^\d\n]*\s+(\d+)$"

    while current_page < len(reader.pages):
        page = reader.pages[current_page]
        text = page.extract_text()

        if not text:
            current_page += 1
            continue
        
        lines = text.splitlines()
        chapter_found = False
        combined_line = " "

        for i, line in enumerate(lines):
            line = line.strip()
            # normalises the text in case of bad image reading
            normalized_line = re.sub(r'\s+', ' ', line)
            normalized_line = re.sub(r'(\d)([A-Za-z])', r'\1 \2', normalized_line)
            normalized_line = re.sub(r'([A-Za-z])(\d)$', r'\1 \2', normalized_line)
            normalized_line = re.sub(r'(\d)\s+(\d)', r'\1\2', normalized_line)

            match = re.search(pattern, normalized_line)

            if match:
                chapter_found = True
                chapter_no, chapter_page = match.groups()
                chapter_page = int(chapter_page) + int(offset)
                chapters.update({str(chapter_no): str(chapter_page)})

            # allows multi line reading incase title spans two lines
            elif i + 1 < len(lines):
                combined_line = line + " " + lines[i + 1].strip()
                # normalises the text in case of bad image reading
                normalized_line = re.sub(r'\s+', ' ', combined_line)
                normalized_line = re.sub(r'(\d)([A-Za-z])', r'\1 \2', normalized_line)
                normalized_line = re.sub(r'([A-Za-z])(\d)$', r'\1 \2', normalized_line)
                normalized_line = re.sub(r'(\d)\s+(\d)', r'\1\2', normalized_line)

                match = re.search(pattern, normalized_line)
                
                if match:
                    chapter_found = True
                    chapter_no, chapter_page = match.groups()
                    chapter_page = int(chapter_page) + int(offset)
                    chapters.update({str(chapter_no): str(chapter_page)})


        if not chapter_found:
            break

        current_page += 1       # moves to next page

    return chapters

def split_by_chaper(reader, chapter):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Practice-output")

    chapter_list = sorted((int(key), int(value)) for key, value in chapter.items())
    for i, (chapter_number, start_page) in enumerate(chapter_list):
        writer = PdfWriter()

        if i + 1 < len(chapter_list):
            end_page = chapter_list[i+1][1]
        else:
            end_page = len(reader.pages)

        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num - 1])

        output_file = os.path.join(desktop_path, f'chapter{chapter_number}.pdf')
        with open(output_file, 'wb') as out:
            writer.write(out)

def main():
    file_path = "test-pdfs/SE.pdf"
    reader = get_file(file_path)
    contents = find_index_page(reader)
    offset = get_page_offset(reader)
    chapter = find_chapter_pages(reader, contents, offset)
    split_by_chaper(reader, chapter)

main()