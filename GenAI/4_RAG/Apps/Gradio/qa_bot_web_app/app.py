# app.py
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
