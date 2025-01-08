from sentence_transformers import SentenceTransformer
from transformers import pipeline
from PyPDF2 import PdfReader
import faiss
import numpy as np

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Step 2: Split text into chunks
def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# Step 3: Create embeddings
def create_embeddings(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    return embeddings, model

# Step 4: Create FAISS index
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Step 5: Retrieve relevant chunks
def retrieve_chunks(query, index, chunks, model, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]

# Step 6: Answer generation
def generate_answer(question, context):
    print("Generating answer using open-source pipeline...")
    return f"[This is a placeholder for the response logic using context: {context}]"

# Main workflow
if __name__ == "__main__":
    pdf_path = "sample.pdf"
    
    # Extract and process text
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    embeddings, embedding_model = create_embeddings(chunks)
    index = create_faiss_index(np.array(embeddings))

    # User interaction
    print("PDF Chatbot Ready! Ask a question:")
    query = input("Your Question: ")

    # Retrieve and respond
    relevant_chunks = retrieve_chunks(query, index, chunks, embedding_model)
    context = " ".join(relevant_chunks)
    answer = generate_answer(query, context)

    print("\nAnswer:", answer)
