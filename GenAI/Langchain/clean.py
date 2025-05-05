import nbformat

path = 'langchain.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

if 'widgets' in nb.metadata:
    del nb.metadata['widgets']

with open('langchain.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)