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

def test_find_chapter_pages_ds():
    path_file = "test-pdfs/DS.pdf"
    reader = splitter.get_file(path_file)
    offset = splitter.get_page_offset(reader)
    page = splitter.find_index_page(reader)
    chapters = splitter.find_chapter_pages(reader, page, offset)

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