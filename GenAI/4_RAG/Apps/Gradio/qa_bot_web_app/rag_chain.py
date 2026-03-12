# rag_chain.py
# Load vectorstore and build QA chain

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vectorstore
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()

# Define LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")  # You can change to HuggingFaceHub()

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
