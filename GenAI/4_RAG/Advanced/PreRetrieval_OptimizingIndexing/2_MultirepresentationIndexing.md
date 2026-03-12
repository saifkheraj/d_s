# Fixed Mermaid Diagrams

## Naïve RAG (single representation: raw chunks)

```mermaid
flowchart LR
    A[Raw docs] --> B[Chunker]
    B --> C[Embedding model]
    C --> D[(Vector store)]
    Q[User Query] --> QE[Query Embedding]
    QE --> D
    D --> K[Top-k chunks]
    K --> L[LLM]
    L --> R[Answer]
```

## Multi-Representation (summaries + originals via MultiVectorRetriever)

```mermaid
flowchart LR
    A[Full docs] --> S["LLM Summarizer<br/>(1..N summaries per doc)"]
    S --> E[Embedding model]
    E --> V[("Vector store: summary vectors<br/>+ metadata {doc_id}")]
    A --> DS[("Docstore: originals<br/>keyed by doc_id")]
    Q[User Query] --> QE[Query Embedding]
    QE --> V
    V -->|doc_id| DS
    DS --> F[Full docs / chosen chunks]
    F --> L[LLM]
    L --> R[Answer]
```

## Key Fixes Made:

1. **Multi-line labels**: Used `<br/>` instead of line breaks within node labels
2. **Edge labels**: Changed `-- doc_id -->` to `-->|doc_id|` for proper edge labeling syntax
3. **Consistent spacing**: Ensured proper indentation and spacing
4. **Quote protection**: Added quotes around multi-line node labels to prevent parsing issues

The main issues were:
- Line breaks within node labels need to use HTML `<br/>` tags
- Edge labels should use the `-->|label|` syntax instead of `-- label -->`
- Multi-line content in nodes should be wrapped in quotes
