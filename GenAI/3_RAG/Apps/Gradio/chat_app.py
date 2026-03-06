# Import necessary packages
from transformers import pipeline
import gradio as gr

# Use a very small model for CPU
model_name = "google/flan-t5-base"


# Load text2text-generation pipeline
generator = pipeline(
    "text2text-generation",
    model=model_name,
    max_length=256,
)

def generate_response(prompt_txt):
    detailed_prompt = f"Provide a long and detailed answer to the following question: {prompt_txt}"
    generated = generator(detailed_prompt)
    return generated[0]['generated_text']

# Create Gradio interface
chat_application = gr.Interface(
    fn=generate_response,
    allow_flagging="never",
    inputs=gr.Textbox(label="Input", lines=2, placeholder="Type your question here..."),
    outputs=gr.Textbox(label="Output"),
    title="Tiny LLM Chatbot (FLAN-T5-Small)",
    description="Ask any question and the chatbot will try to answer."
)

# Launch the app
chat_application.launch(server_name="127.0.0.1", server_port=7860)
