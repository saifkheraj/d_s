import os

# Define all directories to create
folders = [
    "project/backend/data",
    "project/backend/vector_store",
    "project/frontend",
    "project/streamlit_app/utils",
    "project/notebooks"
]

# Define empty files to create
files = [
    "project/backend/index.js",
    "project/backend/retriever.js",
    "project/backend/rag.js",
    "project/backend/data/knowledge_base.txt",
    "project/backend/vector_store/index.json",
    "project/backend/.env",
    "project/frontend/index.html",
    "project/frontend/script.js",
    "project/streamlit_app/app.py",
    "project/streamlit_app/requirements.txt",
    "project/streamlit_app/utils/retriever.py",
    "project/notebooks/RAG_prototype.ipynb",
    "Makefile",
    "Dockerfile",
    "docker-compose.yml",
    "README.md",
    ".gitignore"
]

def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}")

def create_files():
    for file in files:
        with open(file, "w") as f:
            f.write("")  # Create empty file
        print(f"📄 Created file: {file}")

if __name__ == "__main__":
    print("🚀 Setting up RAG project structure...")
    create_folders()
    create_files()
    print("\n🎉 Setup complete! You can now start filling in your code.")

