import os

base_path = "project/streamlit_app"

# Define folders to create inside streamlit_app
folders = [
    f"{base_path}/vector_store",
    f"{base_path}/data"
]

# Define files and their content
files = {
    f"{base_path}/app.py": "# Main Streamlit app will go here\n",
    f"{base_path}/retriever.py": "# FAISS retrieval logic\n",
    f"{base_path}/encoder.py": "# DPR encoding logic\n",
    f"{base_path}/generator.py": "# GPT-2 / BART generation\n",
    f"{base_path}/config.py": "# Configuration variables (e.g., model names, file paths)\n",
    f"{base_path}/utils.py": "# Helper functions (e.g., load text, chunking)\n",
    f"{base_path}/data/knowledge_base.txt": "",
    f"{base_path}/requirements.txt": (
        "streamlit\n"
        "transformers\n"
        "torch\n"
        "faiss-cpu\n"
        "sentencepiece\n"
        "python-dotenv\n"
    ),
    f"{base_path}/.env.example": "OPENAI_API_KEY=your_openai_key_here\n",
    f"{base_path}/Makefile": (
        "install:\n"
        "\tpip install -r requirements.txt\n\n"
        "run:\n"
        "\tstreamlit run app.py\n\n"
        "lint:\n"
        "\tblack .\n"
    ),
    f"{base_path}/Dockerfile": (
        "FROM python:3.10\n"
        "WORKDIR /app\n"
        "COPY . .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "EXPOSE 8501\n"
        'CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]\n'
    ),
    f"{base_path}/README.md": (
        "# Streamlit RAG App\n\n"
        "## 🚀 Setup\n\n"
        "### Run locally:\n"
        "```bash\n"
        "make install\n"
        "make run\n"
        "```\n\n"
        "### Run with Docker:\n"
        "```bash\n"
        "docker build -t streamlit-rag .\n"
        "docker run -p 8501:8501 streamlit-rag\n"
        "```\n"
    )
}

def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Created folder: {folder}")

def create_files():
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Created file: {path}")

if __name__ == "__main__":
    print("🚀 Setting up full Streamlit RAG app structure inside project/streamlit_app/")
    create_folders()
    create_files()
    print("\n✅ All done! You're ready to build your app in `app.py`.")
