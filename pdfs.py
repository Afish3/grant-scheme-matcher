from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pickle
import os

class Pdf:
    """
    Class that contains methods to work with pdf file embeddiings.
    """

    def __init__(self, path) -> None:
        """Initializes an instance of the class."""
        self.path = path
        self.read = self.read_pdf()
        print(self.__str__())

    def __str__(self) -> str:
        return f"{len(self.read)} words read"
    
    def read_pdf(self):
        """Reads the pdf document and creates a string representation of the entire text."""
        text = ""
        pdf_reader = PdfReader(self.path)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    @classmethod
    def chunk_pdf_text(self, text):
        """Returns chunks of text from a PDF document text string.
        
        This ensures that the LLM will be able to handle all the text.
        """
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
        """Text chunks are embedded using OpenAIEmbeddings and FAISS vectorstore. 
        
        The vector representation is then dumped into a pickle file.

        Note: Make sure that the appropriate API keys are defined eiither as environment variables or directly within this function.
        """
        if os.path.exists("all_grants.pkl"):
            with open("all_grants.pkl", "rb") as f:
                knowledge_base = pickle.load(f)
        else:
            embeddings = OpenAIEmbeddings()
            knowledge_base = FAISS.from_texts(texts=chunks, embedding=embeddings)
            with open("all_grants.pkl", "wb") as f:
                pickle.dump(knowledge_base, f)

        return knowledge_base
    