import os

# Project folders
project_root = "qa_bot_web_app"
folders = [
    project_root,
    os.path.join(project_root, "data", "my_pdfs")
]

# Files with starter content
files = {
    os.path.join(project_root, "requirements.txt"): """langchain
langchain_community
langchain_openai
faiss-cpu
sentence-transformers
transformers
gradio
pypdf
tiktoken
""",

    os.path.join(project_root, "ingest.py"): """# ingest.py
# Load PDF, split into chunks, embed, and save vectorstore

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load PDF
loader = PyPDFLoader("data/my_pdfs/my_file.pdf")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Save vectorstore
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index")

print("Vectorstore saved to faiss_index/")
""",

    os.path.join(project_root, "rag_chain.py"): """# rag_chain.py
# Load vectorstore and build QA chain

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vectorstore
vectorstore = FAISS.load_local("faiss_index", embeddings)
retriever = vectorstore.as_retriever()

# Define LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")  # You can change to HuggingFaceHub()

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
""",

    os.path.join(project_root, "app.py"): """# app.py
# Gradio app to ask questions to PDF QA bot

from rag_chain import qa_chain
import gradio as gr

def qa_bot(query):
    result = qa_chain.run(query)
    return result

gr.Interface(fn=qa_bot,
             inputs=gr.Textbox(label="Ask a question"),
             outputs=gr.Textbox(label="Answer"),
             title="QA Bot over PDF",
             description="Ask questions based on your PDF documents.").launch()
"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("QA Bot project structure created in:", project_root)
