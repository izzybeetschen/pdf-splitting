import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pypdf import PdfReader
import splitter

def test_get_file_exists():
    path_file = "test-pdfs/SE.pdf"
    reader = splitter.get_file(path_file)
    assert isinstance(reader, PdfReader)

def test_get_file_nonexistant():
    path_file = "test-pdfs/AI.pdf"
    with pytest.raises(UnboundLocalError):
        splitter.get_file(path_file)

def test_find_index_page_ds():
    path_file = "test-pdfs/DS.pdf"
    reader = splitter.get_file(path_file)
    page = splitter.find_index_page(reader)
    assert page == 6

def test_find_index_page_se():
    path_file = "test-pdfs/SE.pdf"
    reader = splitter.get_file(path_file)
    page = splitter.find_index_page(reader)
    assert page == 12
