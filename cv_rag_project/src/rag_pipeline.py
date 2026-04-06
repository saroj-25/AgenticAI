import json 
import re
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from src.prompt_template import SYSTEM_PROMPT, USER_PROMPT

CHROMA_DIR = "data/chromadb"

def get_vector_store(embedding_model : str = "nomic-embed-text")-> Chroma:
    embeddings = OllamaEmbeddings(model = embedding_model)

    return Chroma(
        persist_directory=CHROMA_DIR, 
        embedding_function= embeddings
    )

def extract_json(text: str) -> dict: 
    text = text.strip()

    try: 
        return json.loads(text)

    except json.JSONDecodeError:
        pass 

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match: 
        return json.loads(match.group(0))
    
    raise ValueError("Model donot return valid JSON ")

def evaluate_candidate(
        vector_store: Chroma, 
        cv_filename: str, 
        job_description: str, 
        llm_model: str = "llama3", 
        top_k: int = 4

    )-> dict: 
    retriever = vector_store.as_retriever(
        search_kwargs = {"k":top_k, "filter":{"source":cv_filename}}
    )

    docs = retriever.invoke(job_description)
    retrieved_cv_chunks = "\n\n".join(docs.page_content for doc in docs)

    promt = USER_PROMPT.format(
        job_description = job_description, 
        retrieved_cv_chunks= retrieved_cv_chunks
    )

    llm = ChatOllama(
        model=llm_model, 
        temperature= 0
    )

    messages = [
        ("system", SYSTEM_PROMPT), 
        ("human", promt)
    ]

    response = llm.invoke(messages)

    result = extract_json(response.content)

    result["cv_file"] = cv_filename

    return result





