# Getting Started with Gradio

Gradio is an **open-source Python library** for creating customizable **web-based user interfaces**. It is particularly useful for deploying machine learning models and computational tools in a simple and interactive way.

---

## Key Concepts

### What is Gradio?

Gradio allows you to easily create a web interface around your Python functions. This makes it simple to share your models and tools with others via a web link.

---

## How to Set Up a Gradio Interface

### 1. Install Gradio

```bash
pip install gradio
```

### 2. Import Gradio

```python
import gradio as gr
```

### 3. Define Your Function

This is the logic or functionality you want to expose via a web interface.

```python
def my_function(input_text):
    return input_text
```

### 4. Create an Interface

Use `gr.Interface()` to specify:

* the function to execute
* the types of inputs
* the types of outputs

```python
iface = gr.Interface(fn=my_function,
                     inputs=gr.Textbox(label="Enter Text"),
                     outputs=gr.Textbox(label="Output Text"))
```

### 5. Launch the Interface

```python
iface.launch()
```

This starts a local server and provides a **local or public URL** where the web interface can be accessed.

---

## Examples

### Simple Text Input & Output

```python
def echo_text(text):
    return text

iface = gr.Interface(fn=echo_text,
                     inputs=gr.Textbox(label="Enter your message"),
                     outputs=gr.Textbox(label="Echoed message"))
iface.launch()
```

### Multiple Inputs

```python
def combine_text_and_number(text, number):
    return f"Text: {text}, Number: {number}"

iface = gr.Interface(fn=combine_text_and_number,
                     inputs=[gr.Textbox(label="Enter Text"), gr.Number(label="Enter Number")],
                     outputs=gr.Textbox(label="Output"))
iface.launch()
```

### File Upload Example

```python
def count_files(files):
    return f"Number of files uploaded: {len(files)}"

iface = gr.Interface(fn=count_files,
                     inputs=gr.File(file_types=None, label="Upload Files", file_count="multiple"),
                     outputs=gr.Textbox(label="File Count"))
iface.launch()
```

---

## Summary

* Gradio makes it easy to turn Python functions into web apps.
* Setup steps:

  1. Write Python function
  2. Create Gradio interface using `gr.Interface`
  3. Launch the interface
  4. Access via local/public URL
* You can create interfaces with text inputs, numbers, and file uploads.

For more details, visit the [Gradio documentation](https://gradio.app/docs/).

Steps
- pip install gradio

![alt text](image.png)

