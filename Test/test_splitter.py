import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.errors import *
import splitter
import zipfile
from io import BytesIO

def test_get_file_exists():
    path_file = "test-pdfs/SE.pdf"
    reader = splitter.get_file(path_file)
    assert isinstance(reader, PdfReader)

def test_get_file_nonexistant():
    path_file = "test-pdfs/AI.pdf"
    reader = splitter.get_file(path_file)
    assert reader is None

def test_get_file_not_pdf():
    path_file = "test-pdfs/x.txt"
    with pytest.raises(ValueError):
        splitter.get_file(path_file)

def test_find_index_page_ds():
    path_file = "test-pdfs/DS.pdf"
    reader = splitter.get_file(path_file)
    page = splitter.find_index_page(reader)
    assert page == 5

def test_find_index_page_se():
    path_file = "test-pdfs/SE.pdf"
    reader = splitter.get_file(path_file)
    page = splitter.find_index_page(reader)
    assert page == 11

def test_find_index_page_os():
    path_file = "test-pdfs/OS.pdf"
    reader = splitter.get_file(path_file)
    page = splitter.find_index_page(reader)
    assert page == 10

def test_get_page_offset_se():
    path_file = "test-pdfs/SE.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    assert offset == 45

def test_get_page_offset_ds():
    path_file = "test-pdfs/DS.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    assert offset == 1

def test_get_page_offset_os():
    path_file = "test-pdfs/OS.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    assert offset == 22

def test_find_chapter_pages_se():
    path_file = "test-pdfs/SE.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    page = splitter.find_index_page(reader)
    chapters = splitter.find_chapter_pages(reader, page, offset)
    assert chapters == {
        "1": str(1 + offset),
        "2": str(13 + offset),
        "3": str(29 + offset),
        "4": str(61 + offset),
        "5": str(79 + offset),
        "6": str(99 + offset),
        "7": str(119 + offset),
        "8": str(139 + offset),
        "9": str(165 + offset),
        "10": str(185 + offset),
        "11": str(195 + offset),
        "12": str(213 + offset),
        "13": str(225 + offset),
        "14": str(247 + offset),
        "15": str(257 + offset),
        "16": str(267 + offset),
        "17": str(287 + offset),
        "18": str(307 + offset),
        "19": str(335 + offset),
        "20": str(347 + offset),
        "21": str(363 + offset),
        "22": str(375 + offset),
        "23": str(395 + offset)
    }

def test_find_chapter_pages_ds():
    path_file = "test-pdfs/DS.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    page = splitter.find_index_page(reader)
    chapters = splitter.find_chapter_pages(reader, page, offset)
    assert chapters == {
        "1": str(17 + offset),
        "2": str(53 + offset),
        "3": str(97 + offset),
        "4": str(161 + offset),
        "5": str(201 + offset),
        "6": str(245 + offset),
        "7": str(295 + offset),
        "8": str(351 + offset),
        "9": str(397 + offset),
        "10": str(439 + offset),
        "11": str(479 + offset),
        "12": str(537 + offset),
        "13": str(581 + offset),
        "14": str(611 + offset),
        "15": str(645 + offset),
        "16": str(691 + offset),
        "17": str(743 + offset),
        "18": str(781 + offset),
        "19": str(833 + offset),
        "20": str(897 + offset),
        "21": str(931 + offset)
    }

