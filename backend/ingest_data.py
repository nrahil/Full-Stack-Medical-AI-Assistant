import os
import uuid
import pickle
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Load environment variables from backend/.env or root .env
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv()

def ingest_pdf(file_path: str, user_id: str, document_id: str = ""):
    # Extract just the filename (e.g., "report.pdf") for metadata tagging
    filename = os.path.basename(file_path)
    print(f"--- Starting Ingestion for {filename} (User: {user_id}) ---")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # 1. Load using PyMuPDF (much more reliable)
    loader = PyMuPDFLoader(file_path)
    data = loader.load()
    print(f"  Loaded {len(data)} pages from PDF")
    
    if not data:
        raise ValueError(f"No pages could be extracted from '{filename}'.")
    
    # 2. Split into chunks (improved chunking strategy)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Smaller chunks for more precise retrieval
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(data)
    print(f"  Split into {len(docs)} chunks")
    
    if not docs:
        raise ValueError(f"No text content could be extracted from '{filename}'. Please ensure the PDF contains readable text and is not an empty or scanned document.")
    
    # 3. Tag every chunk with metadata
    doc_id = document_id or str(uuid.uuid4())
    for i, doc in enumerate(docs):
        doc.metadata["source_filename"] = filename
        doc.metadata["user_id"] = user_id
        doc.metadata["document_id"] = doc_id
        doc.metadata["chunk_id"] = f"{doc_id}_chunk_{i}"
        # PyMuPDF naturally stores 'page' in doc.metadata, but we ensure it's explicitly there
        if "page" not in doc.metadata:
            doc.metadata["page"] = 0
        
        # Placeholder for extraction/detection logic
        doc.metadata["section"] = "general"
        doc.metadata["document_type"] = "medical_report"
        doc.metadata["medical_date"] = "unknown"
        
    print(f"  Tagged all chunks with rich metadata")
    
    # 4. Create Embeddings - using HuggingFace Local Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # 5. Upload to Pinecone (Vector Search)
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if not index_name:
        raise ValueError("PINECONE_INDEX_NAME is not set in environment variables. Please check your .env file.")
    if not os.getenv("PINECONE_API_KEY"):
        raise ValueError("PINECONE_API_KEY is not set in environment variables. Please check your .env file.")
        
    PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
    print(f"  Uploaded {len(docs)} chunks to Pinecone index: '{index_name}'")
    
    # 6. Update Local BM25 Retriever (Keyword Search)
    try:
        from langchain_community.retrievers import BM25Retriever
        bm25_path = os.path.join(BASE_DIR, "bm25_retriever.pkl")
        all_docs = list(docs)
        if os.path.exists(bm25_path):
            try:
                with open(bm25_path, "rb") as f:
                    existing_retriever = pickle.load(f)
                    if hasattr(existing_retriever, "docs") and isinstance(existing_retriever.docs, list):
                        all_docs = existing_retriever.docs + docs
            except Exception as e:
                print(f"  Warning: Could not read existing BM25 index ({e}). Rebuilding new index...")
        
        bm25_retriever = BM25Retriever.from_documents(all_docs)
        with open(bm25_path, "wb") as f:
            pickle.dump(bm25_retriever, f)
        print("  BM25 keyword search index updated successfully.")
    except Exception as bm25_err:
        print(f"  Warning: BM25 indexing skipped due to error: {bm25_err}")
        
    print(f"--- Success! {len(docs)} chunks processed for {filename} ---")
    
    # 7. Return details for the frontend
    chunk_previews = []
    for i, doc in enumerate(docs[:5]):  # Show first 5 chunks as preview
        chunk_previews.append({
            "chunk_number": i + 1,
            "preview": doc.page_content[:120] + "..." if len(doc.page_content) > 120 else doc.page_content,
            "char_count": len(doc.page_content)
        })
    
    return {
        "total_pages": len(data),
        "total_chunks": len(docs),
        "chunk_previews": chunk_previews
    }

if __name__ == "__main__":
    test_pdf = os.path.join(BASE_DIR, "report.pdf")
    if os.path.exists(test_pdf):
        ingest_pdf(test_pdf, user_id="test_user")
    elif os.path.exists("report.pdf"):
        ingest_pdf("report.pdf", user_id="test_user")
    else:
        print("Error: report.pdf not found in the backend folder!")