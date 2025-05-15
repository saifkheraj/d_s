# 🧠 Model Context Protocol (MCP)

**Model Context Protocol (MCP)** is an open standard designed to enable large language model (LLM) applications to integrate seamlessly with external tools, data sources, and prompt templates. Developed by Anthropic, MCP provides a modular, scalable, and secure way to build AI-powered apps without custom boilerplate for each integration.

---

## 📌 Why Use MCP?

* 🔌 **Broad Integrations**: Connect LLMs to databases, CRMs, file systems, messaging platforms, and more.
* 🧩 **Modular Architecture**: Build reusable MCP servers for each tool or resource; share them across multiple AI apps.
* 🛠️ **Simple SDKs**: Use language-specific decorators (e.g., Python) to expose functions and data with minimal code.
* 🧠 **Dynamic Prompting**: Leverage pre-defined prompt templates for consistent, structured interactions.
* 🌐 **Flexible Transports**: Support local stdio, HTTP+SSE, and streamable HTTP for both development and cloud deployments.

---

## ⚙️ Architecture Overview

MCP follows a **Client–Server** model:

| Component          | Description                                                                     |
| ------------------ | ------------------------------------------------------------------------------- |
| **Host (LLM App)** | An application embedding an LLM (e.g., Claude, IDE plugin, chatbot)             |
| **MCP Client**     | Library within the Host that communicates with MCP Servers                      |
| **MCP Server**     | Standalone process exposing Tools, Resources, and Prompt Templates via MCP      |
| **MCP Protocol**   | Defines JSON-RPC–like messages for tool invocation, resource fetch, and prompts |

---

## 🔌 MCP Server Components

### 🛠️ Tools

Callable functions that perform actions. Defined with a decorator, e.g., in Python:

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b
```

### 📁 Resources

Read-only endpoints exposing structured data. Use direct or templated routes:

```python
# Direct resource
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs():
    return ["report.pdf", "notes.txt"]

# Templated resource
o@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str):
    with open(doc_id) as f:
        return f.read()
```

### 🧠 Prompt Templates

Pre-written templates for consistent LLM prompts:

```yaml
- id: summary
  template: |
    You are an expert assistant. Summarize the following document:
    {{content}}
```

---

## 🔁 Communication Lifecycle

1. **Initialization**

   1. Host (MCP Client) sends an `InitializeRequest`.
   2. Server responds with available tools, resources, and templates.
   3. Session becomes active.
2. **Message Exchange**

   * Client invokes tools or fetches resources via JSON messages.
   * Server executes actions or returns data.
3. **Termination**

   * Client closes the session; server cleanup occurs automatically.

---

## 🚀 Transport Modes

### 🖥️ Local Development

* **stdio (stdin/stdout)**: Embed server as a subprocess for fast, network-free prototyping.

### 🌍 Remote Deployment

1. **HTTP + SSE** (Protocol `2024-11-05`)

   * `POST /mcp` for requests
   * Server-Sent Events for streaming responses
2. **Streamable HTTP** (Protocol `2025-03-05`)

   * Single-shot or streaming (token-by-token)
   * Choose stateful or stateless mode

---

## 🔗 Example Flow with Claude

1. Claude (via MCP Client) requests:

   ```json
   { "tool": "summarize_doc", "args": { "doc_id": "meeting_2025-05-15.txt" } }
   ```
2. MCP Server fetches the file, applies the `summary` template, and returns:

   ```json
   { "summary": "Key action items..." }
   ```
3. Claude generates the final structured response.

---

## 🧰 Tooling & Ecosystem

* **Python MCP SDK**: Decorators for tools, resources, and prompt templates.
* **LangChain & Agents**: Integrate MCP servers into agent workflows.
* **IDE Plugins**: Use local MCP servers for document summarization or code assistance.

---

## 💡 Suggested Projects

* Google Drive file fetcher and summarizer.
* GitHub automation bot (commit, branch management).
* CRM manager to query and update records.
* Document Q\&A system using prompt templates.

---

## 📖 Resources

* Official Anthropic MCP Documentation
* DeepLearning.AI Short Course on MCP
* Example GitHub Repositories (Python, Node.js)

---

## 📝 Summary

MCP bridges LLMs and external systems by providing a **standard protocol** for tool invocation, data access, and templating. Its modular design reduces boilerplate, enhances reusability, and accelerates AI application development.
