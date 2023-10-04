import unittest
import os
import pickle
from pdfs import Pdf 

class TestPdfMethods(unittest.TestCase):

    def setUp(self):
        # Create a temporary PDF file for testing
        self.temp_pdf_path = "temp.pdf"
        with open(self.temp_pdf_path, "w") as f:
            f.write("This is a test PDF.")

    def tearDown(self):
        # Remove the temporary PDF file after testing
        if os.path.exists(self.temp_pdf_path):
            os.remove(self.temp_pdf_path)

    def test_read_pdf(self):
        pdf = Pdf(self.temp_pdf_path)
        text = pdf.read_pdf()
        self.assertEqual(text, "This is a test PDF.")

    def test_chunk_pdf_text(self):
        pdf = Pdf(self.temp_pdf_path)
        text = pdf.read_pdf()
        chunks = Pdf.chunk_pdf_text(text)
        self.assertIsInstance(chunks, list)
        self.assertTrue(chunks)

    # """def test_get_embedded_text_chunks(self):
    #     pdf = Pdf(self.temp_pdf_path)
    #     text = pdf.read_pdf()
    #     chunks = Pdf.chunk_pdf_text(text)

    #     # Remove the temporary knowledge base file if it exists
    #     if os.path.exists("all_grants.pkl"):
    #         os.remove("all_grants.pkl")

    #     knowledge_base = Pdf.get_embedded_text_chunks(chunks)

    #     # Check if the knowledge base file was created
    #     self.assertTrue(os.path.exists("all_grants.pkl"))

    # """