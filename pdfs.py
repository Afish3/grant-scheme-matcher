from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
import pickle
import os
# from langchain.document_loaders import TextLoader
# from langchain.docstore.document import Document

class Pdf:
    """
    Class that reads a pdf file of words.
    """

    def __init__(self, path) -> None:
        """Initializes an instance of the class."""
        self.path = path
        self.read = self.read_pdf()
        print(self.__str__())

    def __str__(self) -> str:
        return f"{len(self.read)} words read"
    
    def read_pdf(self):
        text = ""
        pdf_reader = PdfReader(self.path)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    @classmethod
    def chunk_pdf_text(self, text):
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text)
        return chunks
    
    @classmethod
    def get_embedded_text_chunks(self, chunks):
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        # file_name = self.path[:-4]
        if os.path.exists("all_grants.pkl"):
            with open("all_grants.pkl", "rb") as f:
                knowledge_base = pickle.load(f)
        else:
            embeddings = OpenAIEmbeddings()
            knowledge_base = FAISS.from_texts(texts=chunks, embedding=embeddings)
            with open("all_grants.pkl", "wb") as f:
                pickle.dump(knowledge_base, f)

        return knowledge_base
    