def test_find_chapter_pages_os():
    path_file = "test-pdfs/OS.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    page = splitter.find_index_page(reader)
    chapters = splitter.find_chapter_pages(reader, page, offset)
    assert chapters == {
        "1": "23",
        "2": "25",
        "3": "45",
        "4": "47",
        "5": "59",
        "6": str(49 + offset),
        "7": str(65 + offset),
        "8": str(77 + offset),
        "9": str(89 + offset),
        "10": str(103 + offset),
        "11": str(117 + offset),
        "12": str(119 + offset),
        "13": str(121 + offset),
        "14": str(131 + offset),
        "15": str(141 + offset),
        "16": str(155 + offset),
        "17": str(167 + offset),
        "18": str(185 + offset),
        "19": str(199 + offset),
        "20": str(215 + offset),
        "21": str(231 + offset),
        "22": str(243 + offset),
        "23": str(261 + offset),
        "24": str(279 + offset),
        "25": str(285 + offset),
        "26": str(287 + offset),
        "27": str(303 + offset),
        "28": str(315 + offset),
        "29": str(337 + offset),
        "30": str(351 + offset),
        "31": str(367 + offset),
        "32": str(385 + offset),
        "33": str(401 + offset),
        "34": str(413 + offset),
        "35": str(417 + offset),
        "36": str(419 + offset),
        "37": str(433 + offset),
        "38": str(449 + offset),
        "39": str(467 + offset),
        "40": str(493 + offset),
        "41": str(511 + offset),
        "42": str(525 + offset),
        "43": str(547 + offset),
        "44": str(563 + offset),
        "45": str(587 + offset),
        "46": str(601 + offset),
        "47": str(603 + offset),
        "48": str(605 + offset),
        "49": str(621 + offset),
        "50": str(639 + offset),
        "51": str(653 + offset)
    }

# Mock PDF creation helper
def create_mock_pdf(page_count):
    """Creates a mock PDF with the specified number of pages."""
    writer = PdfWriter()
    for i in range(page_count):
        writer.add_blank_page(width=72, height=72)  # Add blank pages
    pdf_buffer = BytesIO()
    writer.write(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# Test 1: Valid chapter split
def test_split_by_chapter_valid():
    pdf_buffer = create_mock_pdf(10)  # Create a 10-page mock PDF
    reader = PdfReader(pdf_buffer)
    chapters = {
        "1": "1",
        "2": "4",
        "3": "7"
    }
    
    zip_buffer = splitter.split_by_chapter(reader, chapters)
    assert isinstance(zip_buffer, BytesIO)

    # Check contents of the ZIP
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files = zip_file.namelist()
        assert "chapter_1.pdf" in files
        assert "chapter_2.pdf" in files
        assert "chapter_3.pdf" in files
        assert len(files) == 3

# Test 2: Single chapter covering all pages
def test_split_by_chapter_single_chapter():
    pdf_buffer = create_mock_pdf(5)  # Create a 5-page mock PDF
    reader = PdfReader(pdf_buffer)
    chapters = {
        "1": "1"
    }
    
    zip_buffer = splitter.split_by_chapter(reader, chapters)
    assert isinstance(zip_buffer, BytesIO)

    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files = zip_file.namelist()
        assert "chapter_1.pdf" in files
        assert len(files) == 1

# Test 3: Empty chapter input
def test_split_by_chapter_empty_chapters():
    pdf_buffer = create_mock_pdf(5)
    reader = PdfReader(pdf_buffer)
    chapters = {}
    
    zip_buffer = splitter.split_by_chapter(reader, chapters)
    assert isinstance(zip_buffer, BytesIO)

    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files = zip_file.namelist()
        assert len(files) == 0  # No chapters, no files

# Test 4: Invalid chapter input (non-numeric pages)
def test_split_by_chapter_invalid_chapters():
    pdf_buffer = create_mock_pdf(5)
    reader = PdfReader(pdf_buffer)
    chapters = {
        "1": "a",  # Invalid page number
        "2": "4"
    }
    
    with pytest.raises(ValueError):
        splitter.split_by_chapter(reader, chapters)

def test_split_by_chapter_invalid_page_range():
    pdf_buffer = create_mock_pdf(5)
    reader = PdfReader(pdf_buffer)
    chapters = {
        "1": "8"  # Beyond total pages
    }
    
    with pytest.raises(IndexError):
        splitter.split_by_chapter(reader, chapters)