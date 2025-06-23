import gradio as gr

# Example function
def greet(name, age, is_student, birth_date, mood):
    message = f"Hello {name}, you are {age} years old.\n"
    message += "You are a student.\n" if is_student else "You are not a student.\n"
    message += f"Your birth date: {birth_date}\n"
    message += f"Your current mood: {mood}"
    return message

# Create interface
iface = gr.Interface(
    fn=greet,
    inputs=[
        gr.Textbox(label="Enter your name"),
        gr.Number(label="Enter your age"),
        gr.Checkbox(label="Are you a student?"),
        gr.Textbox(label="Enter your birth date (YYYY-MM-DD)"),
        gr.Radio(["Happy", "Sad", "Excited", "Angry"], label="Current mood"),
    ],
    outputs=gr.Textbox(label="Greeting")
)

# Launch app
iface.launch()
