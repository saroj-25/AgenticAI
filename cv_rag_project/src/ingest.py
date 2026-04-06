import os 
import shutil
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from src.parser import read_cv ## importing local funciton 

UPLAD_DIR = "data/uploads"
CHORMA_DIR = "data/chroma_db"

def ensure_dir() -> None: 
    os.makedirs(UPLAD_DIR, exist_ok=True)
    os.makedirs(CHORMA_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file) -> str: 
    ensure_dir()
    file_path = os.path.join(UPLAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f: 
        f.write(uploaded_file.getbuffer())
    return file_path

def clear_vector_db() -> None:
    if os.path.exists(CHORMA_DIR):
        shutil.rmtree(CHORMA_DIR)
        os.makedirs(CHORMA_DIR, exist_ok=True)
        
def build_vector_store(file_paths:list[str], embedding_model:str = "nomic-embed-text")-> Chroma:
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200 )

    docs = []

    for file_path in file_paths: 
        text = read_cv(file_path)

        if not text.split():
            continue

        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            docs.append(
                Document(
                    page_content= chunk, 
                    metadata= {
                        "source": Path(file_path).name, 
                        "chunk_id": i
                    }
                )
            )
    embeddings = OllamaEmbeddings(model= embedding_model)

    vector_store = Chroma.from_documents(
            documents=docs,
            embedding= embeddings, 
            persist_directory= CHORMA_DIR
        )
    
    return vector_store
    



