# build_rag_index.py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
DOC_PATH = os.path.join(os.path.dirname(__file__), "cat-facts.txt")

def build_index():
    loader = TextLoader(DOC_PATH, encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(INDEX_PATH, exist_ok=True)
    vectorstore.save_local(INDEX_PATH)
    print("✅ RAG index built and saved to:", INDEX_PATH)

if __name__ == "__main__":
    build_index()
